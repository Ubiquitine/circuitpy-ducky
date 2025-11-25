import neopixel
import board
import digitalio

class LED:
    def __init__(self, brightness=0.2):
        self.use_neopixel = False
        self.use_gpio_led = False
        self.pixel = None
        self.gpio_led = None

        # --- Try NeoPixel first ---
        neopixel_pin = getattr(board, "NEOPIXEL", None)
        if neopixel_pin is not None:
            try:
                self.pixel = neopixel.NeoPixel(
                    neopixel_pin, 1, brightness=brightness, auto_write=True
                )
                self.use_neopixel = True
                return
            except Exception:
                pass  # If NeoPixel init fails, fall back to LED pin

        # --- Try simple LED pin next ---
        led_pin = getattr(board, "LED", None)
        if led_pin is not None:
            try:
                self.gpio_led = digitalio.DigitalInOut(led_pin)
                self.gpio_led.direction = digitalio.Direction.OUTPUT
                self.use_gpio_led = True
                return
            except Exception:
                pass

        # --- No LED present ---
        self.use_neopixel = False
        self.use_gpio_led = False

    def on(self, color=(255, 255, 255)):
        """Turn the LED or NeoPixel on."""
        if self.use_neopixel and self.pixel:
            self.pixel[0] = color
        elif self.use_gpio_led and self.gpio_led:
            # Simple GPIO LED: any color means ON
            self.gpio_led.value = True
        else:
            pass  # No LED available

    def off(self):
        """Turn the LED off."""
        if self.use_neopixel and self.pixel:
            self.pixel[0] = (0, 0, 0)
        elif self.use_gpio_led and self.gpio_led:
            self.gpio_led.value = False
        else:
            pass  # No LED available
