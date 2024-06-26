## Note: I strongly recommend not touching either of these sections, if you need to change what a given button does, go through config.json instead

LEGACY_REPORT_DESCRIPTOR = bytes((
    0x05 ,  0x01 ,          #    USAGE_PAGE (Generic Desktop)
    0x09 ,  0x05 ,          #    USAGE (Game Pad)
    0xa1 ,  0x01 ,          #    COLLECTION (Application)
    0x15 ,  0x00 ,          #    LOGICAL_MINIMUM (0)
    0x25 ,  0x01 ,          #    LOGICAL_MAXIMUM (1)
    0x35 ,  0x00 ,          #    PHYSICAL_MINIMUM (0)
    0x45 ,  0x01 ,          #    PHYSICAL_MAXIMUM (1)
    0x75 ,  0x01 ,          #    REPORT_SIZE (1)
    0x95 ,  0x10 ,          #    REPORT_COUNT (16)
    0x05 ,  0x09 ,          #    USAGE_PAGE (Button)
    0x19 ,  0x01 ,          #    USAGE_MINIMUM (1)
    0x29 ,  0x10 ,          #    USAGE_MAXIMUM (16)
    0x81 ,  0x02 ,          #    INPUT (Data,Var,Abs)
    0x05 ,  0x01 ,          #    USAGE_PAGE (Generic Desktop)
    0x25 ,  0x07 ,          #    LOGICAL_MAXIMUM (7)
    0x46 ,  0x3b ,  0x01 ,  #    PHYSICAL_MAXIMUM (315)
    0x75 ,  0x04 ,          #    REPORT_SIZE (4)
    0x95 ,  0x01 ,          #    REPORT_COUNT (1)
    0x65 ,  0x14 ,          #    UNIT (20)
    0x09 ,  0x39 ,          #    USAGE (Hat Switch)
    0x81 ,  0x42 ,          #    INPUT (Data,Var,Abs)
    0x65 ,  0x00 ,          #    UNIT (0)
    0x95 ,  0x01 ,          #    REPORT_COUNT (1)
    0x81 ,  0x01 ,          #    INPUT (Cnst,Arr,Abs)
    0x26 ,  0xff ,  0x00 ,  #    LOGICAL_MAXIMUM (255)
    0x46 ,  0xff ,  0x00 ,  #    PHYSICAL_MAXIMUM (255) 
    0x09 ,  0x30 ,          #    USAGE (X)
    0x09 ,  0x31 ,          #    USAGE (Y)
    0x09 ,  0x32 ,          #    USAGE (Z)
    0x09 ,  0x35 ,          #    USAGE (Rz)
    0x75 ,  0x08 ,          #    REPORT_SIZE (8)
    0x95 ,  0x04 ,          #    REPORT_COUNT (4)
    0x81 ,  0x02 ,          #    INPUT (Data,Var,Abs)
    0x06 ,  0x00 ,  0xff ,  #    USAGE_PAGE (Vendor Defined 65280)
    0x09 ,  0x20 ,          #    USAGE (32)
    0x95 ,  0x01 ,          #    REPORT_COUNT (1)
    0x81 ,  0x02 ,          #    INPUT (Data,Var,Abs)
    0x0a ,  0x21 ,  0x26 ,  #    USAGE (9761)
    0x95 ,  0x08 ,          #    REPORT_COUNT (8)
    0x91 ,  0x02 ,          #    OUTPUT (Data,Var,Abs)
    0xc0                    #  END_COLLECTION
))

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
MASK_VS_1P =        MASK_Y
MASK_VS_2P =        MASK_X
MASK_VS_3P =        MASK_R
MASK_VS_4P =        MASK_ZL
MASK_VS_1K =        MASK_B
MASK_VS_2K =        MASK_A
MASK_VS_3K =        MASK_L
MASK_VS_4K =        MASK_ZR
