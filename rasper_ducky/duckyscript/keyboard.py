import usb_hid
from adafruit_hid.keyboard import Keyboard


# type: ignore
class RasperDuckyKeyboard:
    def __init__(self, platform: str, language: str):
        self.platform = platform
        self.language = language

        if platform.upper() == "WIN" and language.upper() == "US":
            from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
            from adafruit_hid.keycode import Keycode

            kbd = Keyboard(usb_hid.devices)
            layout = KeyboardLayoutUS(kbd)
            keycode = Keycode

            self.kbd = kbd
            self.layout = layout
        else:
            try:
                layout = __import__(f"keyboard_layout_{platform}_{language}")
                keycode = __import__(f"keycode_{platform}_{language}").Keycode
            except ImportError:
                raise ValueError(
                    f"Language {language} not supported for platform {platform}"
                )
            self.kbd = Keyboard(usb_hid.devices)
            self.layout = layout.KeyboardLayout(self.kbd)

        self.KEYCODES = {
            "WINDOWS": keycode.WINDOWS,
            "GUI": keycode.GUI,
            "APP": keycode.APPLICATION,
            "MENU": keycode.APPLICATION,
            "SHIFT": keycode.SHIFT,
            "ALT": keycode.ALT,
            "CONTROL": keycode.CONTROL,
            "CTRL": keycode.CONTROL,
            "DOWNARROW": keycode.DOWN_ARROW,
            "DOWN": keycode.DOWN_ARROW,
            "LEFTARROW": keycode.LEFT_ARROW,
            "LEFT": keycode.LEFT_ARROW,
            "RIGHTARROW": keycode.RIGHT_ARROW,
            "RIGHT": keycode.RIGHT_ARROW,
            "UPARROW": keycode.UP_ARROW,
            "UP": keycode.UP_ARROW,
            "BREAK": keycode.PAUSE,
            "PAUSE": keycode.PAUSE,
            "CAPSLOCK": keycode.CAPS_LOCK,
            "DELETE": keycode.DELETE,
            "END": keycode.END,
            "ESC": keycode.ESCAPE,
            "ESCAPE": keycode.ESCAPE,
            "HOME": keycode.HOME,
            "INSERT": keycode.INSERT,
            "NUMLOCK": keycode.KEYPAD_NUMLOCK,
            "PAGEUP": keycode.PAGE_UP,
            "PAGEDOWN": keycode.PAGE_DOWN,
            "PRINTSCREEN": keycode.PRINT_SCREEN,
            "ENTER": keycode.ENTER,
            "SCROLLLOCK": keycode.SCROLL_LOCK,
            "SPACE": keycode.SPACE,
            "TAB": keycode.TAB,
            "BACKSPACE": keycode.BACKSPACE,
            "A": keycode.A,
            "B": keycode.B,
            "C": keycode.C,
            "D": keycode.D,
            "E": keycode.E,
            "F": keycode.F,
            "G": keycode.G,
            "H": keycode.H,
            "I": keycode.I,
            "J": keycode.J,
            "K": keycode.K,
            "L": keycode.L,
            "M": keycode.M,
            "N": keycode.N,
            "O": keycode.O,
            "P": keycode.P,
            "Q": keycode.Q,
            "R": keycode.R,
            "S": keycode.S,
            "T": keycode.T,
            "U": keycode.U,
            "V": keycode.V,
            "W": keycode.W,
            "X": keycode.X,
            "Y": keycode.Y,
            "Z": keycode.Z,
            "F1": keycode.F1,
            "F2": keycode.F2,
            "F3": keycode.F3,
            "F4": keycode.F4,
            "F5": keycode.F5,
            "F6": keycode.F6,
            "F7": keycode.F7,
            "F8": keycode.F8,
            "F9": keycode.F9,
            "F10": keycode.F10,
            "F11": keycode.F11,
            "F12": keycode.F12,
        }

    def type_string(self, string):
        self.layout.write(string)

    def press_key(self, key: str):
        self.kbd.press(self.KEYCODES[key])

    def release_key(self, key: str):
        self.kbd.release(self.KEYCODES[key])

    def release_all(self):
        self.kbd.release_all()
