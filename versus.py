SOCD_LEFT = -1
SOCD_NEUTRAL = 0
SOCD_RIGHT = 1

def check_import():
    return True

def directionals(gp, AllButtons, x, y, z, rz, LOW, HIGH, \
        HAT_CENTER, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, \
        CENTER, MIN_TILT, MAX_TILT, xAxisModXDelta, xAxisModYDelta, yAxisModXDelta, yAxisModYDelta):
    # Set all analogs to center and leave'em here
    gp.set_lsx(x)
    gp.set_lsy(y)
    gp.set_rsx(z)
    gp.set_rsy(rz)

    # Dpad
    ## Left+Right=Neutral
    if gp.get_socd_type() == "LRN":
        if AllButtons["leftAnalog"]["UP"].read() == LOW:
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_UP_LEFT)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_UP)
            elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_UP)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_UP_RIGHT)
        elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_LEFT)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_CENTER)
            elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_CENTER)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_RIGHT)
        elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == LOW:
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_DOWN_LEFT)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                gp.set_dpad(HAT_DOWN)
            elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_DOWN)
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                gp.set_dpad(HAT_DOWN_RIGHT)
    ## Last Input Wins
    elif gp.get_socd_type() in [ "last", "LIW", "lastInputWins" ]:
        # Get current dpad state
        dpad_lastframe = gp.get_dpad()
        x_axis_tmp = SOCD_NEUTRAL
        if dpad_lastframe in [ HAT_UP_LEFT, HAT_LEFT, HAT_DOWN_LEFT ]:
            x_axis_tmp = SOCD_LEFT
        elif dpad_lastframe in [ HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT ]:
            x_axis_tmp = SOCD_RIGHT

        # Are both opposite X axis inputs pressed ?
        if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
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
            if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                x_axis_tmp = SOCD_LEFT
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
                x_axis_tmp = SOCD_NEUTRAL
            elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
                x_axis_tmp = SOCD_RIGHT

        # Do a flip, and also Y axis
        if AllButtons["leftAnalog"]["UP"].read() == LOW:
            if x_axis_tmp == SOCD_LEFT:
                gp.set_dpad(HAT_UP_LEFT)
            elif x_axis_tmp == SOCD_NEUTRAL:
                gp.set_dpad(HAT_UP)
            elif x_axis_tmp == SOCD_RIGHT:
                gp.set_dpad(HAT_UP_RIGHT)
        elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
            if x_axis_tmp == SOCD_LEFT:
                gp.set_dpad(HAT_LEFT)
            elif x_axis_tmp == SOCD_NEUTRAL:
                gp.set_dpad(HAT_CENTER)
            elif x_axis_tmp == SOCD_RIGHT:
                gp.set_dpad(HAT_RIGHT)
        elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == LOW:
            if x_axis_tmp == SOCD_LEFT:
                gp.set_dpad(HAT_DOWN_LEFT)
            elif x_axis_tmp == SOCD_NEUTRAL:
                gp.set_dpad(HAT_DOWN)
            elif x_axis_tmp == SOCD_RIGHT:
                gp.set_dpad(HAT_DOWN_RIGHT)
