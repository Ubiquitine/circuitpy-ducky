import time

class Button:
    def __init__(self, pin):
        self.button = pin

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
