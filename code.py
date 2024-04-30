# UART print functions
from uart import RED, YELLOW, GREEN, CYAN, BLUE, VIOLET, DEFAULT, INFO, WARN, ACTION, ERROR, DEBUG, OK, KO, CONFUSED

print(f"{ACTION()} Initializing PythonPad")
# Display version for debugging purposes
try:
    with open("VERSION") as f:
        versionString = f.read()
        print(f"{INFO()} Version {versionString}", end="")
except:
    print("{CONFUSED()} VERSION file not found; skipping check")

# CircuitPython imports
import asyncio
import board
import digitalio
import json
import microcontroller
import time
import traceback
import usb_hid

# Runtime exceptions
import custom_runtime_exceptions as cre

# Hardware watchdog
from watchdog import WatchDogMode, WatchDogTimeout
wdt = microcontroller.watchdog
wdt.mode = None
wdt.timeout = 5

# Main gamepad driver
from gamepad_driver import Gamepad, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, HAT_CENTER 
gp = Gamepad(usb_hid.devices)

# Generic error handler with optional panic
def errorhandler(e, panic=False):
    print(f"{ERROR()} {RED}{type(e)}: ", end="")
    if "message" in dir(e):
        print(e.message, end="")
    else:
        print(e, end="")
    print(f"{DEFAULT}")

    if panic:
        while(True):
            pass

# Defining physical states
HIGH = True
LOW = False

# Don't go all the way, the Switch doesn't really like that and will wrap around once in a blue moon
MIN_TILT = 1
CENTER = 127
MAX_TILT = 254

from legacy import *

# Defining a pin prefix
## TODO: Add more board defs
prefix = "GP"
if "adafruit_feather_esp32s3" in board.board_id:
    prefix = "D"
elif "espressif_esp32s3" in board.board_id:
    prefix = "IO"

# Anthropomorphic definition of a Button
class Button:
    def __init__(self, pin, mappedInput):
        # Declares a Button, with its associated pin and output
        self._pins = [ int(pin) ]
        try:
            self._mask = eval("MASK_{}".format(mappedInput))
        except:
            self._mask = None
        self._io = [ eval("digitalio.DigitalInOut(board.{}{})".format(prefix, int(pin))) ]
        self._io[0].switch_to_input()
        self._io[0].pull = digitalio.Pull.UP
    def addPin(self, pin):
        # Adds a pin to poll for a given input (allows for tying multiple keys to the same function)
        self._pins.append(pin)
        self._io.append(eval("digitalio.DigitalInOut(board.{}{})".format(prefix, int(pin))))
        self._io[-1].switch_to_input()
        self._io[-1].pull = digitalio.Pull.UP
    def read(self):
        # Returns the state of the button
        for io in self._io:
            if io.value == False:
                return LOW
        return HIGH
    def mask(self):
        # Returns the bitmask attached to the button (Mostly used for debugging purposes)
        return self._mask

# Parse config from JSON file
cfg = {}
debugMode = False

print(f"{ACTION()} Reading config...")
with open("config.json") as f:
    cfg = json.load(f)

## General config stuff
## Ideally this is where one would control output verbosity and things like that
## TODO: Find "things like that"
try:
    for item in cfg["general"]:
        if item == "debug" and cfg["general"][item] == True:
            debugMode = True
            if debugMode == True:
                print(f"{INFO()}{GREEN}\t> Debug mode ON{DEFAULT}")
                time.sleep(1)
        elif item == "motd" and cfg["general"][item] == "knock knock":
            import random
            motd = [ "Obtained Narpas' sword",
                    "Found a X-X!V''Q",
                    "Look to la luna",
                    "Hornbuckle who ?",
                    "Wololo !",
                    "LET'S GO JUSTIN BAILEY !!",
                    "You must defeat Sheng Long to stand a chance",
                    "Go home and be a family man !",
                    "Go to www.thiefwithguns.com",
                    "Go to www.devilmayquake.com",
                    "Lamp oil ? Rope ? Bombs ? It's all yours, my friend ! So long as you have enough rubies...",
                    "Hello, stranger !",
                    "Smashing Pumpkins Into Some Pile Of Putrid Debris !",
                    "Did you know: entering Up, Up, Down, Down, Left, Right, Left, Right, B, A, and Start during the boot up sequence does nothing !"
                    ]
            r = random.randint(0, len(motd)-1)
            print(f"{INFO()}{CYAN}\t> {motd[r]}{DEFAULT}")
            time.sleep(1)
except KeyError:
    # If for whatever reason we do not have a "general" section
    # we just skip this and pray to the dark gods
    pass

# Mode selection
print(f"{INFO()} Running pre-checks")
print(f"{ACTION()} Selecting mode... ", end="")
mode = "smash"              ## We default to Smash mode in case of invalid or missing option

## Attempt to read default mode from config
warn_user_about_absent_default_mode = False
warn_user_about_wrong_default_mode = False
try:
    mode = cfg["general"]["defaultMode"]

    if mode in cfg["modes"].values() and mode != "bootloader":
        pass
    else:
        raise cre.WrongDefaultModeException(mode)
except KeyError:
    ### Set flag for warning user down the line
    warn_user_about_absent_default_mode = True
except cre.WrongDefaultModeException:
    warn_user_about_wrong_default_mode = True

## Scan for mode selection
try:
    for k,v in cfg["modes"].items():
        b = Button(k, None)
        if b.read() == LOW:
            if v == "bootloader":
                print(f"{OK()}")
                print(f"{INFO()} We gotta reboot !")
                time.sleep(2)
                microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
                microcontroller.reset()
            else:
                mode = v
        b._io[0].deinit()  # Free the io pin for rebinding later
except Exception as e:
    errorhandler(e)

## Print out to serial
if warn_user_about_absent_default_mode:
    print("\"{}???{}\" {}".format(RED, DEFAULT, KO()))
    print(f"{WARN()} \"defaultMode\" property missing from the \"general\" section of the config; Defaulting to \"{GREEN}smash{DEFAULT}\" mode")

    mode = "smash"
elif warn_user_about_wrong_default_mode:
    print("\"{}{}{}\" {}".format(RED, mode, DEFAULT, KO()))
    print(f"{WARN()} \"{RED}{mode}{DEFAULT}\" is not a cromulent default value; Defaulting to \"{GREEN}smash{DEFAULT}\" mode")

    mode = "smash"
else:
    try:
        print("\"{}{}{}\" {}".format(GREEN, cfg[mode]["canonName"], DEFAULT, OK()))
    except KeyError:
        print("\"{}{}{}\" {}".format(GREEN, mode, DEFAULT, OK()))
        if debugMode:
            print(f"{DEBUG()} No \"{RED}canonName{DEFAULT}\" property for mode \"{GREEN}{mode}{DEFAULT}\"")

# SOCD selection
print(f"{ACTION()} Setting up SOCD cleaning... ", end="")
gp.set_socd_type("LRN")     ## Again, default value for safety
try:
    gp.set_socd_type(cfg[mode]["socdType"])

    if mode not in [ "cpt" ]:   # List subject to expansion
        if gp.get_socd_type() in [ "LRN", "last", "LIW", "lastInputWins" ]:
            print(f"{OK()}")
            print(f"{INFO()} Set SOCD cleaner to \"{GREEN}{gp.get_socd_type()}{DEFAULT}\"")
        else:
            raise cre.WrongSOCDCleaningTypeException(gp.get_socd_type())
    else:
        print(f"{OK()}")
        if mode == "cpt":
            print(f"{INFO()} Set SOCD cleaner to \"{GREEN}Capcom Pro Tour{DEFAULT}\" compliant mode")
except KeyError:
    print(f"{CONFUSED()}")
    print(f"{WARN()} SOCD cleaner type absent; defaulting to \"{GREEN}LRN{DEFAULT}\"")
    gp.set_socd_type("LRN")
except cre.WrongSOCDCleaningTypeException as e:
    print(f"{KO()}")
    print(f"{WARN()} \"{RED}{e.mode}{DEFAULT}\" does not name an SOCD cleaning type; defaulting to \"{GREEN}LRN{DEFAULT}\"")
    gp.set_socd_type("LRN")

# Input binding
AllButtons = { "leftAnalog": {}, "rightAnalog": {}, "modifiers": {}, "buttons": [] }

print(f"{ACTION()} Loading config: \"{GREEN}{mode}{DEFAULT}\"")

## Deal with the modifiers first
### Save cycles by precalculating tilt values
xAxisModXDelta = CENTER - round(CENTER * (2/3))
xAxisModYDelta = CENTER - round(CENTER * (1/3))
yAxisModXDelta = CENTER - round(CENTER * (2/3))
yAxisModYDelta = CENTER - round(CENTER * (1/3))

for k,v in cfg[mode].items():
    if k == "X_AXIS_MOD_X_DELTA":
        try:
            xAxisModXDelta = round(int(eval(v)))
            print(f"{INFO()} Set X axis MOD_X delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set X axis MOD_X delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set X axis MOD_X delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "X_AXIS_MOD_Y_DELTA":
        try:
            xAxisModYDelta = round(int(eval(v)))
            print(f"{INFO()} Set X axis MOD_Y delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set X axis MOD_Y delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set X axis MOD_Y delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "Y_AXIS_MOD_X_DELTA":
        try:
            yAxisModXDelta = round(int(eval(v)))
            print(f"{INFO()} Set Y axis MOD_X delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_X delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_X delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "Y_AXIS_MOD_Y_DELTA":
        try:
            yAxisModYDelta = round(int(eval(v)))
            print(f"{INFO()} Set Y axis MOD_Y delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_Y delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_Y delta value to \"{v}\": {e}{DEFAULT}")

## Printing axis values over UART just to be sure nothing is on fire
if debugMode and mode == "smash":
    print(f"{DEBUG()} X axis values:")
    print(f"{DEBUG()}   ModX delta:     {xAxisModXDelta}")
    print(f"{DEBUG()}   ModY delta:     {xAxisModYDelta}")
    print(f"{DEBUG()}   LEFT:           {MIN_TILT}")
    print(f"{DEBUG()}   LEFT MOD_X:     {round(CENTER - xAxisModXDelta)}")
    print(f"{DEBUG()}   LEFT MOD_Y:     {round(CENTER - xAxisModYDelta)}")
    print(f"{DEBUG()}   CENTER:         {CENTER}")
    print(f"{DEBUG()}   RIGHT MOD_Y:    {round(CENTER + xAxisModYDelta)}")
    print(f"{DEBUG()}   RIGHT MOD_X:    {round(CENTER + xAxisModXDelta)}")
    print(f"{DEBUG()}   RIGHT:          {MAX_TILT}")

    print(f"{DEBUG()} Y axis values:")
    print(f"{DEBUG()}   ModX delta:     {yAxisModXDelta}")
    print(f"{DEBUG()}   ModY delta:     {yAxisModYDelta}")
    print(f"{DEBUG()}   UP:             {MIN_TILT}")
    print(f"{DEBUG()}   UP MOD_X:       {round(CENTER - yAxisModXDelta)}")
    print(f"{DEBUG()}   UP MOD_Y:       {round(CENTER - yAxisModYDelta)}")
    print(f"{DEBUG()}   CENTER:         {CENTER}")
    print(f"{DEBUG()}   DOWN MOD_Y:     {round(CENTER + yAxisModYDelta)}")
    print(f"{DEBUG()}   DOWN MOD_X:     {round(CENTER + yAxisModXDelta)}")
    print(f"{DEBUG()}   DOWN:           {MAX_TILT}")

## Now the rest of the inputs
for k,v in cfg[mode].items():
    try:
        int(k)  # If the key isn't an int, it *has* to be a modifier value;
                # We have already dealt with those above so we catch the exception
                # and skip over to the next item in line
        if v != "None":
            if v in [ "UP", "DOWN", "LEFT", "RIGHT" ]:
                try:
                    AllButtons["leftAnalog"][v].addPin(k)
                except KeyError:
                    AllButtons["leftAnalog"][v] = Button(k, v)
            elif v in [ "C_UP", "C_DOWN", "C_LEFT", "C_RIGHT" ]:
                # We don't specifically catch those in versus mode
                # because we just don't parse for right stick inputs
                # ...
                # Not that it would hurt to do so !
                try:
                    AllButtons["rightAnalog"][v].addPin(k)
                except KeyError:
                    AllButtons["rightAnalog"][v] = Button(k, v)
            elif v in [ "MOD_X", "MOD_Y", "MOD_V", "MOD_W" ]:
                try:
                    AllButtons["modifiers"][v].addPin(k)
                except KeyError:
                    AllButtons["modifiers"][v] = Button(k, v) 
            else:
                    AllButtons["buttons"].append(Button(k, v))
            if debugMode == True:
                print(f"{INFO()} Bound key \"{GREEN}{v}{DEFAULT}\" to input on pin {BLUE}{k}{DEFAULT}")
    except ValueError as e:
        # This is expected behaviour; we merely hide it to the UART interface
        # See beginning of the try/except block
        pass
    except Exception as e:
        # Another exception has occured; we catch that and show
        # TODO: Maybe determine if the exception is recoverable ?
        if debugMode == True:
            print(f"{WARN()} Attempted to bind key \"{v}\" to pin {k} but failed")
            print(f"{WARN()} {type(e)}: {e}")

# Import functions from the appropriate file
try:
    try:
        runtime_file = cfg[mode]["file"]
    except KeyError:
        runtime_file = mode
    print(f"{ACTION()} Importing main loop functions from {runtime_file}.py... ", end="")
    exec(f"from {runtime_file} import check_import, directionals")
    if check_import() == True:
        print(f"[{GREEN}OK{DEFAULT}]")
    else:
        raise ImportError
except Exception as e:
    print(f"[{RED}KO{DEFAULT}]")
    errorhandler(e, panic=True)

# If we have a server set up, start it now
has_server = False
try:
    import localserver
    has_server = localserver.check_import()
    print(f"{INFO()} Server code detected !")
except ImportError:
    # Mask the error, it just means we don't have one
    if debugMode == True:
        print(f"{DEBUG()} Server config not found; skipping webserver")
except Exception as e:
    # Don't mask the error, it might not be harmless at all
    errorhandler(e)

if has_server:
    try:
        localserver.localserver.start(str(localserver.wifi.radio.ipv4_address_ap))
        print(f"{INFO()} Local server started with SSID \"{GREEN}{localserver.ap_ssid}{DEFAULT}\" on {GREEN}{str(localserver.wifi.radio.ipv4_address_ap)}{DEFAULT}")
    except Exception as e:
        print(f"{ERROR()} {RED}Local server failed to start !!{DEFAULT}")
        errorhandler(e)

# Define action button polling as asynchronous to the main loop
#async def poll_buttons():
def poll_buttons():
    for b in AllButtons["buttons"]:
        if b.read() == LOW:
            gp.press_button(b.mask())
    #await asyncio.sleep_ms(0)

#async def main():
def main():
    while True:
        try:
            # Buttons
            ## This is shared between all modes, don't touch it
            gp.reset_buttons()
            #await asyncio.gather(poll_buttons())
            poll_buttons()

            # Handle directional input in separate files for easier readability
            x = CENTER
            y = CENTER
            z = CENTER
            rz = CENTER

            ## TODO: de-fuglify this call smh
            directionals(gp, AllButtons, x, y, z, rz, LOW, HIGH, \
                    HAT_CENTER, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, \
                    CENTER, MIN_TILT, MAX_TILT, xAxisModXDelta, xAxisModYDelta, yAxisModXDelta, yAxisModYDelta)

            # Finally send the report, yay !
            gp.send()

            # If we have a server running, poll and handle requests
            if has_server:
                try:
                    pool_result = localserver.localserver.poll()
                    if pool_result == localserver.REQUEST_HANDLED_RESPONSE_SENT:
                        print(f"{INFO()} Request served !")
                except Exception as e:
                    errorhandler(e)

            # Feed the watchdog
            wdt.feed()
        # Catch the watchdog exceptions
        except WatchDogTimeout as e:
            if debugMode:
                print(f"{DEBUG()} {e}")
        # TODO: Define other runtime exceptions ?

# We're good to go, enter loop
print(f"{ACTION()} {GREEN}All systems go ! Entering main loop !{DEFAULT}")
#asyncio.run(main())
main()
