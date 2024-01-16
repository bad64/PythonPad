print("=== Initializing PythonPad ===")

import board
import digitalio
import json
import microcontroller
import usb_hid

from GamepadDriver import Gamepad, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, HAT_CENTER
gp = Gamepad(usb_hid.devices)

def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Defining physical states
HIGH = True
LOW = False

# Don't go all the way, the Switch doesn't really like that and will wrap around
MIN_TILT = 1
CENTER = 127
MAX_TILT = 254

# Defining bitmasks
MASK_Y =             0b0000000000000001
MASK_B =             0b0000000000000010
MASK_A =             0b0000000000000100
MASK_X =             0b0000000000001000
MASK_L =             0b0000000000010000
MASK_R =             0b0000000000100000
MASK_ZL =            0b0000000001000000
MASK_ZR =            0b0000000010000000
MASK_SELECT =        0b0000000100000000
MASK_START =         0b0000001000000000
MASK_L3 =            0b0000010000000000
MASK_R3 =            0b0000100000000000
MASK_HOME =          0b0001000000000000
MASK_CAPTURE =       0b0010000000000000
MASK_UNUSED1 =       0b0100000000000000
MASK_UNUSED2 =       0b1000000000000000

# WTAF is a button
class Button:
    def __init__(self, pin, mappedInput):
        self._pin = int(pin)
        self._mappedInput = mappedInput
        self._mask = None
        # Set up actual i/o layer
        self._io = eval("digitalio.DigitalInOut(board.GP{})".format(self._pin))
        self._io.switch_to_input()
        self._io.pull = digitalio.Pull.UP
        if self._mappedInput in [ "UP", "DOWN", "LEFT", "RIGHT", "C_UP", "C_DOWN", "C_LEFT", "C_RIGHT", "MOD_X", "MOD_Y" ]:
            self._mask = None
        else:
            self._mask = eval("MASK_{}".format(self._mappedInput))
    def getPinNumber(self):
        return self._pin
    def input(self):
        return self._mappedInput
    def io(self):
        return self._io
    def read(self):
        if self._io.value == False:
            return LOW
        else:
            return HIGH
    def mask(self):
        return self._mask

# Parse config from JSON file
cfgSmash = {}       # Default config, use to poll for alternate modes
cfgStandard = {}    # Regular FG config ## TODO
runningCfg = {}

with open("config_smash.json") as f:
    cfgSmash = json.load(f)

# Bind all inputs
AllButtons = { "leftAnalog": {}, "rightAnalog": {}, "modifiers": {}, "buttons": [] }

print("Loading inputs...")
for k,v in cfgSmash.items():
    if v != "None":
        if v in [ "UP", "DOWN", "LEFT", "RIGHT" ]:
            AllButtons["leftAnalog"][v] = Button(k, v)
        elif v in [ "C_UP", "C_DOWN", "C_LEFT", "C_RIGHT" ]:
            AllButtons["rightAnalog"][v] = Button(k, v)
        elif v in [ "MOD_X", "MOD_Y" ]:
            AllButtons["modifiers"][v] = Button(k, v)
        else:
            AllButtons["buttons"].append(Button(k, v))
        print(f"Bound key \"{v}\" to input on pin {k}")

# Run pre-checks
print("Running pre-checks...")
for b in AllButtons["buttons"]:
    ## Check if we want to reboot to bootloader
    if b.input() == "START" and b.read() == LOW:
        print("Rebooting !")
        microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
        microcontroller.reset()
    ## Check if we want the fighting game config
    if b.input() == "A" and b.read() == LOW:
        print("FGC mode go !")
        pass

# We're good to go, enter loop
print("PythonPad starts !")

while True:
    # Buttons
    gp.reset_buttons()

    for b in AllButtons["buttons"]:
        if b.read() == LOW:
            gp.press_button(b.mask())

    # Left stick
    x = CENTER
    y = CENTER
    z = CENTER
    rz = CENTER

    ## X axis
    if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
        x = MIN_TILT
    elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
        x = CENTER
    elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
        x = MAX_TILT
    ## Y axis
    if AllButtons["leftAnalog"]["UP"].read() == LOW and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
        y = MIN_TILT
    elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
        y = CENTER
    elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == LOW:
        y = MAX_TILT
    else:
        y = MIN_TILT

    ## Apply modifiers
    if AllButtons["modifiers"]["MOD_X"].read() == LOW and AllButtons["modifiers"]["MOD_Y"].read() == LOW: ## We d-pad now 
        if x == MIN_TILT:
            if y == MIN_TILT:
                gp.set_dpad(HAT_UP_LEFT)
            elif y == CENTER:
                gp.set_dpad(HAT_LEFT)
            elif y == MAX_TILT:
                gp.set_dpad(HAT_DOWN_LEFT)
        elif x == CENTER:
            if y == MIN_TILT:
                gp.set_dpad(HAT_UP)
            elif y == CENTER:
                gp.set_dpad(HAT_CENTER)
            elif y == MAX_TILT:
                gp.set_dpad(HAT_DOWN)
        if x == MAX_TILT:
            if y == MIN_TILT:
                gp.set_dpad(HAT_UP_RIGHT)
            elif y == CENTER:
                gp.set_dpad(HAT_RIGHT)
            elif y == MAX_TILT:
                gp.set_dpad(HAT_DOWN_RIGHT)
        gp.set_lsx(CENTER)
        gp.set_lsy(CENTER)
    else:
        gp.set_dpad(HAT_CENTER)
        if AllButtons["modifiers"]["MOD_X"].read() == LOW and AllButtons["modifiers"]["MOD_Y"].read() == HIGH:
            if x == MIN_TILT:
                x = int(127 - (126 * 2/3))
            elif x == MAX_TILT:
                x = int(127 + (126 * 2/3))
            else:
                pass

            if y == MIN_TILT:
                y = int(127 - (126 * 2/3))
            elif y == MAX_TILT:
                y = int(127 + (126 * 2/3))
            else:
                pass
        elif AllButtons["modifiers"]["MOD_X"].read() == HIGH and AllButtons["modifiers"]["MOD_Y"].read() == LOW:
            if x == MIN_TILT:
                x = int(127 - (126 * 1/3))
            elif x == MAX_TILT:
                x = int(127 + (126 * 1/3))
            else:
                pass

            if y == MIN_TILT:
                y = int(127 - (126 * 1/3))
            elif y == MAX_TILT:
                y = int(127 + (126 * 1/3))
            else:
                pass
        gp.set_lsx(x)
        gp.set_lsy(y)

    # Right stick
    ## X axis
    if AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH:
        z = MIN_TILT
    elif AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH:
        z = CENTER
    elif AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW:
        z = MAX_TILT
    else:
        z = MIN_TILT
    ## Y axis
    if AllButtons["rightAnalog"]["C_UP"].read() == LOW and AllButtons["rightAnalog"]["C_DOWN"].read() == HIGH:
        rz = MIN_TILT
    elif AllButtons["rightAnalog"]["C_UP"].read() == HIGH and AllButtons["rightAnalog"]["C_DOWN"].read() == HIGH:
        rz = CENTER
    elif AllButtons["rightAnalog"]["C_UP"].read() == HIGH and AllButtons["rightAnalog"]["C_DOWN"].read() == LOW:
        rz = MAX_TILT

    gp.set_rsx(z)
    gp.set_rsy(rz)
    #gp.set_rsx(range_map(z, -120, 120, 7, 249))
    #gp.set_rsy(range_map(rz, -120, 120, 7, 249))


    gp.send()
