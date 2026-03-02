import neopixel # type: ignore
import board
import digitalio

PIXEL_ORDER_BY_BOARD = {
    "waveshare_rp2350_one": neopixel.RGB,
    "waveshare_rp2040_one": neopixel.RGB,
}

DEFAULT_PIXEL_ORDER = neopixel.GRB

class LED:
    def __init__(self, brightness=0.2):
        self.use_neopixel = False
        self.use_gpio_led = False
        self.pixel = None
        self.gpio_led = None

        neopixel_pin = getattr(board, "NEOPIXEL", None)
        if neopixel_pin is not None:
            try:
                order = self._get_pixel_order()
                self.pixel = neopixel.NeoPixel(
                    neopixel_pin, 1,
                    brightness=brightness,
                    auto_write=True,
                    pixel_order=order
                )
                self.use_neopixel = True
                return
            except Exception as e:
                print("NeoPixel init failed:", e)

        led_pin = getattr(board, "LED", None)
        if led_pin is not None:
            try:
                self.gpio_led = digitalio.DigitalInOut(led_pin)
                self.gpio_led.direction = digitalio.Direction.OUTPUT # type: ignore
                self.use_gpio_led = True
                return
            except Exception as e:
                print("GPIO LED init failed:", e)

    def _get_pixel_order(self):
        board_id = getattr(board, "board_id", "").lower()
        return PIXEL_ORDER_BY_BOARD.get(board_id, DEFAULT_PIXEL_ORDER)

    def on(self, color=(255, 255, 255)):
        if self.use_neopixel and self.pixel:
            self.pixel[0] = color
        elif self.use_gpio_led and self.gpio_led:
            self.gpio_led.value = True  # type: ignore

    def off(self):
        if self.use_neopixel and self.pixel:
            self.pixel[0] = (0, 0, 0)
        elif self.use_gpio_led and self.gpio_led:
            self.gpio_led.value = False  # type: ignore
