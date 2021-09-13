Colours are defined using some syntax for the Colour library (https://github.com/vaab/colour).  
Colours can be listed by their human, web compatible representation (e.g. red), or by rgb values (rgb=(1,0,0)). 
Don't include any quote marks.

https://www.w3.org/TR/css-color-3/#svg-color

e.g. A custom pattern for red, white, and blue could be defined as CUSTOM=red|rgb=(1,1,1)|darkblue


[update_manager neopixel_animations]
type: git_repo
path: ~/klipper_neopixel_utility
origin: 
#   The full git URL of the "origin" remote for the repository.  This can
#   be be viewed by navigating to your repository and running:
#     git remote -v
#   This parameter must be provided.
primary_branch:
#   The name of the primary branch used for release code on this repo.  This
#   option allows clients to specify 'main', or their own unique name, as
#   the branch used for repo validity checks.  The default is master.
env:~/klippy-env/bin/python
#   The path to the client's virtual environment executable on disk.  For
#   example, Moonraker's venv is located at ~/moonraker-env/bin/python.
#   The default is no env, which disables updating python packages.
requirements:requirements.txt
#  This is the location in the repository to the client's virtual environment
#  requirements file. This location is relative to the root of the repository.
#  This parameter must be provided if the "env" option is set, otherwise it
#  should be omitted.
install_script: install.sh
#  The file location, relative to the repository, for the installation script.
#  The update manager parses this file for "system" packages that need updating.
#  The default is no install script, which disables system package updates
host_repo:
#   The GitHub repo in which zipped releases are hosted.  Note that this does
#   not need to match the repository in the "origin" option, as it is possible
#   to use a central GitHub repository to host multiple client builds.  As
#   an example, Moonraker's repo hosts builds for both Moonraker and Klipper.
#   This option defaults to the repo extracted from the "origin" option,
#   however if the origin is not hosted on GitHub then this parameter must
#   be provided.
is_system_service: False