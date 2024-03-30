def check_import():
    # Canary function to check if the import went okay
    return True

def safe_test(cfg, btn):
    # Testing function to be used for buttons that *may or may not* be present in the config file
    # Here I'm testing for V and W modifier keys for example
    for item in cfg:
        try:
            return item[btn].read()
        except:
            pass
    return False

def directionals(gp, AllButtons, x, y, z, rz, LOW, HIGH, \
        HAT_CENTER, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, \
        CENTER, MIN_TILT, MAX_TILT, xAxisModXDelta, xAxisModYDelta, yAxisModXDelta, yAxisModYDelta):
    # Left stick
    ## X axis
    if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
        x = MIN_TILT
        if gp.get_socd_lock() == True:
            gp.unlock_socd()
    elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
        x = CENTER
        if gp.get_socd_lock() == True:
            gp.unlock_socd()
    elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
        x = MAX_TILT
        if gp.get_socd_lock() == True:
            gp.unlock_socd()
    elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
        if gp.get_socd_type() == "LRN":
            x = CENTER
        elif gp.get_socd_type() in [ "LIW", "last", "lastInputWins" ]:
            # Reference current state of directions
            lsx_last = gp.get_lsx()

            # Are we locked ?
            if gp.get_socd_lock() == True:
                # Do nuthin'
                x = lsx_last
            elif gp.get_socd_lock() == False:
                # Who's on first ?
                if lsx_last < 127:      # We should be somewhere on the left
                    x = MAX_TILT        # So we set the virtual stick to the right
                #elif lsx_last == 127:   # Should not be possible; do something about it
                #    pass
                elif lsx_last > 127:    # Yadda yadda right yadda stick to left
                    x = MIN_TILT

                # Aaaand we lock
                if gp.get_socd_lock() == False:
                    gp.lock_socd()

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
    if AllButtons["rightAnalog"]["C_UP"].read() == LOW and AllButtons["rightAnalog"]["C_DOWN"].read() == HIGH:
        rz = MIN_TILT
        if AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH:
            z = MIN_TILT
        elif AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW:
            z = MAX_TILT
        elif (AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH) \
        or (AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW):
            z = CENTER
    elif AllButtons["rightAnalog"]["C_UP"].read() == HIGH and AllButtons["rightAnalog"]["C_DOWN"].read() == LOW:
        rz = MAX_TILT
        if AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH:
            z = MIN_TILT
        elif AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW:
            z = MAX_TILT
        elif (AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH) \
        or (AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW):
            z = CENTER
    elif (AllButtons["rightAnalog"]["C_UP"].read() == HIGH and AllButtons["rightAnalog"]["C_DOWN"].read() == HIGH) \
    or (AllButtons["rightAnalog"]["C_UP"].read() == LOW and AllButtons["rightAnalog"]["C_DOWN"].read() == LOW):
        rz = CENTER
        if AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH:
            z = MIN_TILT
            if safe_test(AllButtons["modifiers"], "MOD_V") or AllButtons["modifiers"]["MOD_X"].read() == LOW:
                rz = MIN_TILT
            elif safe_test(AllButtons["modifiers"], "MOD_W") or AllButtons["modifiers"]["MOD_Y"].read() == LOW:
                rz = MAX_TILT
        elif AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW:
            z = MAX_TILT
            if safe_test(AllButtons["modifiers"], "MOD_V") or AllButtons["modifiers"]["MOD_X"].read() == LOW:
                rz = MIN_TILT
            elif safe_test(AllButtons["modifiers"], "MOD_W") or AllButtons["modifiers"]["MOD_Y"].read() == LOW:
                rz = MAX_TILT
        elif (AllButtons["rightAnalog"]["C_LEFT"].read() == HIGH and AllButtons["rightAnalog"]["C_RIGHT"].read() == HIGH) \
        or (AllButtons["rightAnalog"]["C_LEFT"].read() == LOW and AllButtons["rightAnalog"]["C_RIGHT"].read() == LOW):
            # No need to test for extra modifiers
            z = CENTER

    gp.set_rsx(z)
    gp.set_rsy(rz)
