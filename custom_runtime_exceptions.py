# Runtime exceptions for debug purposes

class WrongDefaultModeException(Exception):
    "Raised when the defaultMode property isn't a valid mode defined in the config file"
    def __init__(self, emode):
        self.mode = emode
        self.message = f"{emode} is not a valid mode setting"

class WrongSOCDCleaningTypeException(Exception):
    "Raised when the socdType property isn't a valid mode defined in the config file"
    def __init__(self, emode):
        self.mode = emode
        self.message = f"{emode} is not a valid SOCD cleaning type"
