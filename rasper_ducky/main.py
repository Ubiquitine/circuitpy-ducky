import time
import storage
from duckyscript.button import Button
# sleep at the start to allow the device to be recognized by the host computer
time.sleep(0.5)

btn_pin = Button.get_button_pin()
btn = Button(btn_pin)
safe_mode = btn.is_pressed()


def execute(code: str):
    from duckyscript.lexer import Lexer
    from duckyscript.parser import Parser
    from duckyscript.interpreter import Interpreter
    from duckyscript.preprocessor import Preprocessor
    
    preprocessor = Preprocessor()
    code = preprocessor.process(code)
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(btn)
    interpreter.interpret(ast)
    
    del preprocessor, lexer, tokens, parser, ast, interpreter

if safe_mode or storage.getmount("/").readonly:
    from duckyscript.led import LED
    led = LED()
    print("SAFE MODE. Not executing payload.")
    led.on((255, 0, 255))
    time.sleep(5)
    led.off()
else:
    with open("payload.dd", "r") as file:
        payload_code = file.read()
    execute(payload_code)
