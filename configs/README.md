Here's the main config files I've written for the couple of MCUs I tested !

> [!IMPORTANT]
> Grab only one, drop it into the root of the `CIRCUITPYTHON` drive (where you put `code.py`), and **RENAME IT AS `config.json`. IT WILL NOT WORK IF YOU SKIP THAT STEP.**

If you want to change an input, pick a pin, then write a value based on the table below. Save the file; CircuitPython should automatically reload everything and you're good to go. For the Versus mode, you can use dedicated macros that correspond to a traditional arcade controller input scheme using the prefix "VS\_" (i.e.: VS\_1P, VS\_2K and so forth)

## Valid inputs

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
In short: Pick your base config file; upload it to your board, then rename it as `config.json`. Edit it with your favorite text editor to map your inputs. If you're on Windows and can't see the `.json` file extension, [blame Microsoft](https://support.microsoft.com/en-us/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01). <sub>Really this decision leads to way more backdoors than you think it does</sub>
---

## HELP ! My board stopped doing anything !!

Don't panic ! It's gonna be okay ! It just *appears* to be dead. It's not.

If you used the wrong file, or did some dodgy modifications, the firmware will fail to initialize and... that's it. It'll just sit there, waiting for you to write a valid config file to the drive.  
If you have a serial monitor, you can add `"debug": true` to the `"general"` section of your config file and use that to get more useful debug info.
