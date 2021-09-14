Colours are defined using some syntax for the Colour library (https://github.com/vaab/colour).  
Colours can be listed by their human, web compatible representation (e.g. red), or by rgb values (rgb=(1,0,0)). 
Don't include any quote marks.

https://www.w3.org/TR/css-color-3/#svg-color

e.g. A custom pattern for red, white, and blue could be defined as CUSTOM=red|rgb=(1,1,1)|darkblue


source ~/klippy-env/bin/activate
pip install Colour
deactivate

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