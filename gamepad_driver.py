# Based on https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/examples/hid_gamepad.py

import struct
import time

from adafruit_hid import find_device

from uart import RED, YELLOW, GREEN, CYAN, BLUE, VIOLET, DEFAULT, INFO, ACTION, ERROR, OK, KO

# Report structure
REPORT_SIZE = 8

# Offsets
OFFSET_BUTTONS = 16
OFFSET_HAT = OFFSET_BUTTONS + 8
OFFSET_JOY_X = OFFSET_HAT + 8
OFFSET_JOY_Y = OFFSET_JOY_X + 8
OFFSET_JOY_Z = OFFSET_JOY_Y + 8
OFFSET_JOY_RZ = OFFSET_JOY_Z + 8

# Hat defs
HAT_CENTER = 255
HAT_UP = 0
HAT_UP_RIGHT = 1
HAT_RIGHT = 2
HAT_DOWN_RIGHT = 3
HAT_DOWN = 4
HAT_DOWN_LEFT = 5
HAT_LEFT = 6
HAT_UP_LEFT = 7

# General functions
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def fits_in_1b(value):
    a = bytearray(1)
    try:
        struct.pack_into("<B", a, 0, value)
        return "Fits in 1 byte"
    except:
        return "Doesn't fit in 1 byte ??"

def fits_in_2b(value):
    a = bytearray(2)
    try:
        struct.pack_into("<H", a, 0, value)
        return "Fits in 2 bytes"
    except:
        return "Doesn't fit in 2 bytes ??"

class Gamepad:
    def __init__(self, devices, xinput=False):
        print(f"{ACTION()} Creating Gamepad device ", end="")
        self._xinput = xinput
        try:
            self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)
            print(f"{OK()}")
        except Exception as e:
            print(f"{KO()}")
            if "message" in dir(e):
                print(f"{ERROR()}{e.message}")
            else:
                print(f"{ERROR()}{e}")
            while True:
                print("\r", end="")

        # Set SOCD info
        self._socd = "LRN"
        self._socd_lock = False

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._hat = 255
        self._joy_x = 127
        self._joy_y = 127
        self._joy_z = 127
        self._joy_rz = 127

        if not xinput:
            # report[0] buttons 1-8
            # report[1] buttons 9-16
            # report[2] hat switch
            # report[3] joystick 0 x
            # report[4] joystick 0 y
            # report[5] joystick 1 x
            # report[6] joystick 1 y
            print(f"{ACTION()} Initializing report struct ", end="")
            try:
                self._report = bytearray(8)
                print(f"{OK()}")
            except Exception as e:
                print(f"{KO()}")

            # Remember the last report as well, so we can avoid sending
            # duplicate reports.
            self._last_report = bytearray(8)

        elif xinput:
            # report[0] Y X B A View Menu Ignore Ignore
            # report[1] Ignore Ignore Next Prev Right Left Down Up
            # report[2-12] Reserved
            print(f"{ACTION()} Initializing report struct ", end="")
            try:
                self._report = bytearray(12)
                print(f"{OK()}")
            except Exception as e:
                print(f"{KO()}")

            self._last_report = bytearray(12)

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        print(f"{ACTION()} Trying to ready up device")
        count = 0
        while True:
            print(f"{ACTION()} > Attempt number {count + 1}... ", end="")
            try:
                self.reset_all()
                print(f"{OK()}")
                break
            except OSError as e:
                print(f"{KO()}")
                if "message" in dir(e):
                    print(e.message)
                else:
                    print(e)
                if count + 1 < 5:
                    count += 1
                    time.sleep(1)
                else:
                    raise e
        print(f"{INFO()} Gamepad init success !")

    def crashdump(self, report=None, e=None):
        print("")
        print("=====GURU MEDITATION=====")

        print(f"Buttons:    {RED}", end="")
        print("{0:016b}".format(self._buttons_state))
        print("{}{}".format(DEFAULT, fits_in_2b(self._buttons_state)))

        print(f"Hat:        {self._hat}\t({YELLOW}", end="")
        print("{0:08b}".format(self._hat), end="")
        print("{})\n{}".format(DEFAULT, fits_in_1b(self._hat)))

        print(f"X:          {self._joy_x}\t({GREEN}", end="")
        print("{0:08b}".format(self._joy_x), end="")
        print("{})\n{}".format(DEFAULT, fits_in_1b(self._joy_x)))

        print(f"Y:          {self._joy_y}\t({CYAN}", end="")
        print("{0:08b}".format(self._joy_y), end="")
        print("{})\n{}".format(DEFAULT, fits_in_1b(self._joy_y)))

        print(f"Z:          {self._joy_z}\t({BLUE}", end="")
        print("{0:08b}".format(self._joy_z), end="")
        print("{})\n{}".format(DEFAULT, fits_in_1b(self._joy_z)))

        print(f"RZ:         {self._joy_rz}\t({VIOLET}", end="")
        print("{0:08b}".format(self._joy_rz), end="")
        print("{})\n{}".format(DEFAULT, fits_in_1b(self._joy_rz)))
        print()

        if report:
            print("Report: ", end="")
            
            if type(report) == bytes or type(report) == bytearray:
                print("bytes")
                
                print(RED, end="")
                print("{0:08b}".format(report[0]), end="")
                print("{0:08b}".format(report[1]), end=" ")

                print(YELLOW, end="")
                print("{0:08b}".format(report[2]), end=" ")

                print(GREEN, end="")
                print("{0:08b}".format(report[3]), end=" ")

                print(CYAN, end="")
                print("{0:08b}".format(report[4]), end=" ")

                print(BLUE, end="")
                print("{0:08b}".format(report[5]), end=" ")

                print(VIOLET, end="")
                print("{0:08b}".format(report[6]), end=" ")

                print(DEFAULT)
                
            else:
                print(type(report))
                print(RED, end="")
                buf = "{0:064b}".format(int.from_bytes(report, 'little'))

                for i in range(0, 64):
                    if i == OFFSET_BUTTONS-8:
                        print(YELLOW, end="")
                    elif i == OFFSET_HAT-8:
                        print(GREEN, end="")
                    elif i == OFFSET_JOY_X-8:
                        print(CYAN, end="")
                    elif i == OFFSET_JOY_Y-8:
                        print(BLUE, end="")
                    elif i == OFFSET_JOY_Z-8:
                        print(VIOLET, end="")
                    elif i == OFFSET_JOY_RZ-8:
                        print(WHITE, end="")

                    print(buf[i], end="")
                print(DEFAULT)

        if e:
            raise e

    def reset_buttons(self):
        self._buttons_state = 0

    def press_button(self, bitmask):
        self._buttons_state |= bitmask

    def release_button(self, bitmask):
        self._buttons_state &= ~bitmask

    def set_socd_type(self, value):
        self._socd = value

    def get_socd_type(self):
        return self._socd

    def get_socd_lock(self):
        return self._socd_lock

    def lock_socd(self):
        self._socd_lock = True

    def unlock_socd(self):
        self._socd_lock = False

    def set_dpad(self, value):
        self._hat = value

    def get_dpad(self):
        return self._hat

    def set_lsx(self, value):
        self._joy_x = value

    def get_lsx(self):
        return self._joy_x

    def set_lsy(self, value):
        self._joy_y = value

    def get_lsy(self):
        return self._joy_y

    def set_rsx(self, value):
        self._joy_z = value

    def get_rsx(self):
        return self._joy_z

    def set_rsy(self, value):
        self._joy_rz = value

    def get_rsy(self):
        return self._joy_rz

    def reset_all(self):
        self._buttons_state = 0
        self._hat = 255
        self._joy_x = 127
        self._joy_y = 127
        self._joy_z = 127
        self._joy_rz = 127
        self.send(always=True)

    def send(self, always=False):
        if self._xinput == False:
            # Some weird bit alignment issue makes splitting the button array required
            buttons1 = self._buttons_state >> 8
            buttons2 = ((self._buttons_state << 0) & ((1 << 8) - 1))

            try:
                struct.pack_into("<BBBBBBBB", self._report, 0, buttons2, buttons1, self._hat, self._joy_x, self._joy_y, self._joy_z, self._joy_rz, 0b00000000,)
            except Exception as e:
                self.crashdump(None, e)

            try:
                if always or self._last_report != self._report:
                    self._gamepad_device.send_report(self._report)
                    self._last_report[:] = self._report
            except Exception as e:
                self.crashdump(self._report, e)
        elif self._xinput == True:
            try:
                struct.pack_into("<BBBBBBBBBBBB", self._report, 0, buttons2, buttons1, self._hat, self._joy_x, self._joy_y, self._joy_z, self._joy_rz, 0b00000000, 0x0, 0x0, 0x0, 0x0)
            except Exception as e:
                self.crashdump(None, e)

            try:
                if always or self._last_report != self._report:
                    self._gamepad_device.send_report(self._report)
                    self._last_report[:] = self._report
            except Exception as e:
                self.crashdump(self._report, e)
