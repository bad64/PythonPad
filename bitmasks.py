# Note: I strongly recommend not touching either of these sections, if you need to change what a given button does, go through config.json instead
## General
MASK_UP =           0b0001
MASK_DOWN =         0b0010
MASK_LEFT =         0b0100
MASK_RIGHT =        0b1000

## For Smash (or general Switch usage)
MASK_Y =            0b0000000000000001
MASK_B =            0b0000000000000010
MASK_A =            0b0000000000000100
MASK_X =            0b0000000000001000
MASK_L =            0b0000000000010000
MASK_R =            0b0000000000100000
MASK_ZL =           0b0000000001000000
MASK_ZR =           0b0000000010000000
MASK_SELECT =       0b0000000100000000
MASK_START =        0b0000001000000000
MASK_L3 =           0b0000010000000000
MASK_R3 =           0b0000100000000000
MASK_HOME =         0b0001000000000000
MASK_CAPTURE =      0b0010000000000000
MASK_UNUSED1 =      0b0100000000000000      # Note that these are *actually* unused and most games won't let you bind them
MASK_UNUSED2 =      0b1000000000000000      # joy.cpl sees them though ?

## For regular fighting games
MASK_SQUARE =       0b0000000000000001
MASK_CROSS =        0b0000000000000010
MASK_CIRCLE =       0b0000000000000100
MASK_TRIANGLE =     0b0000000000001000
MASK_L1 =           0b0000000000010000
MASK_R1 =           0b0000000000100000
MASK_L2 =           0b0000000001000000
MASK_R2 =           0b0000000010000000
