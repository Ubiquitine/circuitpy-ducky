import board
import neopixel

class LED:
    def __init__(self, brightness=0.2):
        # One RGB LED connected to board.NEOPIXEL
        self.pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=brightness, auto_write=True)

    def on(self, color=(255, 255, 255)):
        """Turn the LED on with a given RGB color (default: white)."""
        self.pixel[0] = color

    def off(self):
        """Turn the LED off."""
        self.pixel[0] = (0, 0, 0)