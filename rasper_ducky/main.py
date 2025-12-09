import time
import storage
# sleep at the start to allow the device to be recognized by the host computer
time.sleep(0.5)


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
    interpreter = Interpreter()
    interpreter.interpret(ast)
    
    del preprocessor, lexer, tokens, parser, ast, interpreter

if storage.getmount("/").readonly: # type: ignore
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
