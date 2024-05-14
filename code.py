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

# Define a mapping interface
class Mapping:
    def __init__(self, pin, name):
        self.pin_number = pin
        self.pin = eval(f"board.{prefix}{pin}")
        self.name = name
        self.locked = False
        self.class_name = "MAP_".join(name.upper())
        self.mask = eval(f"MASK_{name.upper()}")
        print(f"{INFO()} Bound pin {GREEN}{self.pin_number}{DEFAULT} to {CYAN}{self.name}{DEFAULT}")
    async def scan(self, buffer):
        with countio.Counter(self.pin, edge=countio.Edge.FALL, pull=digitalio.Pull.UP) as interrupt:
            while True:
                if interrupt.count > 0:
                    if not self.locked:
                        interrupt.reset()
                        buffer &= self.mask
                        self.lock()
                        if debugMode:
                            print(f"{DEBUG()} Pressed {self.name}")
                else:
                    interrupt.reset()
                    buffer ^= self.mask
                    self.unlock()
                await asyncio.sleep_ms(0)
    def lock(self):
        self.locked = True
    def unlock(self):
        self.locked = False
    def register(self, taskbuffer, inputbuffer):
        taskbuffer.append(asyncio.create_task(self.scan(inputbuffer)))
        if debugMode:
            print(f"{DEBUG()} Registered async scan function for {self.name}")

class SpecialButton:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.class_name = "MAP_".join(name.upper())
        self._io = eval("digitalio.DigitalInOut(board.{}{})".format(prefix, int(pin)))
        print(f"{INFO()} Bound pin {GREEN}{self.pin}{DEFAULT} to {CYAN}{self.name}{DEFAULT}")
    def is_pressed(self):
        if self._io.value == False:
            return LOW
        return HIGH

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
        if b.value == LOW:
            if v == "bootloader":
                print(f"{OK()}")
                print(f"{INFO()} We gotta reboot !")
                time.sleep(2)
                microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
                microcontroller.reset()
            else:
                mode = v
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
print(f"{ACTION()} Loading config: \"{GREEN}{mode}{DEFAULT}\"")

buttons = 0
leftanalog = 0

for k,v in cfg[mode].items():
    if k == "EXTRAS":
        pass
    else:
        if "MOD_" in k:
            exec(f"MAP_{k} = SpecialButton(v, k)")
        else:
            exec(f"MAP_{k} = Mapping(v, k)")

# Import functions from the appropriate file
try:
    try:
        runtime_file = cfg[mode]["file"]
    except KeyError:
        runtime_file = mode
    print(f"{ACTION()} Importing main loop functions from {runtime_file}.py... ", end="")
    exec(f"from {runtime_file} import check_import, register_buttons, register_leftanalog, register_rightanalog, process_buttons, process_leftanalog, process_rightanalog")
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

async def main():
    # Register all the buttons
    buttons_task = []
    register_buttons(buttons_task, buttons)

    while True:
        try:
            # Handle action buttons
            for task in buttons_task:
                await asyncio.gather(task)

            gp.set_buttons(buttons)

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
asyncio.run(main())
