def check_import():
    return True

def directionals(gp, AllButtons, x, y, z, rz, LOW, HIGH, \
        HAT_CENTER, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, \
        CENTER, MIN_TILT, MAX_TILT, xAxisModXDelta, xAxisModYDelta, yAxisModXDelta, yAxisModYDelta, \
        socdType, socdLastX, socdLastY):
    # Set all analogs to center and leave'em here
    gp.set_lsx(x)
    gp.set_lsy(y)
    gp.set_rsx(z)
    gp.set_rsy(rz)

    # Dpad
    ## Get the current dpad state
    dpad_lastframe = gp.get_dpad()

    if AllButtons["leftAnalog"]["UP"].read() == LOW:
        if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_UP_LEFT)
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_UP)
        elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            if socdType == "LRN":
                gp.set_dpad(HAT_UP)
            elif socdType == "last":
               pass 
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            gp.set_dpad(HAT_UP_RIGHT)
    elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
        if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_LEFT)
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_CENTER)
        elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            if socdType == "LRN":
                gp.set_dpad(HAT_CENTER)
            elif socdType == "last":
               pass 
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            gp.set_dpad(HAT_RIGHT)
    elif AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == LOW:
        if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_DOWN_LEFT)
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_DOWN)
        elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            if socdType == "LRN":
                gp.set_dpad(HAT_DOWN)
            elif socdType == "last":
               pass 
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            gp.set_dpad(HAT_DOWN_RIGHT)
