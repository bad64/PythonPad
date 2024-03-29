[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Static Badge](https://img.shields.io/badge/Made_with-CircuitPython-orange)](https://github.com/adafruit/circuitpython)

# CircuitPython based all buttons all purpose (but mostly Smash) controller firmware

All of this info is at least pertinent to the RP2040. Haven't tested on any other CircuitPython compatible board yet, so there be dragons.

This is what powers my [Goblin](https://github.com/bad64/OpenFightStick/tree/main/Goblin) controller ! (Board files to be published as of this writing)

## What it do

This is supposed to be the followup to my Pico-SDK based PicoPad. It features:

- Human-readable and customizable keybindings, without needing to recompile or go through a web-based UI
- Code that is <sup>(allegedly[^1])</sup> easier to maintain and extend
- Far more verbose error reporting
- Portability to any device that supports CircuitPython

Surely there must be some huge tradeoffs compared to C, right ?

- It boots slightly slower (around 5 seconds on a Pico W)
- ...no really that's it

As far as I can tell it doesn't lag noticeably behind the C version -- someone with a better setup than mine might want to test that, because I cannot !

## How it do

Depends on:

- CircuitPython >= 8.2.9
- adafruit\_hid (available in the [CircuitPython Library Bundle](https://circuitpython.org/libraries))
- adafruit\_ticks.mpy (same as above)

Flash the CircuitPython UF2 file to your microcontroller, then extract the libs (that is both the MPY file and the entire `adafruit_hid` folder) to the `lib` directory of your CircuitPython drive. If you're having doubts, I suggest clicking on the CircuitPython badge at the top of this README, and follow their installation guide, though it will give you basically the same steps.

*Then* drag and drop the main files into the drive. Unplug and replug your device to make it run `boot.py` again.

> [!IMPORTANT]
> Your device ***must*** reload `boot.py`. The easiest way to achieve this is unplugging and replugging, but different boards might have different ways to achieve this.

## But how it do tho ?

Once you're all set up, when plugged into a computer, it will show up as both a HID device and a storage device because of CircuitPython [deep magic](http://www.catb.org/jargon/html/D/deep-magic.html). This drive should be invisible to consoles (maybe ? The Switch doesn't care about it at least) and hosts a variety of files. We will focus on four:

- `boot.py` contains the HID report descriptor and the HID init code. It's probably a good idea to leave it alone. **You can softlock yourself out of that drive if you freestyle too much.** (It's fixable by forcing your device into bootloader mode and reflashing CircuitPython though, but you still should be appropriately scared when doing things to this file)
- `GamepadDriver.py` is, as the name subtly implies, ~~a library to control your fridge via MQTT~~ the driver implementation of the Gamepad class. Again, probably best to not touch it, though it's a lot less sensitive than `boot.py`.
- `code.py` is the main loop. You can screw around with it, it's probably the one that is going to do the least damage to your flash memory, unless you decide to write whole megabytes to it for some reason
- And finally, `config.json`, used for binding keys to individual buttons in the report (Translation: *file makes board go brrt when press button*)

The file consists of pairs of keys and values (as most JSON files tend to be written as, at a surface level anyway). The keys are pin numbers (again, relative to the RP2040 and my own Hydra board; adapt to your own use), and the values correspond to which input is tied to that particular pin. This technically means you can tie an input to more than one pin, but one pin cannot trigger more than one input (nor is that a desirable feature, according to some rulesets. Consult your local TO for advice before use)

> [!NOTE]
> Said inputs follow the mapping of the Switch Pro Controller. Please be careful if you're more used to the Xbox mapping; face buttons are horizontally inverted (Y on the SPC is X on Xbox controllers, B on the SPC is A on Xbox, etc), L and R are LB and RB respectively, START is MENU and SELECT is BACK. C\_\* inputs correspond to the right stick (*not R3*, just directions on the right stick). MOD\_X and MOD\_Y don't exist on either controller and kinda do their own thing.

> [!NOTE]
> TODO: Write about inputs and how to configure them in more detail

In short: Edit `config.json` to map your inputs. If you're on Windows and can't see the `.json` file extension, [blame Microsoft](https://support.microsoft.com/en-us/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01) <sub>Really this decision leads to way more backdoors than you think it does</sub>

[^1]: I do miss pointers though...
