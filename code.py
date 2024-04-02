print("=== Initializing PythonPad ===")
# Display version for debugging purposes
try:
    with open("VERSION") as f:
        versionString = f.read()
        print(f"[\033[34mINFO\033[39m] Version {versionString}")
except:
    print("[\033[34mINFO\033[39m] VERSION file not found; skipping check")

import board
import digitalio
import json
import microcontroller
import time
import traceback
import usb_hid

from gamepad_driver import Gamepad, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, HAT_CENTER, RED, YELLOW, GREEN, CYAN, BLUE, VIOLET, DEFAULT
gp = Gamepad(usb_hid.devices)

# Shortcut functions for things printed everywhere
def INFO():
    return f"[{BLUE}INFO{DEFAULT}]"

def WARN():
    return f"[{YELLOW}WARNING{DEFAULT}]"

def ACTION():
    return f"[{CYAN}ACTION{DEFAULT}]"

def ERROR():
    return f"[{RED}ERROR{DEFAULT}]"

def DEBUG():
    return f"[{VIOLET}DEBUG{DEFAULT}]"

# Defining physical states
HIGH = True
LOW = False

# Don't go all the way, the Switch doesn't really like that and will wrap around once in a blue moon
MIN_TILT = 1
CENTER = 127
MAX_TILT = 254

# Defining bitmasks
## Note: I strongly recommend not touching either of these sections, if you need to change what a given button does, go through config.json instead

## For Smash (or general Switch usage)
MASK_Y =            0b0000000000000001
MASK_B =            0b0000000000000010
MASK_A =            0b0000000000000100
MASK_X =            0b0000000000001000
MASK_L =            0b0000000000010000
MASK_R =            0b0000000000100000
MASK_ZL =           0b0000000001000000
MASK_ZR =           0b0000000010000000
MASK_SELECT =       0b0000000100000000
MASK_START =        0b0000001000000000
MASK_L3 =           0b0000010000000000
MASK_R3 =           0b0000100000000000
MASK_HOME =         0b0001000000000000
MASK_CAPTURE =      0b0010000000000000
MASK_UNUSED1 =      0b0100000000000000
MASK_UNUSED2 =      0b1000000000000000

## For regular fighting games
MASK_VS_1P =        MASK_Y
MASK_VS_2P =        MASK_X
MASK_VS_3P =        MASK_R
MASK_VS_4P =        MASK_ZL
MASK_VS_1K =        MASK_B
MASK_VS_2K =        MASK_A
MASK_VS_3K =        MASK_L
MASK_VS_4K =        MASK_ZR

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
        # Declares a Button, with its associated pin and the input it triggers on the host
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
                print(f"{GREEN}\t> Debug mode ON{DEFAULT}")
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
            print(f"{CYAN}\t> {motd[r]}{DEFAULT}")
            time.sleep(1)
except KeyError:
    pass

# Mode selection
print(f"{ACTION()} Running pre-checks...")
mode = "smash"              ## We default to Smash mode in case of invalid or missing option
try:
    ## Attempt to read the default mode from config
    mode = cfg["general"]["defaultMode"]
    if mode in cfg["modes"].values() and mode != "bootloader":
        pass    ## No need to print, this is fine to silence since we print the boot
                ## mode further down the line
    else:
        print(f"{WARN()} {YELLOW}Invalid mode: {mode}; defaulting to \"{GREEN}smash{YELLOW}\"{DEFAULT}")
        mode = "smash"
except:
    pass

gp.set_socd_type("LRN")     ## Again, default value for safety
try:
    gp.set_socd_type(cfg["general"]["socdType"])

    if gp.get_socd_type() in [ "LRN", "last", "LIW", "lastInputWins" ]:
        print(f"{INFO()} Set SOCD cleaner to \"{GREEN}{gp.get_socd_type()}{DEFAULT}\"")
    else:
        print(f"{WARN()} {YELLOW}Invalid SOCD cleaner setting \"{gp.get_socd_type()}\"; defaulting to \"LRN\"{DEFAULT}")
        gp.set_socd_type("LRN")
except:
    print(f"{WARN()} {YELLOW}SOCD cleaner type absent; defaulting to \"{GREEN}LRN{YELLOW}\"{DEFAULT}")
    gp.set_socd_type("LRN")

has_server = False
try:
    import localserver
    has_server = localserver.check_import()
    print(f"{INFO()} Server code detected !")
except ImportError:
    # Mask the error, it's harmless
    print(f"{WARN()} Server config not found; skipping webserver")
except Exception as e:
    # Don't mask the error, it might not be harmless at all
    print(f"{ERROR()}{RED}", end="")
    if "message" in dir(e):
        print(e.message, end="")
    else:
        print(e, end="")
    print(f"{DEFAULT}")

## Iterate over keys defined in the "modes" section
try:
    for k,v in cfg["modes"].items():
        b = Button(k, None)
        if b.read() == LOW:
            if v == "bootloader":
                print(f"{INFO()} We gotta reboot !")
                time.sleep(2)
                microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
                microcontroller.reset()
            else:
                mode = v
        b._io[0].deinit()  # Free the io pin for rebinding later
except Exception as e:
    if "message" in dir(e):
        print(f"{ERROR()}{RED}{e.message}{DEFAULT}")
    else:
        print(f"{ERROR()}{RED}{e}{DEFAULT}")

# Input binding
AllButtons = { "leftAnalog": {}, "rightAnalog": {}, "modifiers": {}, "buttons": [] }

print(f"{ACTION()} Loading config: \"{mode}\"")

## Deal with the modifiers first
### Save cycles by precalculating tilt values
xAxisModXDelta = CENTER - round(CENTER * (2/3))
xAxisModYDelta = CENTER - round(CENTER * (1/3))
yAxisModXDelta = CENTER - round(CENTER * (2/3))
yAxisModYDelta = CENTER - round(CENTER * (1/3))
zAxisModXDelta = CENTER - round(CENTER * (1/2))
zAxisModYDelta = CENTER - round(CENTER * (1/2))
rzAxisModXDelta = CENTER - round(CENTER * (1/2))
rzAxisModYDelta = CENTER - round(CENTER * (1/2))

modifiedXAxis = False
modifiedYAxis = False
modifiedZAxis = False
modifiedRZAxis = False

for k,v in cfg[mode].items():
    if k == "X_AXIS_MOD_X_DELTA":
        modifiedXAxis = True
        try:
            xAxisModXDelta = round(int(eval(v)))
            print(f"{INFO()} Set X axis MOD_X delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set X axis MOD_X delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set X axis MOD_X delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "X_AXIS_MOD_Y_DELTA":
        modifiedXAxis = True
        try:
            xAxisModYDelta = round(int(eval(v)))
            print(f"{INFO()} Set X axis MOD_Y delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set X axis MOD_Y delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set X axis MOD_Y delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "Y_AXIS_MOD_X_DELTA":
        modifiedYAxis = True
        try:
            yAxisModXDelta = round(int(eval(v)))
            print(f"{INFO()} Set Y axis MOD_X delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_X delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_X delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "Y_AXIS_MOD_Y_DELTA":
        modifiedYAxis = True
        try:
            yAxisModYDelta = round(int(eval(v)))
            print(f"{INFO()} Set Y axis MOD_Y delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_Y delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{ERROR()} {RED}Cannot set Y axis MOD_Y delta value to \"{v}\": {e}{DEFAULT}")

## Printing axis values over UART just to be sure nothing is on fire
if debugMode:
    if modifiedXAxis:
        print(f"{DEBUG()} New X axis values:")
        print(f"{DEBUG()}    LEFT:           {MIN_TILT}")
        print(f"{DEBUG()}    LEFT MOD_X:     {round(CENTER - xAxisModXDelta)}")
        print(f"{DEBUG()}    LEFT MOD_Y:     {round(CENTER - xAxisModYDelta)}")
        print(f"{DEBUG()}    CENTER:         {CENTER}")
        print(f"{DEBUG()}    RIGHT MOD_Y:    {round(CENTER + xAxisModYDelta)}")
        print(f"{DEBUG()}    RIGHT MOD_X:    {round(CENTER + xAxisModXDelta)}")
        print(f"{DEBUG()}    RIGHT:          {MAX_TILT}")

    if modifiedYAxis:
        print(f"{DEBUG() }New Y axis values:")
        print(f"{DEBUG()}    UP:             {MIN_TILT}")
        print(f"{DEBUG()}    UP MOD_X:       {round(CENTER - yAxisModXDelta)}")
        print(f"{DEBUG()}    UP MOD_Y:       {round(CENTER - yAxisModYDelta)}")
        print(f"{DEBUG()}    CENTER:         {CENTER}")
        print(f"{DEBUG()}    DOWN MOD_Y:     {round(CENTER + yAxisModYDelta)}")
        print(f"{DEBUG()}    DOWN MOD_X:     {round(CENTER + yAxisModXDelta)}")
        print(f"{DEBUG()}    DOWN:           {MAX_TILT}")

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
            print(f"{WARN()} {YELLOW}Attempted to bind key \"{v}\" to pin {k} but failed{DEFAULT}")
            print(f"{WARN()} {YELLOW}[{type(e)}]: {e}{DEFAULT}")

# Import functions from the appropriate file
try:
    print(f"{ACTION()} Importing main loop functions from {mode}.py... ", end="")
    exec(f"from {mode} import check_import, directionals")
    if check_import() == True:
        print(f"[{GREEN}OK{DEFAULT}]")
    else:
        raise ImportError
except Exception as e:
    print(f"[{RED}KO{DEFAULT}]")
    raise e

# If we have a server set up, start it now
if has_server:
    try:
        localserver.localserver.start(str(localserver.wifi.radio.ipv4_address_ap))
        print(f"{INFO()} Local server started with SSID \"{GREEN}{localserver.ap_ssid}{DEFAULT}\" on {GREEN}{str(localserver.wifi.radio.ipv4_address_ap)}{DEFAULT}")
    except Exception as e:
        print(f"{ERROR()} {RED}Local server failed to start !!{DEFAULT}")
        print(f"{ERROR()}{RED} ", end="")
        if "message" in dir(e):
            print(e.message, end="")
        else:
            print(e, end="")
        print(f"{DEFAULT}")

# We're good to go, enter loop
print("=== PythonPad starts ! ===")

while True:
    # Buttons
    ## This is shared between all modes, don't touch it
    gp.reset_buttons()

    for b in AllButtons["buttons"]:
        if b.read() == LOW:
            gp.press_button(b.mask())

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
            print(f"{ERROR()} {RED}{type(e)}: ", end="")
            if "message" in dir(e):
                print(e.message)
            else:
                print(e)
            print(f"{DEFAULT}")
