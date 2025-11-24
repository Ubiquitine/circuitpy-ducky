import board
import digitalio
import storage

NO_STORAGE_PIN = digitalio.DigitalInOut(board.GP29)
NO_STORAGE_PIN.switch_to_input(pull=digitalio.Pull.UP)
no_storage_status = NO_STORAGE_PIN.value

no_storage = no_storage_status
if no_storage:
    storage.disable_usb_drive()
