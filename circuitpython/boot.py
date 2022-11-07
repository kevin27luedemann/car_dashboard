import usb_cdc
import supervisor
usb_cdc.enable(console=True, data=True)    # Enable console and data

supervisor.disable_autoreload()
