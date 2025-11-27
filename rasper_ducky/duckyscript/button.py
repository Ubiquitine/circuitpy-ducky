import time
import board
import digitalio


class Button:
    BUTTON_BY_BOARD = {
        "waveshare_rp2350_one": "GP29",
        "waveshare_rp2040_one": "GP29",
        "raspberry_pi_pico": "GP15",
        "m5stack_cardputer": "BUTTON",
    }

    DEFAULT_BUTTON = "GP0"

    @classmethod
    def get_button_pin(cls):
        board_id = getattr(board, "board_id", "").lower()
        pin_name = cls.BUTTON_BY_BOARD.get(board_id, cls.DEFAULT_BUTTON)
        return getattr(board, pin_name, getattr(board, cls.DEFAULT_BUTTON))

    def __init__(self, pin):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

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
