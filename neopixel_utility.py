import logging
from colour import Color
import random
import math
from neopixel import PrinterNeoPixel

GAMMA_TABLE_STEPS=100

class NeopixelUtility(PrinterNeoPixel):
    def __init__(self, config):
        PrinterNeoPixel.__init__(self, config)
        name = config.get_name().split()[1]
        gcode = self.printer.lookup_object('gcode')
        self.reactor = self.printer.get_reactor()

        gcode.register_mux_command(
            "SET_LED_ANIM", "LED", name,
            self.cmd_SET_LED_ANIM,
            desc=self.cmd_SET_LED_ANIM_help)
        gcode.register_mux_command(
            "SET_LED_BLINK", "LED", name,
            self.cmd_SET_LED_BLINK)
        gcode.register_mux_command(
            "SET_LED_RANDO", "LED", name,
            self.cmd_SET_LED_RANDO)
        gcode.register_mux_command(
            "SET_LED_GRADIENT", "LED", name,
            self.cmd_SET_LED_GRADIENT)

    # Copied relevant parts from neopixels SET_LED cmd
    def _set_neopixels(self, red, green, blue, white=1., index=None, transmit=True):
        def reactor_bgfunc(print_time):
            with self.mutex:
                #logging.info("Setting: {0} {1} {2}".format(red, green, blue))
                self.update_color_data(red, green, blue, white, index)
                if transmit:
                    self.send_data(print_time)
        def lookahead_bgfunc(print_time):
            self.reactor.register_callback(lambda et: reactor_bgfunc(print_time))

        # No sync - just do it
        lookahead_bgfunc(None)

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

    def cmd_SET_LED_BLINK(self, params):
        #current_color_data = self.get_status(None)['color_data']
        self._set_neopixels(1.,1.,0.)
        logging.info(self.get_status(None)['color_data'])
        logging.info(self.get_status(None)['color_data'])
        logging.info('pause in')
        self._pause(1.)
        logging.info(self.get_status(None)['color_data'])
        logging.info('pause out')
        self._set_neopixels(0.,1.,0.)
        logging.info(self.get_status(None)['color_data'])
        self._pause(1)
        for i in range(1,self.chain_count):
            #logging.info("{0} {1}".format(i, colour))
            #self.update_color_data(random.random(), random.random(), random.random(), 0., i)
            self._set_neopixels(random.random(),random.random(),random.random(),index=i, transmit=False)
        logging.info(self.get_status(None)['color_data'])
        self._set_neopixels(1.,1.,1.,index=self.chain_count)
        logging.info(self.get_status(None)['color_data'])

    def cmd_SET_LED_GRADIENT(self, params):
        for i in range(1,self.chain_count):
            linear_gradient = float(i) / self.chain_count
            self._set_neopixels(*self._gamma_convert(Color(rgb=(linear_gradient,linear_gradient,linear_gradient))).rgb,index=i, transmit=False)
        self._set_neopixels(1.,1.,1.,index=self.chain_count)

    def cmd_SET_LED_RANDO(self, params):
        for i in range(1,self.chain_count):
            self._set_neopixels(random.random(),random.random(),random.random(),index=i, transmit=False)
        self._set_neopixels(1.,1.,1.,index=self.chain_count)

    cmd_SET_LED_ANIM_help = "Run an animation"
    def cmd_SET_LED_ANIM(self, params):
        # Parameters:
        # - GAMMA Default to 2, unless specified or defined already in config
        # - GAMMA_ADJUST Default to TRUE, unless specified or defined already in config
        # - SPEED Relative speed of animations to base ([0 to 10] -> default 1.)
        # - TERMINATE Length of time to run before terminating (for looping animations)



        # Animations (+ Animation Specific Parameters) / Separate into animations and allocations?  What about Rider?
        # Random
        # Rainbow
        # March  Direction, Speed, Steps
        # Pattern Pattern
        # Fade
        # Pulse
        # Solid Colour
        # Rider Pattern

        self.gcode.respond_info("this is a test")

        # ['__doc__', '__init__', '__module__', 'build_config', 'chain_count', 'cmd_SET_LED', 'cmd_SET_LED_help', 'color_data', 'color_order', 'get_status', 'mcu', 'mutex', 'neopixel_send_cmd', 'neopixel_update_cmd', 'oid', 'old_color_data', 'pin', 'printer', 'send_data', 'update_color_data']
        #logging.info(self.get_status(None)['color_data'])
        logging.info(params)
        logging.debug("Debug")
        pass
        # reactor = self.printer.get_reactor()
        # try:
        #     proc = subprocess.Popen(
        #         self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # except Exception:
        #     logging.exception(
        #         "shell_command: Command {%s} failed" % (self.name))
        #     raise self.gcode.error("Error running command {%s}" % (self.name))
        # if self.verbose:
        #     self.proc_fd = proc.stdout.fileno()
        #     self.gcode.respond_info("Running Command {%s}...:" % (self.name))
        #     hdl = reactor.register_fd(self.proc_fd, self._process_output)
        # eventtime = reactor.monotonic()
        # endtime = eventtime + self.timeout
        # complete = False
        # while eventtime < endtime:
        #     eventtime = reactor.pause(eventtime + .05)
        #     if proc.poll() is not None:
        #         complete = True
        #         break
        # if not complete:
        #     proc.terminate()
        # if self.verbose:
        #     if self.partial_output:
        #         self.gcode.respond_info(self.partial_output)
        #         self.partial_output = ""
        #     if complete:
        #         msg = "Command {%s} finished\n" % (self.name)
        #     else:
        #         msg = "Command {%s} timed out" % (self.name)
        #     self.gcode.respond_info(msg)
        #     reactor.unregister_fd(hdl)
        #     self.proc_fd = None

def load_config_prefix(config):
    return NeopixelUtility(config)
