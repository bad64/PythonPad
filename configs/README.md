Here's the main config files I've written for the couple of MCUs I tested !

> [!IMPORTANT]
> Grab only one, drop it into the root of the `CIRCUITPYTHON` drive (where you put `code.py`), and **RENAME IT AS `config.json`. IT WILL NOT WORK IF YOU SKIP THAT STEP.**

If you want to change an input, pick a pin, then write a value based on the table below. Save the file; CircuitPython should automatically reload everything and you're good to go. For the Versus mode, you can use dedicated macros that correspond to a traditional arcade controller input scheme using the prefix "VS\_" (i.e.: VS\_1P, VS\_2K and so forth)

# Sections

## General

If you're missing this section, the firmware will assume a lot of default stuff. It'll still *work* though. All of these properties are *technically* optional:

- `debugMode`: Turns on debug mode. This is probably useless to you as an end user. True or false, defaults to false
- `defaultMode`: The default mode in which the firmware starts up. Said mode **must** be defined in the "modes" section. Defaults to "smash"

## Modes

If you're missing this, nothing changes. You just won't be able to select a mode at boot time
All key/value pairs are user defined and there is no set standard; I recommend defining at least one key to boot into `bootloader` mode. All pin numbers **must** be made of two digits (e.g. pin "07" instead of "7").

## Every user-definable mode

You need at least one. I would recommend defining a `smash` section at least due to the firmware defaulting to it.

- `canonName`: Optional. Gives your config a more verbose name for debugging purposes. No use for an end user
- `socdType`: Optional. Sets the cleaning type to use for this config. Accepts "LRN" (for Left+Right=Neutral), and any of "LIW", "lastInputWins", "last" for Last Input Wins (duh). Defaults to "LRN"
- Pin numbers: Mandatory. Ties a pin to a host-side input (so technically an output from the firmware's perspective). Multiple pins can be tied to the same input. See chart below for accepted values:

| Inputs | Inputs | Inputs | Inputs |
| --- | --- | --- | --- |
| UP | DOWN | LEFT | RIGHT |
| A | B | X | Y |
| R | ZR | L | ZL |
| START | SELECT | HOME | |
| L3 | R3 | MOD\_X | MOD\_Y |
| C\_UP | C\_DOWN | C\_LEFT | C\_RIGHT |
| VS\_1P | VS\_2P | VS\_3P | VS\_4P |
| VS\_1K | VS\_2K | VS\_3K | VS\_4K |

> [!IMPORTANT]
> Those inputs above follow the mapping of the Switch Pro Controller. Please be careful if you're more used to the Xbox mapping:
>
> (From Switch Pro Controller to Xbox mappings)
> * Y <-> X
> * B <-> A
> * R -> RB
> * ZR -> RT
> * L -> LB
> * ZL -> LT
> * \+ (aka START in the config file) -> Share
> * \- (aka SELECT in the config file) -> View
> * HOME -> giant Xbox button type thing 

Out of an abundance of caution, you should not alter the number of pins defined in a config file. If a pin isn't defined in the config file, there is usually a very good reason ! Beware of [dragons](https://en.wikipedia.org/wiki/Here_be_dragons).

---

Tl;dr: Pick your base config file; upload it to your board, then rename it as `config.json`. Edit it with your favorite text editor to map your inputs. If you're on Windows and can't see the `.json` file extension, [blame Microsoft](https://support.microsoft.com/en-us/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01). <sub>Really this decision leads to way more backdoors than you think it does</sub>

---

## HELP ! My board stopped doing anything !!

Don't panic ! It's gonna be okay ! It just *appears* to be dead. It's not.

If you used the wrong file, or did some dodgy modifications, the firmware will fail to initialize and... that's it. It'll just sit there, waiting for you to write a valid config file to the drive.  
If you have a serial monitor, you can add `"debug": true` to the `"general"` section of your config file and use that to get more useful debug info.
