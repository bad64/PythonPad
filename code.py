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
import countio
import digitalio
import json
import microcontroller
import time
import traceback
import usb_hid
from math import floor, ceil

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

# Import bitmasks
from bitmasks import *

# Defining a pin prefix
prefix = "GP"                                       # RP2040, default
if "adafruit_feather_esp32s3" in board.board_id:    # Feather ESP32-S3
    prefix = "D"
elif "espressif_esp32s3" in board.board_id:         # Espressif ESP32-S3/One Board
    prefix = "IO"

# Define a mapping interface
class Button:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.mask = eval(f"MASK_{name.upper()}")
        self._io = eval("digitalio.DigitalInOut(board.{}{})".format(prefix, int(pin)))
        self._io.switch_to_input()
        self._io.pull = digitalio.Pull.UP
        print(f"{INFO()} Bound pin {GREEN}{self.pin}{DEFAULT} to {CYAN}{self.name}{DEFAULT}")
    def read(self):
        if self._io.value == False:
            return LOW
        return HIGH
    def get_io(self):
        return(self._io)

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

    if mode in cfg["modes"].keys() and mode != "bootloader":
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
        b = eval("digitalio.DigitalInOut(board.{}{})".format(prefix, int(v)))
        b.switch_to_input()
        b.pull = digitalio.Pull.UP
        if b.value == LOW:
            if v == "bootloader":
                print(f"{OK()}")
                print(f"{INFO()} We gotta reboot !")
                time.sleep(2)
                microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
                microcontroller.reset()
            else:
                mode = k
        b.deinit()  # Free the io pin for rebinding later
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
        print("\"{}{}{}\" {}".format(GREEN, cfg[mode]["EXTRAS"]["canonName"], DEFAULT, OK()))
    except KeyError:
        print("\"{}{}{}\" {}".format(GREEN, mode, DEFAULT, OK()))
        if debugMode:
            print(f"{DEBUG()} No \"{RED}canonName{DEFAULT}\" property for mode \"{GREEN}{mode}{DEFAULT}\"")

# SOCD selection
print(f"{ACTION()} Setting up SOCD cleaning... ", end="")
gp.set_socd_type("LRN")     ## Again, default value for safety
try:
    gp.set_socd_type(cfg[mode]["EXTRAS"]["socdType"])

    if gp.get_socd_type() in [ "LRN", "LIW", "CPT" ]:
        print(f"{OK()}")
        print(f"{INFO()} Set SOCD cleaner to \"{GREEN}{gp.get_socd_type()}{DEFAULT}\"")
    else:
        raise cre.WrongSOCDCleaningTypeException(gp.get_socd_type())
except KeyError:
    print(f"{CONFUSED()}")
    print(f"{WARN()} SOCD cleaner type absent; defaulting to \"{GREEN}LRN{DEFAULT}\"")
    gp.set_socd_type("LRN")
except cre.WrongSOCDCleaningTypeException as e:
    print(f"{KO()}")
    print(f"{WARN()} \"{RED}{e.mode}{DEFAULT}\" does not name an SOCD cleaning type; defaulting to \"{GREEN}LRN{DEFAULT}\"")
    gp.set_socd_type("LRN")

# Input binding
print(f"{ACTION()} Loading config: \"{GREEN}{mode}{DEFAULT}\"")

binding_errors = 0
for k,v in cfg[mode].items():
    if k == "EXTRAS":
        for sub_k, sub_v in cfg[mode]["EXTRAS"].items():
            if sub_k in [ "MOD_X", "MOD_Y" ]:
                try:
                    exec(f"MAP_{sub_k} = Button(sub_v, sub_k)")
                except Exception as e:
                    print(f"{ERROR()} Attempted to map pin \"{CYAN}{v}{DEFAULT}\" to input \"{GREEN}{k}{DEFAULT}\" but failed !!")
                    if "message" in dir(e):
                        print(f"{ERROR()} {e.message}")
                    else:
                        print(f"{ERROR()} {e}")
                    binding_errors += 1
    else:
        try:
            exec(f"MAP_{k} = Button(v, k)")
        except Exception as e:
            print(f"{ERROR()} Attempted to map pin \"{CYAN}{v}{DEFAULT}\" to input \"{GREEN}{k}{DEFAULT}\" but failed !!")
            if "message" in dir(e):
                print(f"{ERROR()} {e.message}")
            else:
                print(f"{ERROR()} {e}")
            binding_errors += 1

if binding_errors != 0:
    print(f"{ERROR()} Critical binding errors have been detected, halting")
    while True:
        print("\r", end="")

# Pre-compute tilt values
def tilt_check(reference, value, axis, modifier, orientation):
    retval = reference
    try:
        if reference == value:
            print("{} Set {} axis MOD {} {} to {}{}{}".format(INFO(), axis, modifier, orientation, GREEN, reference, DEFAULT))
            return reference
        else:
            print("{} Set {} axis MOD {} {} to {}{}{} [{}OVERRIDE{}]".format(INFO(), axis, modifier, orientation, GREEN, value, DEFAULT, YELLOW, DEFAULT))
            return value
    except ValueError as e:
        print("{} Invalid value for property {}\"{}_AXIS_MOD_{}_DELTA\"{}: {}".format(ERROR(), RED, axis, modifier, DEFAULT, value))
        print("{} Defaulting X axis MOD X negative value to {}{}{}".format(INFO(), GREEN, reference, DEFAULT))
    except KeyError as e:
        # Do nothing, fail silently, and use defaults
        pass
    except Exception as e:
        if "message" in dir(e):
            print(f"{ERROR()} {e.message}")
        else:
            print(f"{ERROR()} {e}")
    return reference

tilt_values = {}
if mode == "smash":
    print(f"{ACTION()} Pre-computing tilt values")

    ## Default values
    tilt_values["X_NEGATIVE"] = MIN_TILT
    tilt_values["X_MOD_X_NEGATIVE"] = ceil(CENTER - (CENTER * (2/3)))
    tilt_values["X_MOD_Y_NEGATIVE"] = ceil(CENTER - (CENTER * (1/3)))
    tilt_values["X_CENTER"] = CENTER
    tilt_values["X_MOD_X_POSITIVE"] = floor(CENTER + (CENTER * (2/3)))
    tilt_values["X_MOD_Y_POSITIVE"] = floor(CENTER + (CENTER * (1/3)))
    tilt_values["X_POSITIVE"] = MAX_TILT

    tilt_values["Y_NEGATIVE"] = MIN_TILT
    tilt_values["Y_MOD_X_NEGATIVE"] = ceil(CENTER - (CENTER * (2/3)))
    tilt_values["Y_MOD_Y_NEGATIVE"] = ceil(CENTER - (CENTER * (1/3)))
    tilt_values["Y_CENTER"] = CENTER
    tilt_values["Y_MOD_X_POSITIVE"] = floor(CENTER + (CENTER * (2/3)))
    tilt_values["Y_MOD_Y_POSITIVE"] = floor(CENTER + (CENTER * (1/3)))
    tilt_values["Y_POSITIVE"] = MAX_TILT

    # TODO: Refactor this
    ## X axis computation
    buf_x = cfg["smash"]["EXTRAS"]["X_AXIS_MOD_X_DELTA"]
    buf_y = cfg["smash"]["EXTRAS"]["X_AXIS_MOD_Y_DELTA"]
    ### X axis -, X mod
    tilt_values["X_MOD_X_NEGATIVE"] = tilt_check(tilt_values["X_MOD_X_NEGATIVE"], eval(f"ceil(CENTER - ({buf_x}))"), "X", "X", "negative")
    ### X axis -, Y mod
    tilt_values["X_MOD_Y_NEGATIVE"] = tilt_check(tilt_values["X_MOD_Y_NEGATIVE"], eval(f"ceil(CENTER - ({buf_y}))"), "X", "Y", "negative")
    ### X axis +, Y mod
    tilt_values["X_MOD_Y_POSITIVE"] = tilt_check(tilt_values["X_MOD_Y_POSITIVE"], eval(f"floor(CENTER + ({buf_y}))"), "X", "Y", "positive")
    ### X axis +, X mod
    tilt_values["X_MOD_X_POSITIVE"] = tilt_check(tilt_values["X_MOD_X_POSITIVE"], eval(f"floor(CENTER + ({buf_x}))"), "X", "X", "positive")

    ## Y axis computation
    buf_x = cfg["smash"]["EXTRAS"]["Y_AXIS_MOD_X_DELTA"]
    buf_y = cfg["smash"]["EXTRAS"]["Y_AXIS_MOD_Y_DELTA"]
    ### Y axis -, X mod
    tilt_values["Y_MOD_X_NEGATIVE"] = tilt_check(tilt_values["Y_MOD_X_NEGATIVE"], eval(f"ceil(CENTER - ({buf_x}))"), "Y", "X", "negative")
    ### Y axis -, Y mod
    tilt_values["Y_MOD_Y_NEGATIVE"] = tilt_check(tilt_values["Y_MOD_Y_NEGATIVE"], eval(f"ceil(CENTER - ({buf_y}))"), "Y", "Y", "negative")
    ### Y axis +, Y mod
    tilt_values["Y_MOD_Y_POSITIVE"] = tilt_check(tilt_values["Y_MOD_Y_POSITIVE"], eval(f"floor(CENTER + ({buf_y}))"), "Y", "Y", "positive")
    ### Y axis +, X mod
    tilt_values["Y_MOD_X_POSITIVE"] = tilt_check(tilt_values["Y_MOD_X_POSITIVE"], eval(f"floor(CENTER + ({buf_x}))"), "Y", "X", "positive")

    #for k,v in tilt_values.items():
    #    tilt_values[k] = int(v)

# Import functions from the appropriate file
try:
    try:
        runtime_file = cfg[mode]["file"]
    except KeyError:
        runtime_file = mode
    print(f"{ACTION()} Importing main loop functions from {runtime_file}.py... ", end="")
    exec(f"from {runtime_file} import check_import, do_leftstick, do_rightstick, do_buttons")
    if check_import() == True:
        print(f"[{GREEN}OK{DEFAULT}]")
    else:
        raise ImportError
except Exception as e:
    raise e
    print(f"[{RED}KO{DEFAULT}]")
    errorhandler(e, panic=True)

async def main():
    while True:
        try:
            # Reset everything
            gp.reset_buttons()
            x = CENTER
            y = CENTER
            z = CENTER
            rz = CENTER

            # Handle main buttons through proxy functions into a buffer
            if mode == "smash":
                do_buttons([ MAP_A, MAP_B, MAP_X, MAP_Y, MAP_L, MAP_L3, MAP_ZR, MAP_R, MAP_R3, MAP_START, MAP_SELECT, MAP_HOME ], gp)
            elif mode == "versus":
                do_buttons([ MAP_CIRCLE, MAP_CROSS, MAP_TRIANGLE, MAP_SQUARE, MAP_L1, MAP_L2, MAP_L3, MAP_R1, MAP_R2, MAP_R3, MAP_START, MAP_SELECT, MAP_HOME ], gp)

            # Handle left stick with modifiers
            if mode == "smash":
                do_leftstick(gp.get_socd_type(), [ MAP_UP, MAP_DOWN, MAP_LEFT, MAP_RIGHT ], [ MAP_MOD_X, MAP_MOD_Y ], tilt_values, gp)
            elif mode == "versus":
                do_leftstick(gp.get_socd_type(), [ MAP_UP, MAP_DOWN, MAP_LEFT, MAP_RIGHT ], gp)

            # Handle right stick
            if mode == "smash":
                do_rightstick([ MAP_C_UP, MAP_C_DOWN, MAP_C_LEFT, MAP_C_RIGHT ], MIN_TILT, CENTER, MAX_TILT, gp)
            elif mode == "versus":
                pass # Don't need RS in versus mode

            # Finally send the report, yay !
            gp.send()

            wdt.feed()
        # Catch the watchdog exceptions
        except WatchDogTimeout as e:
            if debugMode:
                print(f"{DEBUG()} {e}")

# We're good to go, enter loop
print(f"{ACTION()} {GREEN}All systems go ! Entering main loop !{DEFAULT}")
asyncio.run(main())
