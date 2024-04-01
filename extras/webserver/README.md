# Ad-hoc webserver configurator hybrid thingamajig

~~Absolutely not inspired by GP2040~~

Oh boy this one is a dragon and a half. It's a very, *very* unfinished WIP that I mayr or may not complete someday.  
Currently it only views configuration files, it doesn't allow one to edit them. (This might not even be possible on CircuitPython)

## How do

Install the `adafruit_httpserver` library (refer to the top level README, it's in the Adafruit library package). Copy and paste both `localserver.py` and the `webserver` folder at the root of the CIRCUITPYTHON drive. **Edit localserver.py to modify your access point parameters.**

Plug in your controller; it will create a wireless access point with a 10.0.0.0 subnet. Use whatever terminal you see fit to connect to it. Marvel at your configuration file.

## TODO

- Editing configuration file
