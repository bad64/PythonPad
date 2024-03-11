Here's the main config files I've written for the couple of MCUs I tested !

> [!IMPORTANT]
> Grab only one, drop it into the root of the `CIRCUITPYTHON` drive (where you put `code.py`), and **RENAME IT AS `config.json`. IT WILL NOT WORK IF YOU SKIP THAT STEP.**

## HELP ! My board stopped doing anything !!

Don't panic ! It's gonna be okay ! It just *appears* to be dead. It's not.

If you used the wrong file, or did some dodgy modifications, the firmware will fail to initialize and... that's it. It'll just sit there, waiting for you to write a valid config file to the drive.  
If you have a serial monitor, you can add `"debug": true` to the `"general"` section of your config file and use that to get more useful debug info.

## Valid inputs

| --- | --- | --- | ---
| UP | DOWN | LEFT | RIGHT |
| A | B | X | Y |
| R | ZR | L | ZL |
| START | SELECT | HOME | |
| L3 | R3 | MOD\_X | MOD\_Y |
| C\_UP | C\_DOWN | C\_LEFT | C\_RIGHT |
| VS\_1P | VS\_2P | VS\_3P | VS\_4P |
| VS\_1K | VS\_2K | VS\_3K | VS\_4K |

## Editing guide

TODO
