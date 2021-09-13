import logging
from colour import Color
import random
import math
import ast
import sys
import collections
from neopixel import PrinterNeoPixel


GAMMA_TABLE_STEPS=100
Pattern = collections.namedtuple('Pattern','name function')

class NeopixelUtility(PrinterNeoPixel):
    def __init__(self, config):
        PrinterNeoPixel.__init__(self, config)
        name = config.get_name().split()[1]
        self.gcode = self.printer.lookup_object('gcode')
        self.reactor = self.printer.get_reactor()

        self.gamma = config.get('gamma', 2.7)
        self.gamma_adjust = config.getboolean('gamma_adjust', True)
        self.gamma_table = self._gamma_table(GAMMA_TABLE_STEPS, self.gamma)

        self.gcode.register_mux_command(
            "SET_LED_PATTERN", "LED", name,
            self.cmd_SET_LED_PATTERN,
            desc=self.cmd_SET_LED_PATTERN_help)

        self.gcode.register_mux_command(
            "SET_LED_ANIMATION", "LED", name,
            self.cmd_SET_LED_ANIMATION,
            desc=self.cmd_SET_LED_ANIMATION_help)

    # Parameters:
    # - SPEED Relative speed of animations to base ([0 to 10] -> default 1.)
    # - TERMINATE Length of time to run before terminating (for looping animations)
    # - RANGE Allow a subset of pixels to be set?


    # Animations (+ Animation Specific Parameters) / Separate into animations and allocations?  What about Rider?
    # Random
    # Rainbow (repeat vs full range)
    # March  Direction, Speed, Steps
    # Pattern Pattern
    # Fade
    # Pulse
    # Solid Colour
    # Rider Pattern
    # Loading pattern (slowly fills up full lights - loadtofull?)
    # Lightning
    # Raindrops

    cmd_SET_LED_PATTERN_help = "Set a static pattern for the LEDs"
    def cmd_SET_LED_PATTERN(self, params):
        #logging.debug(self.get_status(None)['color_data'])
        pattern = params.get('PATTERN', 'Unknown')
        limits = map(int,params.get('RANGE', '1,{0}'.format(self.chain_count)).split(','))

        patterns = [
            Pattern('random', self.__pattern_random),
            Pattern('gradient', self.__pattern_gradient),
            Pattern('custom', self.__pattern_custom)
        ]

        pattern_list = map(str.lower,list(zip(*patterns))[0])

        if pattern.lower() not in pattern_list:
            pattern = 'random'
            self.gcode.respond_info(
                'Using random pattern.  Please select a pattern using' \
                ' PATTERN= and pass one of the following'\
                ' patterns: {}'.format(', '.join(pattern_list)))

        func = [x.function for x in patterns if x.name == pattern.lower()][0]
        #logging.debug(pattern)
        #logging.debug(func)
        func(params, limits)

    cmd_SET_LED_ANIMATION_help = "Start an animation"
    def cmd_SET_LED_ANIMATION(self, params):
        self._set_neopixels(1.,1.,1.)
        self._set_neopixels(.5,.5,.5)
        logging.debug(self.get_status(None)['color_data'])
        self._pause(0.05)
        logging.debug(self.get_status(None)['color_data'])
        self._pause(0.05)
        logging.debug(self.get_status(None)['color_data'])
        self._pause(0.05)
        logging.debug(self.get_status(None)['color_data'])
        pass

    def __pattern_gradient(self, params, limits):
        ascending = params.get_int('ASCENDING', 1)

        if ascending:
            for i in range(1,self.chain_count):
                linear_gradient = float(i) / self.chain_count
                c = Color(rgb=(linear_gradient,linear_gradient,linear_gradient))
                self._set_neopixels(*c.rgb, index=i, transmit=False)
            self._set_neopixels(1.,1.,1.,index=self.chain_count)
        else:
            for i in range(self.chain_count,1,-1):
                linear_gradient = float(self.chain_count - i + 1) / self.chain_count
                c = Color(rgb=(linear_gradient,linear_gradient,linear_gradient))
                self._set_neopixels(*c.grb, index=i, transmit=False)
            self._set_neopixels(1.,1.,1.,index=1)

    def __pattern_random(self, params, limits):
        for i in range(limits[0],limits[1]):
            self._set_neopixels(random.random(),random.random(),random.random(),index=i, transmit=False)
        self._set_neopixels(1.,1.,1.,index=limits[1])

    def __pattern_custom(self, params, limits):
        custom = params.get('CUSTOM', '')
        if custom == '':
            self.gcode.respond_info(
                'Please define  a pattern using CUSTOM=.  See the' \
                ' documentation for details.  Defaulting to red|white|blue')
            custom = 'red|white|blue'


        colour_pattern = []
        colour_pattern_strings = [x for x in custom.split('|')]
        for string in colour_pattern_strings:
            try:
                if string.strip().startswith('rgb') and ('=' in string):
                    colour_pattern.append(Color(rgb=ast.literal_eval(string.split('=')[1])))
                else:
                    colour_pattern.append(Color(string))
            except:
                logging.debug('Exception: {0}'.format(sys.exc_info()[0]))
                self.gcode.respond_info(
                'Could not intepret {0} as a colour.  Please check' \
                ' the documentation.  Replacing entry with white'.format(string))
                colour_pattern.append(Color('white'))

        pattern_length = len(colour_pattern)
        if pattern_length == 0:
            self.gcode.respond_info(
                'Pattern is empty.  Defaulting to red|white|blue')
            colour_pattern = [Color('red'), Color('white'), Color('blue')]
            pattern_length = 3
        chain_length = limits[1] - limits[0] + 1
        q, r = divmod(chain_length, pattern_length)

        for i in range(q):
            start = limits[0] + (i * pattern_length)
            for j in range(pattern_length):
                transmit = (i == q-1) and (r==0)
                self._set_neopixels(*colour_pattern[j].rgb, index=(start+j), transmit=transmit)

        if r > 0:
            self.gcode.respond_info('q:{0} r:{1}'.format(q,r))
            start = limits[0] + (q * pattern_length)
            for i in range(r):
                transmit = (i == r-1)
                self._set_neopixels(*colour_pattern[i].rgb, index=(start+i), transmit=transmit)

    def _gamma_lookup(self, number):
        return self.gamma_table[int(round((GAMMA_TABLE_STEPS-1) * number))]

    def _gamma_convert(self, colour):
        return Color(rgb=map(self._gamma_lookup, colour.rgb))

    def _gamma_table(self, nsteps, gamma):
        gammaedUp = [math.pow(x, gamma) for x in range(nsteps)]
        return [x/max(gammaedUp) for x in gammaedUp]

    def _pause(self, time=0.):
        eventtime = self.reactor.monotonic()
        end  = eventtime + time
        while eventtime < end:
            eventtime = self.reactor.pause(eventtime + .05)

    # Copied relevant parts from neopixels SET_LED cmd
    def _set_neopixels(self, red, green, blue, white=0., index=None, transmit=True):
        def reactor_bgfunc(print_time):
            with self.mutex:
                c = Color(rgb=(red,green,blue))
                if self.gamma_adjust:
                    c = self._gamma_convert(c)

                #logging.info("Setting: {0} {1} {2}".format(red, green, blue))
                self.update_color_data(*c.rgb, white=white, index=index)
                if transmit:
                    self.send_data(print_time)
        def lookahead_bgfunc(print_time):
            self.reactor.register_callback(lambda et: reactor_bgfunc(print_time))

        # No sync - just do it
        lookahead_bgfunc(None)

def load_config_prefix(config):
    return NeopixelUtility(config)
