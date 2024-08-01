HIGH = True
LOW = False

HAT_CENTER = 255
HAT_UP = 0
HAT_UP_RIGHT = 1
HAT_RIGHT = 2
HAT_DOWN_RIGHT = 3
HAT_DOWN = 4
HAT_DOWN_LEFT = 5
HAT_LEFT = 6
HAT_UP_LEFT = 7

# LIW specific SOCD pseudo-defines
SOCD_LEFT = -1
SOCD_NEUTRAL = 0
SOCD_RIGHT = 1

def check_import():
    # Canary function to check if the import went okay
    return True

def do_buttons(buttons, gp):
    retval = 0
    for button in buttons:
        if button.read() == LOW:
            retval |= button.mask
    gp.set_buttons(retval)

def do_leftstick(socdType, cardinals, gp):
    UP = cardinals[0]
    DOWN = cardinals[1]
    LEFT = cardinals[2]
    RIGHT = cardinals[3]

    retval = HAT_CENTER

    if socdType == "LRN":
        if UP.read() == LOW:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                retval = HAT_UP_LEFT
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                retval = HAT_UP
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                retval = HAT_UP_RIGHT
        elif UP.read() == HIGH and DOWN.read() == HIGH:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                retval = HAT_LEFT
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                retval = HAT_CENTER
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                retval = HAT_RIGHT
        elif UP.read() == HIGH and DOWN.read() == LOW:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                retval = HAT_DOWN_LEFT
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                retval = HAT_DOWN
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                retval = HAT_DOWN_RIGHT
    elif socdType == "CPT":
        if UP.read() == LOW and DOWN.read() == HIGH:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                retval = HAT_UP_LEFT
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                retval = HAT_UP
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                retval = HAT_UP_RIGHT
        elif UP.read() == LOW and DOWN.read() == LOW or UP.read() == HIGH and DOWN.read() == HIGH:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                retval = HAT_LEFT
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                retval = HAT_CENTER
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                retval = HAT_RIGHT
        elif UP.read() == HIGH and DOWN.read() == LOW:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                retval = HAT_DOWN_LEFT
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                retval = HAT_DOWN
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                retval = HAT_DOWN_RIGHT
    elif socdType == "LIW":
        # Get last known dpad state
        dpad_lastframe = gp.get_dpad()
        x_axis_tmp = SOCD_NEUTRAL
        if dpad_lastframe in [ HAT_UP_LEFT, HAT_LEFT, HAT_DOWN_LEFT ]:
            x_axis_tmp = SOCD_LEFT
        elif dpad_lastframe in [ HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT ]:
            x_axis_tmp = SOCD_RIGHT

        # Are both opposite X axis inputs pressed ?
        if LEFT.read() == LOW and RIGHT.read() == LOW:
            # Are we locked ?
            if gp.get_socd_lock() == True:
                # Do nothing
                pass
            elif gp.get_socd_lock() == False:
                # Who's on first ?
                if dpad_lastframe in [ HAT_UP_LEFT, HAT_LEFT, HAT_DOWN_LEFT ]:
                    x_axis_tmp = SOCD_RIGHT     # We right now
                elif dpad_lastframe in [ HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT ]:
                    x_axis_tmp = SOCD_LEFT      # We left now
                else:
                    x_axis_tmp = SOCD_NEUTRAL

                # Then lock
                if gp.get_socd_lock() == False:
                    gp.lock_socd()
        else:
            # Unlock if needed
            if gp.get_socd_lock() == True:
                gp.unlock_socd()

            # Scan buttons as usual
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                x_axis_tmp = SOCD_LEFT
            elif LEFT.read() == HIGH and RIGHT.read() == HIGH:
                x_axis_tmp = SOCD_NEUTRAL
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                x_axis_tmp = SOCD_RIGHT

        # Same for Y axis
        if UP.read() == LOW:
            if x_axis_tmp == SOCD_LEFT:
                retval = HAT_UP_LEFT
            elif x_axis_tmp == SOCD_NEUTRAL:
                retval = HAT_UP
            elif x_axis_tmp == SOCD_RIGHT:
                retval = HAT_UP_RIGHT
        elif UP.read() == HIGH and DOWN.read() == HIGH:
            if x_axis_tmp == SOCD_LEFT:
                retval = HAT_LEFT
            elif x_axis_tmp == SOCD_NEUTRAL:
                retval = HAT_CENTER
            elif x_axis_tmp == SOCD_RIGHT:
                retval = HAT_RIGHT
        elif UP.read() == HIGH and DOWN.read() == LOW:
            if x_axis_tmp == SOCD_LEFT:
                retval = HAT_DOWN_LEFT
            elif x_axis_tmp == SOCD_NEUTRAL:
                retval = HAT_DOWN
            elif x_axis_tmp == SOCD_RIGHT:
                retval = HAT_DOWN_RIGHT

    gp.set_dpad(retval)

def do_rightstick():
    # You're a big fool !
    return False
