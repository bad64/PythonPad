import usb_cdc
import usb_hid
import supervisor

# Set how the device presents itself to the host
supervisor.set_usb_identification(
        manufacturer="Bad64",
        product="PicoPad",
        vid=0x0f0d,
        pid=0x0092
        )

# Gamepad report descriptor
GAMEPAD_REPORT_DESCRIPTOR = bytes((
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

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(0,),           # Descriptor uses report ID 0
    in_report_lengths=(8,),    # This gamepad sends 8 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable((gamepad,))
usb_cdc.enable(console=True, data=False)
