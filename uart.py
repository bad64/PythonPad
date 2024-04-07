# Ancillary UART related display functions

# Colors
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BLUE = "\033[34m"
VIOLET = "\033[35m"
WHITE = "\033[37m"
DEFAULT = "\033[39m"

# Shortcut functions for things printed everywhere
def INFO():
    return f"[{BLUE}INFO{DEFAULT}]"

def WARN():
    return f"[{YELLOW}WARNING{DEFAULT}]"

def ACTION():
    return f"[{CYAN}ACTION{DEFAULT}]"

def ERROR():
    return f"[{RED}ERROR{DEFAULT}]"

def DEBUG():
    return f"[{VIOLET}DEBUG{DEFAULT}]"

def OK():
    return f"{DEFAULT}[{GREEN}OK{DEFAULT}]"

def KO():
    return f"{DEFAULT}[{GREEN}KO{DEFAULT}]"

def CONFUSED():
    return f"{DEFAULT}[{YELLOW}??{DEFAULT}]"
