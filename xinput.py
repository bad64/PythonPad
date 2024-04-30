XINPUT_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,       # Usage Page (Generic Desktop) 
    0x09, 0x05,       # Usage (Gamepad) \
    0xA1, 0x01,       # Collection (Application) 
    0x85, 0x01,       #  Report ID (1 / keystroke) 

    # This HID report is used for Windows and non-Windows OS.
    # Left Thumbstick 
    0x09, 0x01,       # Usage (Pointer) 
    0xA1, 0x00,       # Collection (Physical) 
    0x09, 0x30,       # Usage (X) 
    0x09, 0x31,       # Usage (Y) 
    0x15, 0x00,       # Logical Min (0) 
    0x27, 0xFF, 0xFF, 0x00, 0x00, # Logical Max (0xFFFF) 
    0x95, 0x02,       # Report Count (2) 
    0x75, 0x10,       # Report Size (16) 
    0x81, 0x02,       # Input (Data,Var,Abs) 
    0xC0,                   # End Collection (Thumbstick) 

    # Right Thumbstick 
    0x09, 0x01,       # Usage (Pointer) 
    0xA1, 0x00,       # Collection (Physical) 
    0x09, 0x32,       # Usage (Z)  X and Y for Right thumbstick (16-bit) 
    0x09, 0x35,       # Usage (Rz) 
    0x15, 0x00,       # Logical Min (0) 
    0x27, 0xFF, 0xFF, 0x00, 0x00,  # Logical Max (0xFFFF) \
    0x95, 0x02,       # Report Count (2) 
    0x75, 0x10,       # Report Size (16) \
    0x81, 0x02,       # Input (Data,Var,Abs) 
    0xC0,                   # End Collection (Thumbstick) 

    # Left Trigger 
    0x05, 0x02,       # Usage Page (Simulation Controls) 
    0x09, 0xC5,       # Usage (Brake) 
    0x15, 0x00,       # Logical Min (0) 
    0x26, 0xFF, 0x03, # Logical Max (0x3FF) 
    0x95, 0x01,       # Report Count (1) 
    0x75, 0x0A,       # Report Size (10) 
    0x81, 0x02,       # Input (Data,Var,Abs) 
    # Padding 6 bits \
    0x15, 0x00,       # Logical Min (0) 
    0x25, 0x00,       # Logical Max (0) 
    0x75, 0x06,       # Report Size (6) 
    0x95, 0x01,       # Report Count (1) 
    0x81, 0x03,       # Input (Constant) 

    # Right Trigger 
    0x05, 0x02,       # Usage Page (Simulation Controls) 
    0x09, 0xC4,       # Usage (Accelerator)  
    0x15, 0x00,       # Logical Min (0) 
