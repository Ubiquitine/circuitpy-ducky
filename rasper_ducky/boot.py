import storage
from duckyscript.button import Button

# Enable payload execution
ARMED=False

btn = Button()

no_storage = not btn.is_pressed()
if no_storage and ARMED:
    storage.disable_usb_drive()
