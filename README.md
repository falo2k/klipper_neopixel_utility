# Klipper Neopixel Pattern and Animation Utility

This module acts as an upgrade for the existing neopixel module to allow easy setting of patterns and animations in gcode.  To use the module in Klipper, replace your existing `[neopixel my_neopixels]` entry with `[neopixel_utiliy my_neopixels]`.  Existing neopixel commands like `SET_LED` will work as before.

## Features
- Ability to select a pattern of lights either from a predefined pattern, or by specifying a series of colours to repeat
- Ability to animate LEDs using either the starting state of the LEDs or a specific pattern for that animation
- Simple gamma correction to turn linear RGB values into something more aligned to a perceived linear brightness scale.

## Configuration
Configuration is the same as a standard `[neopixel]` block, with two optional configuration entries:
```
gamma: 2.7
# Sets the value used for gamma correction.  Defaults to 2.7, which seems a reasonable value for neopixels
gamma_adjust: True
# Enable or disable the gamma adjustment of the new functions.  Defaults to True.
```

## Commands
### Pattern Command
The basic pattern command is as follows:

`SET_LED_PATTERN LED=my_neopixels PATTERN=Random RANGE=1,10`

If no pattern is specified, then the pattern will be randomised.  The optional Range parameter defines which LEDs to change (inclusive).  Specific patterns have additional optional arguments.

#### Random
Rando rando rando
#### Gradient
ASCENDING=0/1
Currently white LEDs only
#### Custom
Custom repeating pattern
CUSTOM=red|green|blue|orange

Patterns should be delimited with pipe characters (`|`). Colours are defined using their [human, web compatible representation](https://www.w3.org/TR/css-color-3/#svg-color) (e.g. `red`), or by rgb values (e.g. `rgb=(1,0,0)`).  Don't include quote marks.

e.g. A custom pattern for red, white, and blue could be defined as `CUSTOM=red|rgb=(1,1,1)|darkblue`

### Animation Command
The basic animation command is as follows:

`SET_LED_ANIMATION LED=my_neopixels ANIMATION=March RANGE=1,10`

If no animation is specified, then the March animation will be used.  The optional Range parameter defines which LEDs to change (inclusive).  Specific animations have additional optional arguments.

#### March
ASCENDING=1
SPEED= 0.1
DURATION=5

#### Strobe
SPEED=0.05
COLOUR=red
DURATION=5
ASCENDING=1

#### March
#### Strobe

## TO DO
- Better error handling
- Slightly smarter gamma correction
- Make animations run in parallel
- Add more patterns (coloured gradient / palette)
- Add more animators (pulse, strobe, raindrops, lightning, fade, loading, etc.)
- Add a quick utility for taking a colour fom a palette - useful for things like temperature settings

## Installation
Checkout the repo in the home directory and install using the following commands:
```
cd ~
git clone https://github.com/falo2k/klipper_neopixel_utility.git
source ~/klippy-env/bin/activate
pip install Colour
deactivate
```


## Updates
Use the following block in your moonraker configuration for automatic updates.  This is currently set to the dev channel as it's a work in progress.

```
[update_manager neopixel_utility]
type: git_repo
path: ~/klipper_neopixel_utility
origin: https://github.com/falo2k/klipper_neopixel_utility.git
primary_branch: dev
#   The name of the primary branch used for release code on this repo.  This
#   option allows clients to specify 'main', or their own unique name, as
#   the branch used for repo validity checks.  The default is master.
#   dev is my testing branch, main should be stable
env:~/klippy-env/bin/python
requirements:requirements.txt
install_script: install.sh
#  Note that the install will put a symlink in ~/klipper/klippy/extras/ to use the
#  module
is_system_service: False
```