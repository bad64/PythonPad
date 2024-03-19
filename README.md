[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Static Badge](https://img.shields.io/badge/Made_with-CircuitPython-orange)](https://github.com/adafruit/circuitpython)

# CircuitPython based all buttons all purpose (but mostly Smash) controller firmware

This is what powers my [Goblin](https://github.com/bad64/OpenFightStick/tree/main/Goblin) and [Gnome](https://github.com/bad64/OpenFightStick/tree/main/Gnome) controllers !  
Here's what has been tested so far:

| Board | MCU | Works ? | Comments
| --- | --- | --- | --- | 
| Raspberry Pi Pico | RP2040 | &#9989; | Literally made for it |
| Adafruit Feather ESP32-S3 | ESP32-S3 | &#9989; | Tested on the 4MB Flash model|
| ESP32-S3-DevKitC-1-N8R2 | ESP32-S3 | &#9989; | Powers the One Board |

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

*Then* drag and drop the main files (see below) into the drive. Unplug and replug your device to make it run `boot.py` again.

> [!IMPORTANT]
> Your device ***must*** reload `boot.py`. The easiest way to achieve this is unplugging and replugging, but different boards might have different ways to achieve this.

## But how it do tho ?

Once you're all set up, when plugged into a computer, it will show up as both a HID device and a storage device because of CircuitPython [deep magic](http://www.catb.org/jargon/html/D/deep-magic.html). This drive should be invisible to consoles (maybe ? The Switch doesn't care about it at least) and hosts a variety of files. We will focus on four:

- `boot.py` contains the HID report descriptor and the HID init code. It's probably a good idea to leave it alone. **You can softlock yourself out of that drive if you freestyle too much.** (It's fixable by forcing your device into bootloader mode and reflashing CircuitPython though, but you still should be appropriately scared when doing things to this file)
- `GamepadDriver.py` is, as the name subtly implies, ~~a library to control your fridge via MQTT~~ the driver implementation of the Gamepad class. Again, probably best to not touch it, though it's a lot less sensitive than `boot.py`
- `code.py` is the main loop. You can screw around with it, it's probably the one that is going to do the least damage to your flash memory, unless you decide to write whole megabytes to it for some reason
- `VERSION` is an optional file telling the firmware to output its version number. Only really useful for debugging
- `CHANGELOG.md` and `LICENSE` can be ignored. They won't do anything when uploaded to the board anyway
- And finally, one configuration file, in JSON format. See the `config/` subdirectory and their associated README files

The file consists of pairs of keys and values (as most JSON files tend to be written as, at a surface level anyway). The keys are pin numbers (again, relative to the RP2040 and my own Hydra board; adapt to your own use), and the values correspond to which input is tied to that particular pin. This technically means you can tie an input to more than one pin, but one pin cannot trigger more than one input (nor is that a desirable feature, according to some rulesets. Consult your local TO for advice before use)

## Oh yeah there's a traditional versus fighting mode too

There are two ways to access Versus mode:  
- Hold the key associated to the mode as defined in your config file while plugging your controller
- In the "general" section of said config file, you can set `"defaultMode"` to `versus` 

The firmware will then boot into "Versus mode", which is simply a mode where inputs are remapped for a better 2D fighting game experience[^2]:

* Action buttons try to emulate the button placements on a traditional box
* Non-existent keys (typically both modifiers along with C-Down and A) map to the Up directional to approximate placement of said direction on a more well known button layout
* All directional inputs are considered d-pad inputs instead of analog
* C-stick gets yoten[^3]
* SOCD gets resolved to LRN & UDU[^4][^5]

## Updating the firmware

Updating is pretty easy: Connect your controller to a computer, and copy over the `boot.py`, `GamepadDriver.py`, `VERSION` (optional), and `code.py` files, overwriting those present on the CIRCUITPYTHON drive. In theory, you shouldn't have to overwrite `config.json` and should be able to keep your configuration across all versions. (If the controller stops working after such an update, try uploading the default version of that file again)

## Extending the firmware with new modes

> [!WARNING]
> This is for advanced users/tinkerers/people that already have a solid understanding of Python.
> 
> I may have made the underlying framework easy to use, but that comes at the cost of safety features. You shouldn't be able to actually brick your microcontroller (*hopefully*) from within CircuitPython, but I would keep backups on hand before any modification if I were you.

On paper, this is actually fairly straightforward, until you get to the actual implementation. (This happens to describe the field of programming as a whole, incidentally)

The first part is arguably the easiest one: Edit `config.json`; Add a new entry in the `modes` section, using a pin number as key and whatever name you want as a value[^6].Expand the file with a section using the same name as the one you just added. Technically the names do not need to match, but I follow the [KISS principle](https://en.wikipedia.org/wiki/KISS_principle) and so should you ! Anyway, copy the bindings from another existing section to give yourself a comfortable base to work with.

Now, into the dragon's den: `code.py`. Locate the section that goes "This is where you should add alternate modes"[^7]. Add your mode name to the conditional. And this is basically where I can no longer assist you: The world is your oyster, and if you know some basic Python (and can decipher the already present code), the biggest hurdle you will face will be directionals since all other inputs are handled about the same. Should you want to handle one differently for whatever reason, please do so within the relevant conditional instead of modifying the button reading loop directly.

## Troubleshooting/FAQ

Q: My gamepad stopped responding after I edited `config.json` ! Why ?  
A: You probably gave it either a bogus value (like a W button, which only exists on keyboards), or a pin number that isn't made up of two digits (i.e. pin *7* instead of *07*). Double check what you typed !

Q: Same question but for `code.py`  
A: This one is harder to diagnose properly through a non-interactive GitHub page. The short answer is that you're probably triggering an exception since, for diagnosis purposes, the main loop isn't encased in a `try ... except` block (I honestly don't know if I *should* do that tbh). In more concise terms: "Code bad". What you can do is use a serial monitor (such as TeraTerm on Windows or Minicom on anything \*NIX based... or, hell, the one bundled in the Arduino IDE if you have to; it just won't interpret VT100 escape sequences/color codes) and repeat whatever it is you did; the exception should show up on your serial monitor, and hopefully help you fix whatever causes it.

Q: Will this firmware work on board/MCU XYZ ?  
A: I dunno. I can't test every micro out there (even if I set up a Patreon to cover the costs, I just don't have the time). The nature of (Circuit)Python means that if the board can run the interpreter at all (and has physical USB peripheral pins), there's a fairly high chance PythonPad will work on it. With the caveat that you will then want to adapt the pinout by hand.

Q: Why should I use this instead of [GP2040-CE](https://gp2040-ce.info/) ?  
A: No shade thrown to them, it's a really good piece of firmware. *But*: 1) AFAIK GP2040-CE doesn't necessarily support Smash (which is the main target of PythonPad, and the FGC firmware being an extra, rather than the other way around), and 2) As the name implies, GP2040-CE runs on RP2040-based boards such as the Pico. If you want something else (STM32, nRF528xx, whatever it is the Teensy uses, etc), GP2040 won't work without some serious modification. PythonPad **should**.

Q: Will you add RGBLEDs/bluetooth/Nunchuk/Ring Fit/etc support ?  
A: I *might*. Currently I'm developing this for an ESP32-S3 based board and I almost maxed out the I/O on it as it is. Maybe once I start daisy chaining MCUs via the power of I2C. Never say never !  
*Update 11/03/2024: RGB strips are supported on the One Board, assigned to IO9 ! No code for it yet though, but at least the hardware is here*

## TODO

- SOCD cleaning types
- Decoupling input poll routines from the main loop/file
- Safe testing for every input
- Testing on other common microcontrollers
- Analog ?

[^1]: I do miss pointers though...
[^2]: It works pretty well on Tekken 8 too !
[^3]: Past participle of "to yeet"
[^4]: **L**eft + **R**ight = **N**eutral, **U**p + **D**own = **U**p
[^5]: Again depending on the game you play, tournament organizer, frequency of whalesong, and so on, this might not be a legal config. Always consult your local TO for advice !
[^6]: Murphy's law says someone will eventually try to name one with emojis or non-printable characters, so consider this footnote as a proverbial and quasi literal asterisk
[^7]: Not hyperbole, this is the string you want to search for in your editor
