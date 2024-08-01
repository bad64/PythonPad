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

def do_leftstick(socdType, cardinals, modifiers, tilt_values, gp):
    UP = cardinals[0]
    DOWN = cardinals[1]
    LEFT = cardinals[2]
    RIGHT = cardinals[3]

    MOD_X = modifiers[0]
    MOD_Y = modifiers[1]

    if MOD_X.read() == LOW and MOD_Y.read() == LOW:
        # D-pad mode
        gp.set_lsx(tilt_values["X_CENTER"])
        gp.set_lsy(tilt_values["Y_CENTER"])

        ## Let's face it: if you're in Smash mode you're just taunting with the d-pad
        ## Not gonna implement SOCD based logic, CPT will do fine
        if UP.read() == LOW and DOWN.read() == HIGH:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                gp.set_dpad(HAT_UP_LEFT)
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                gp.set_dpad(HAT_UP)
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                gp.set_dpad(HAT_UP_RIGHT)
        elif UP.read() == LOW and DOWN.read() == LOW or UP.read() == HIGH and DOWN.read() == HIGH:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                gp.set_dpad(HAT_LEFT)
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                gp.set_dpad(HAT_CENTER)
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                gp.set_dpad(HAT_RIGHT)
        elif UP.read() == HIGH and DOWN.read() == LOW:
            if LEFT.read() == LOW and RIGHT.read() == HIGH:
                gp.set_dpad(HAT_DOWN_LEFT)
            elif LEFT.read() == LOW and RIGHT.read() == LOW or LEFT.read() == HIGH and RIGHT.read() == HIGH:
                gp.set_dpad(HAT_DOWN)
            elif LEFT.read() == HIGH and RIGHT.read() == LOW:
                gp.set_dpad(HAT_DOWN_RIGHT)
    else:
        gp.set_dpad(HAT_CENTER)
        x = tilt_values["X_CENTER"]
        y = tilt_values["Y_CENTER"]

        # Sort out the X axis first without modifiers
        if LEFT.read() == LOW and RIGHT.read() == HIGH:
            x = tilt_values["X_NEGATIVE"]
            if gp.get_socd_lock() == True:
                gp.unlock_socd()
        elif LEFT.read() == HIGH and RIGHT.read() == LOW:
            x = tilt_values["X_POSITIVE"]
            if gp.get_socd_lock() == True:
                gp.unlock_socd()
        elif LEFT.read() == HIGH and RIGHT.read() == HIGH:
            x = tilt_values["X_CENTER"]        
            if gp.get_socd_lock() == True:
                gp.unlock_socd()
        elif LEFT.read() == LOW and RIGHT.read() == LOW:
            if socdType in [ "LRN", "CPT"]:
                x = tilt_values["X_CENTER"]
            elif socdType == "LIW":
                # Get last X axis state
                last_x = gp.get_lsx()

                # Are we locked ?
                if gp.get_socd_lock() == True:
                    # Don't do squat
                    x = last_x
                elif gp.get_socd_lock() == False:
                    # Who got here first ?
                    if last_x < tilt_values["X_CENTER"]:
                        x = tilt_values["X_POSITIVE"]
                    elif last_x > tilt_values["X_CENTER"]:
                        x = tilt_values["X_NEGATIVE"]

                    # Don't forget to lock
                    if gp.get_socd_lock() == False:
                        gp.lock_socd()

        # Do Y axis now
        if UP.read() == LOW:
            y = tilt_values["Y_NEGATIVE"]
        elif UP.read() == HIGH and DOWN.read() == LOW:
            y = tilt_values["Y_POSITIVE"]
        else:
            y = tilt_values["Y_CENTER"]

        # Apply modifiers
        if x == tilt_values["X_NEGATIVE"]:
            if MOD_X.read() == LOW and MOD_Y.read() == HIGH:
                x = tilt_values["X_MOD_X_NEGATIVE"]
            elif MOD_X.read() == HIGH and MOD_Y.read() == LOW:
                x = tilt_values["X_MOD_Y_NEGATIVE"]
            else:
                pass
        elif x == tilt_values["X_POSITIVE"]:
            if MOD_X.read() == LOW and MOD_Y.read() == HIGH:
                x = tilt_values["X_MOD_X_POSITIVE"]
            elif MOD_X.read() == HIGH and MOD_Y.read() == LOW:
                x = tilt_values["X_MOD_Y_POSITIVE"]
            else:
                pass

        if y == tilt_values["Y_NEGATIVE"]:
            if MOD_X.read() == LOW and MOD_Y.read() == HIGH:
                y = tilt_values["Y_MOD_X_NEGATIVE"]
            elif MOD_X.read() == HIGH and MOD_Y.read() == LOW:
                y = tilt_values["Y_MOD_Y_NEGATIVE"]
            else:
                pass
        elif y == tilt_values["Y_POSITIVE"]:
            if MOD_X.read() == LOW and MOD_Y.read() == HIGH:
                y = tilt_values["Y_MOD_X_POSITIVE"]
            elif MOD_X.read() == HIGH and MOD_Y.read() == LOW:
                y = tilt_values["Y_MOD_Y_POSITIVE"]
            else:
                pass

        gp.set_lsx(x)
        gp.set_lsy(y)

def do_rightstick(buttons, MIN_TILT, CENTER, MAX_TILT, gp):
    C_UP = buttons[0]
    C_DOWN = buttons[1]
    C_LEFT = buttons[2]
    C_RIGHT = buttons[3]

    if C_LEFT.read() == LOW and C_RIGHT.read() == HIGH:
        gp.set_rsx(MIN_TILT)
    elif C_LEFT.read() == HIGH and C_RIGHT.read() == LOW:
        gp.set_rsx(MAX_TILT)
    else:
        gp.set_rsx(CENTER)

    if C_UP.read() == LOW and C_DOWN.read() == HIGH:
        gp.set_rsy(MIN_TILT)
    elif C_UP.read() == HIGH and C_DOWN.read() == LOW:
        gp.set_rsy(MAX_TILT)
    else:
        gp.set_rsy(CENTER)

