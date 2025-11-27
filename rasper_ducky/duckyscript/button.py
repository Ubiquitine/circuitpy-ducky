import time
import board
import digitalio

BUTTON_BY_BOARD = {
    "waveshare_rp2350_one": "GP29",
    "waveshare_rp2040_one": "GP29",
    "raspberry_pi_pico": "GP15",
    "m5stack_cardputer": "BUTTON",
}

DEFAULT_BUTTON = "GP0"

class Button:

    def __init__(self, pin=None):
        if pin is None:
            pin = self._get_button_pin()
        self.button = digitalio.DigitalInOut(pin)
        self.button.switch_to_input(pull=digitalio.Pull.UP)

    def _get_button_pin(self):
        board_id = getattr(board, "board_id", "").lower()
        pin_name = BUTTON_BY_BOARD.get(board_id, DEFAULT_BUTTON)
        return getattr(board, pin_name, getattr(board, DEFAULT_BUTTON))

    def wait_for_press(self):
        """Wait for button press (transition from HIGH to LOW)"""
        # Wait for button to be released if currently pressed
        while not self.button.value:
            time.sleep(0.01)

        # Wait for button press
        while self.button.value:
            time.sleep(0.01)

        # Debounce
        time.sleep(0.05)

    def is_pressed(self):
        return not self.button.value
