[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)![Static Badge](https://img.shields.io/badge/CircuitPython-orange)

# CircuitPython based all buttons all purpose controller firmware

All of this info is at least pertinent to the RP2040. Haven't tested on any other CircuitPython compatible board yet, so there be dragons.

## What it do

This is supposed to be the followup to my Pico-SDK based PicoPad. It features:

- Human-readable and customizable keybindings
- Code that is (allegedly) easier to maintain and extend
- Far more verbose error reporting

Surely there must be some huge tradeoffs compared to C, right ?

- It boots slightly slower (around 5 seconds)
- ...no really that's it

As far as I can tell it doesn't lag noticeably behind the C version -- someone with a better setup than mine might want to test that, because I cannot !

## How it do

Depends on:

- CircuitPython >= 8.2.9
- adafruit\_hid (available in the Adafruit MPY bundle)
- adafruit\_ticks.mpy (same as above)

Flash the CircuitPython UF2 file to your microcontroller, then extract the libs (that is both the MPY file and the entire `adafruit_hid` folder) to the `lib` directory of your CircuitPython drive. If you're having doubts, I suggest clicking on the CircuitPython badge and follow their installation guide, though it will give you about the same steps.

*Then* drag and drop the main files into the drive. Unplug and replug your device to make it run `boot.py` again. **THIS IS IMPORTANT. IT WILL NOT WORK WITHOUT A FULL RESET.**

## TODO

- FGC mode (extra modes in general)
- `code.py` cleanup
