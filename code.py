print("=== Initializing PythonPad ===")

import board
import digitalio
import json
import microcontroller
import usb_hid

from GamepadDriver import Gamepad, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, HAT_CENTER, RED, DEFAULT
gp = Gamepad(usb_hid.devices)

# Defining physical states
HIGH = True
LOW = False

# Don't go all the way, the Switch doesn't really like that and will wrap around
MIN_TILT = 1
CENTER = 127
MAX_TILT = 254

# Defining bitmasks
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

MASK_VS_1P =        MASK_X
MASK_VS_2P =        MASK_Y
MASK_VS_3P =        MASK_R
MASK_VS_4P =        MASK_ZL
MASK_VS_1K =        MASK_A
MASK_VS_2K =        MASK_B
MASK_VS_3K =        MASK_L
MASK_VS_4K =        MASK_ZR

# WTAF is a button
class Button:
    def __init__(self, pin, mappedInput):
        self._pins = [ int(pin) ]
        try:
            self._mask = eval("MASK_{}".format(mappedInput))
        except:
            self._mask = None
        self._io = [ eval("digitalio.DigitalInOut(board.GP{})".format(int(pin))) ]
        self._io[0].switch_to_input()
        self._io[0].pull = digitalio.Pull.UP
    def addPin(self, pin):
        self._pins.append(pin)
        self._io.append(eval("digitalio.DigitalInOut(board.GP{})".format(int(pin))))
        self._io[-1].switch_to_input()
        self._io[-1].pull = digitalio.Pull.UP
    def read(self):
        for io in self._io:
            if io.value == False:
                return LOW
        return HIGH
    def mask(self):
        return self._mask

# Parse config from JSON file
cfg = {}

with open("config.json") as f:
    cfg = json.load(f)

# Run pre-checks (mode select etc)
print("Running pre-checks...")
mode = "smash"
for k,v in cfg["modes"].items():
    b = Button(k, None)
    if b.read() == LOW:
        if v == "bootloader":
            print("We gotta reboot !")
            microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
            microcontroller.reset()
        else:
            mode = v
    b._io[0].deinit()  # Free the io pin for rebinding later

# Bind all inputs
AllButtons = { "leftAnalog": {}, "rightAnalog": {}, "modifiers": {}, "buttons": [] }

print(f"Loading config: \"{mode}\"")

## Save cycles (lmao as if that was needed) by precalculating tilt values
xAxisModXDelta = CENTER - round(CENTER * (2/3))
xAxisModYDelta = CENTER - round(CENTER * (1/3))
yAxisModXDelta = CENTER - round(CENTER * (2/3))
yAxisModYDelta = CENTER - round(CENTER * (1/3))

modifiedXAxis = False
modifiedYAxis = False

for k,v in cfg[mode].items():
    if k == "X_AXIS_MOD_X_DELTA":
        modifiedXAxis = True
        try:
            xAxisModXDelta = round(int(eval(v)))
            print(f"Set X axis MOD_X delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{RED}Cannot set X axis MOD_X delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{RED}Cannot set X axis MOD_X delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "X_AXIS_MOD_Y_DELTA":
        modifiedXAxis = True
        try:
            xAxisModYDelta = round(int(eval(v)))
            print(f"Set X axis MOD_Y delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{RED}Cannot set X axis MOD_Y delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{RED}Cannot set X axis MOD_Y delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "Y_AXIS_MOD_X_DELTA":
        modifiedYAxis = True
        try:
            yAxisModXDelta = round(int(eval(v)))
            print(f"Set Y axis MOD_X delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{RED}Cannot set Y axis MOD_X delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{RED}Cannot set Y axis MOD_X delta value to \"{v}\": {e}{DEFAULT}")
    elif k == "Y_AXIS_MOD_Y_DELTA":
        modifiedYAxis = True
        try:
            yAxisModYDelta = round(int(eval(v)))
            print(f"Set Y axis MOD_Y delta to {round(eval(v))}")
        except Exception as e:
            if 'message' in dir(e):
                print(f"{RED}Cannot set Y axis MOD_Y delta value to \"{v}\": {e.message}{DEFAULT}")
            else:
                print(f"{RED}Cannot set Y axis MOD_Y delta value to \"{v}\": {e}{DEFAULT}")

if modifiedXAxis:
    print("New X axis values:")
    print(f"    LEFT:           {MIN_TILT}")
    print(f"    LEFT MOD_X:     {round(CENTER - xAxisModXDelta)}")
    print(f"    LEFT MOD_Y:     {round(CENTER - xAxisModYDelta)}")
    print(f"    CENTER:         {CENTER}")
    print(f"    RIGHT MOD_Y:    {round(CENTER + xAxisModYDelta)}")
    print(f"    RIGHT MOD_X:    {round(CENTER + xAxisModXDelta)}")
    print(f"    RIGHT:          {MAX_TILT}")

if modifiedYAxis:
    print("New Y axis values:")
    print(f"    UP:             {MIN_TILT}")
    print(f"    UP MOD_X:       {round(CENTER - yAxisModXDelta)}")
    print(f"    UP MOD_Y:       {round(CENTER - yAxisModYDelta)}")
    print(f"    CENTER:         {CENTER}")
    print(f"    DOWN MOD_Y:     {round(CENTER + yAxisModYDelta)}")
    print(f"    DOWN MOD_X:     {round(CENTER + yAxisModXDelta)}")
    print(f"    DOWN:           {MAX_TILT}")

for k,v in cfg[mode].items():
    try:
        int(k)  # If the key isn't an int it's a modifier value
        if v != "None":
            if v in [ "UP", "DOWN", "LEFT", "RIGHT" ]:
                try:
                    AllButtons["leftAnalog"][v].addPin(k)
                except KeyError:
                    AllButtons["leftAnalog"][v] = Button(k, v)
            elif v in [ "C_UP", "C_DOWN", "C_LEFT", "C_RIGHT" ]:
                try:
                    AllButtons["rightAnalog"][v].addPin(k)
                except KeyError:
                    AllButtons["rightAnalog"][v] = Button(k, v)
            elif v in [ "MOD_X", "MOD_Y" ]:
                try:
                    AllButtons["modifiers"][v].addPin(k)
                except KeyError:
                    AllButtons["modifiers"][v] = Button(k, v) 
            else:
                AllButtons["buttons"].append(Button(k, v))
            print(f"Bound key \"{v}\" to input on pin {k}")
    except:
        pass

# We're good to go, enter loop
print("PythonPad starts !")

while True:
    # Buttons
    ## This is shared between all modes
    gp.reset_buttons()

    for b in AllButtons["buttons"]:
        if b.read() == LOW:
            gp.press_button(b.mask())

    x = CENTER
    y = CENTER
    z = CENTER
    rz = CENTER

    if mode == "smash":
        # Left stick
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
                    x = CENTER - xAxisModXDelta
                elif x == MAX_TILT:
                    x = CENTER + xAxisModXDelta
                else:
                    pass

                if y == MIN_TILT:
                    y = CENTER - yAxisModXDelta
                elif y == MAX_TILT:
                    y = CENTER + yAxisModXDelta
                else:
                    pass
            elif AllButtons["modifiers"]["MOD_X"].read() == HIGH and AllButtons["modifiers"]["MOD_Y"].read() == LOW:
                if x == MIN_TILT:
                    x = CENTER - xAxisModYDelta
                elif x == MAX_TILT:
                    x = CENTER + xAxisModYDelta
                else:
                    pass

                if y == MIN_TILT:
                    y = CENTER - yAxisModYDelta
                elif y == MAX_TILT:
                    y = CENTER + yAxisModYDelta
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

    elif mode == "versus":
        gp.set_lsx(x)
        gp.set_lsy(y)
        gp.set_rsx(z)
        gp.set_rsy(rz)

        # Left stick(/Dpad)
        if AllButtons["leftAnalog"]["UP"].read() == LOW:
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_UP_LEFT)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_UP)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_UP_RIGHT)
        elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_LEFT)
            elif (AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH) or (AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW):
                gp.set_dpad(HAT_CENTER)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_RIGHT)
        elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == LOW:
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_DOWN_LEFT)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_DOWN)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_DOWN_RIGHT)

    gp.send()
