import storage
from duckyscript.button import Button

# Enable payload execution
ARMED=False

btn_pin = Button.get_button_pin()
btn = Button(btn_pin)

no_storage = not btn.is_pressed()
if no_storage and ARMED:
    storage.disable_usb_drive()
