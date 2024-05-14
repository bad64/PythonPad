# LIW specific SOCD pseudo-defines
SOCD_LEFT = -1
SOCD_NEUTRAL = 0
SOCD_RIGHT = 1

def check_import():
    # Canary function to check if the import went okay
    return True

def register_buttons(buttons_task, buttons):
    # Register proxy asynchronous functions to poll buttons
    exec(f"MAP_CIRCLE.register({buttons_task}, {buttons})")
    exec(f"MAP_CROSS.register({buttons_task}, {buttons})")
    exec(f"MAP_SQUARE.register({buttons_task}, {buttons})")
    exec(f"MAP_TRIANGLE.register({buttons_task}, {buttons})")
    exec(f"MAP_L1.register({buttons_task}, {buttons})")
    exec(f"MAP_R1.register({buttons_task}, {buttons})")
    exec(f"MAP_L2.register({buttons_task}, {buttons})")
    exec(f"MAP_R2.register({buttons_task}, {buttons})")
    exec(f"MAP_HOME.register({buttons_task}, {buttons})")
    exec(f"MAP_START.register({buttons_task}, {buttons})")
    exec(f"MAP_SELECT.register({buttons_task}, {buttons})")
    exec(f"MAP_L3.register({buttons_task}, {buttons})")
    exec(f"MAP_R3.register({buttons_task}, {buttons})")

def register_leftanalog():
    #TODO
    pass

def register_rightanalog():
    #TODO
    pass
