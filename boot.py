import usb_cdc
import usb_hid
import supervisor

# Set how the device presents itself to the host
supervisor.set_usb_identification(
        manufacturer="Bad64",
        product="PythonPad",
        vid=0x0f0d,
        pid=0x0092
        )

TEST_XINPUT = False

if TEST_XINPUT:
    from xinput import XINPUT_REPORT_DESCRIPTOR

    gamepad = usb_hid.Device(
        report_descriptor=XINPUT_REPORT_DESCRIPTOR,
        usage_page=0x01,            # Generic Desktop Control
        usage=0x05,                 # Gamepad
        report_ids=(0,),            # Descriptor uses report ID 0
        in_report_lengths=(12,),    # This gamepad sends 12 bytes in its report.
        out_report_lengths=(1,),    # It does receives one report.
        xinput=True,
    )
else:
    from legacy import LEGACY_REPORT_DESCRIPTOR

    gamepad = usb_hid.Device(
        report_descriptor=LEGACY_REPORT_DESCRIPTOR,
        usage_page=0x01,           # Generic Desktop Control
        usage=0x05,                # Gamepad
        report_ids=(0,),           # Descriptor uses report ID 0
        in_report_lengths=(8,),    # This gamepad sends 8 bytes in its report.
        out_report_lengths=(0,),   # It does not receive any reports.
    )

usb_hid.enable((gamepad,))
usb_cdc.enable(console=True, data=False)
