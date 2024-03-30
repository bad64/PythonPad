# Capcom being Capcom...
# This basically is turbo LRN: Left+Right resolves to Neutral
# and Up+Down resolves to Neutral as well instead of Up
# as we've been doing for the past decade
#
# Good job Capcom. Really. Could clean that from within SF6
# but nooooooooo. Have to force that on controller makers

def check_import():
    # Canary function to check if the import went okay
    return True

def safe_test(cfg, btn):
    # Testing function to be used for buttons that *may or may not* be present in the config file
    # Mate it's the CPT compliant config, you really don't want to do this here
    for item in cfg:
        try:
            return item[btn].read()
        except:
            pass
    return False

def directionals(gp, AllButtons, x, y, z, rz, LOW, HIGH, \
        HAT_CENTER, HAT_UP, HAT_UP_RIGHT, HAT_RIGHT, HAT_DOWN_RIGHT, HAT_DOWN, HAT_DOWN_LEFT, HAT_LEFT, HAT_UP_LEFT, \
        CENTER, MIN_TILT, MAX_TILT, xAxisModXDelta, xAxisModYDelta, yAxisModXDelta, yAxisModYDelta):
    # Set all analogs to center and leave'em here
    gp.set_lsx(x)
    gp.set_lsy(y)
    gp.set_rsx(z)
    gp.set_rsy(rz)

    # Dpad
    if AllButtons["leftAnalog"]["UP"].read() == LOW and AllButtons["leftAnalog"]["DOWN"].read() == HIGH:
        if AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_UP_LEFT)
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == HIGH:
            gp.set_dpad(HAT_UP)
        elif AllButtons["leftAnalog"]["LEFT"].read() == LOW and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            gp.set_dpad(HAT_UP)
        elif AllButtons["leftAnalog"]["LEFT"].read() == HIGH and AllButtons["leftAnalog"]["RIGHT"].read() == LOW:
            gp.set_dpad(HAT_UP_RIGHT)
    elif (AllButtons["leftAnalog"]["UP"].read() == HIGH and AllButtons["leftAnalog"]["DOWN"].read() == HIGH) \
            or (AllButtons["leftAnalog"]["UP"].read() == LOW and AllButtons["leftAnalog"]["DOWN"].read() == LOW):
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
