import time
import digitalio
import board
from duckyscript.lexer import Lexer
from duckyscript.parser import Parser
from duckyscript.interpreter import Interpreter
from duckyscript.preprocessor import Preprocessor

# sleep at the start to allow the device to be recognized by the host computer
time.sleep(0.5)

buttonPin = digitalio.DigitalInOut(board.GP29)
buttonPin.switch_to_input(pull=digitalio.Pull.UP)
safe_mode_status = buttonPin.value

def execute(code: str):
    preprocessor = Preprocessor()
    code = preprocessor.process(code)
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(buttonPin)
    interpreter.interpret(ast)

safe_mode = not safe_mode_status
if safe_mode:
    print("SAFE MODE. Not executing payload.")
else:
    with open("payload.dd", "r") as file:
        payload_code = file.read()
    execute(payload_code)
