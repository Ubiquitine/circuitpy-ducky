class Tok:
    VAR = "VAR"
    DELAY = "DELAY"
    IDENTIFIER = "IDENTIFIER"
    ASSIGN = "ASSIGN"
    SKIP = "SKIP"
    MISMATCH = "MISMATCH"
    PRINTSTRING = "PRINTSTRING"
    PRINTSTRINGLN = "PRINTSTRINGLN"
    EOF = "EOF"
    EOL = "EOL"
    KEYPRESS = "KEYPRESS"
    REM = "REM"
    REM_BLOCK = "REM_BLOCK"
    END_REM_BLOCK = "END_REM_BLOCK"
    WAIT_FOR_BUTTON_PRESS = "WAIT_FOR_BUTTON_PRESS"
    BUTTON_DEF = "BUTTON_DEF"
    END_BUTTON = "END_BUTTON"
    LED_G = "LED_G"
    LED_R = "LED_R"
    LED_B = "LED_B"
    LED_OFF = "LED_OFF"
    HOLD = "HOLD"
    RELEASE = "RELEASE"
    RANDOM_CHAR = "RANDOM_CHAR"
    RANDOM_CHAR_FROM = "RANDOM_CHAR_FROM"
    ATTACKMODE = "ATTACKMODE"
    HID = "HID"
    STORAGE = "STORAGE"
    OFF = "OFF"
    IF = "IF"
    THEN = "THEN"
    END_IF = "END_IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"
    WHILE = "WHILE"
    END_WHILE = "END_WHILE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    FUNCTION = "FUNCTION"
    END_FUNCTION = "END_FUNCTION"
    RETURN = "RETURN"
    # OPERATORS
    OP_SHIFT_LEFT = "OP_SHIFT_LEFT"
    OP_SHIFT_RIGHT = "OP_SHIFT_RIGHT"
    OP_GREATER_EQUAL = "OP_GREATER_EQUAL"
    OP_LESS_EQUAL = "OP_LESS_EQUAL"
    OP_EQUAL = "OP_EQUAL"
    OP_NOT_EQUAL = "OP_NOT_EQUAL"
    OP_GREATER = "OP_GREATER"
    OP_LESS = "OP_LESS"
    OP_OR = "OP_OR"
    OP_BITWISE_AND = "OP_BITWISE_AND"
    OP_BITWISE_OR = "OP_BITWISE_OR"
    OP_PLUS = "OP_PLUS"
    OP_MINUS = "OP_MINUS"
    OP_MULTIPLY = "OP_MULTIPLY"
    OP_DIVIDE = "OP_DIVIDE"
    OP_MODULO = "OP_MODULO"
    OP_POWER = "OP_POWER"
    OP_NOT = "OP_NOT"
    OP_AND = "OP_AND"
    # LITERALS
    STRING = "STRING"
    NUMBER = "NUMBER"
    TRUE = "TRUE"
    FALSE = "FALSE"
    # CUSTOM RASPER DUCKY COMMANDS (non rubber ducky standards)
    RD_KBD = "RD_KBD"
    RD_KBD_PLATFORM = "RD_KBD_PLATFORM"
    RD_KBD_LANGUAGE = "RD_KBD_LANGUAGE"


class Token:
    __slots__ = ('type', 'value', 'line', 'column')

    def __init__(self, tok_type, value="", line=0, column=0):
        self.type = tok_type
        self.value = value
        self.line = line
        self.column = column

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return "TOKEN(" + self.type + ", " + self.value + ", " + str(self.line) + ", " + str(self.column) + ")"


class Lexer:
    __slots__ = ('code', 'start', 'current', 'line', 'line_start', 'end',
                 '_OPERATORS', '_KEYWORDS', '_OPERATORS_SET', '_ALPHA_EXTRAS',
                 '_STRING_TOKEN_TYPES', '_has_isupper')

    def __init__(self, code):
        self.code = code
        self.start = 0
        self.current = 0
        self.line = 1
        self.line_start = 0
        self.end = len(code)

        # Detect if isupper() is available (only method that might be missing)
        try:
            "A".isupper()
            self._has_isupper = True
        except AttributeError:
            self._has_isupper = False

        # Cache lookups in instance for faster access
        self._OPERATORS = {
            "=": Tok.ASSIGN,
            "==": Tok.OP_EQUAL,
            "!=": Tok.OP_NOT_EQUAL,
            ">": Tok.OP_GREATER,
            "<": Tok.OP_LESS,
            ">=": Tok.OP_GREATER_EQUAL,
            "<=": Tok.OP_LESS_EQUAL,
            "&&": Tok.OP_AND,
            "||": Tok.OP_OR,
            "!": Tok.OP_NOT,
            "+": Tok.OP_PLUS,
            "-": Tok.OP_MINUS,
            "*": Tok.OP_MULTIPLY,
            "/": Tok.OP_DIVIDE,
            "%": Tok.OP_MODULO,
            "^": Tok.OP_POWER,
            "&": Tok.OP_BITWISE_AND,
            "|": Tok.OP_BITWISE_OR,
            "<<": Tok.OP_SHIFT_LEFT,
            ">>": Tok.OP_SHIFT_RIGHT,
            "(": Tok.LPAREN,
            ")": Tok.RPAREN,
        }

        self._OPERATORS_SET = frozenset("=><!)+-*/%^&|(")

        self._KEYWORDS = {
            "VAR": Tok.VAR,
            "DELAY": Tok.DELAY,
            "STRING": Tok.PRINTSTRING,
            "STRINGLN": Tok.PRINTSTRINGLN,
            "ATTACKMODE": Tok.ATTACKMODE,
            "HID": Tok.HID,
            "STORAGE": Tok.STORAGE,
            "OFF": Tok.OFF,
            "IF": Tok.IF,
            "THEN": Tok.THEN,
            "END_IF": Tok.END_IF,
            "ELSE": Tok.ELSE,
            "ELSE_IF": Tok.ELSE_IF,
            "WHILE": Tok.WHILE,
            "END_WHILE": Tok.END_WHILE,
            "FUNCTION": Tok.FUNCTION,
            "END_FUNCTION": Tok.END_FUNCTION,
            "RETURN": Tok.RETURN,
            "TRUE": Tok.TRUE,
            "FALSE": Tok.FALSE,
            "AND": Tok.OP_AND,
            "OR": Tok.OP_OR,
            "NOT": Tok.OP_NOT,
            "HOLD": Tok.HOLD,
            "RELEASE": Tok.RELEASE,
            "RANDOM_LOWERCASE_LETTER": Tok.RANDOM_CHAR,
            "RANDOM_UPPERCASE_LETTER": Tok.RANDOM_CHAR,
            "RANDOM_LETTER": Tok.RANDOM_CHAR,
            "RANDOM_NUMBER": Tok.RANDOM_CHAR,
            "RANDOM_SPECIAL": Tok.RANDOM_CHAR,
            "RANDOM_CHAR": Tok.RANDOM_CHAR,
            "RANDOM_CHAR_FROM": Tok.RANDOM_CHAR_FROM,
            "WAIT_FOR_BUTTON_PRESS": Tok.WAIT_FOR_BUTTON_PRESS,
            "BUTTON_DEF": Tok.BUTTON_DEF,
            "END_BUTTON": Tok.END_BUTTON,
            "LED_G": Tok.LED_G,
            "LED_R": Tok.LED_R,
            "LED_B": Tok.LED_B,
            "LED_OFF": Tok.LED_OFF,
            "RD_KBD": Tok.RD_KBD,
        }

        # Include $ and # for variables and defines
        self._ALPHA_EXTRAS = frozenset("_$#")

        # Pre-cache token types that need string parsing
        self._STRING_TOKEN_TYPES = frozenset([Tok.PRINTSTRING, Tok.PRINTSTRINGLN, Tok.RANDOM_CHAR_FROM])

    def is_at_end(self):
        return self.current >= self.end

    def advance(self):
        current = self.current
        if current < self.end:
            self.current = current + 1
            return self.code[current]
        return None

    def previous(self):
        current = self.current
        return self.code[current - 1] if current > 0 else None

    def peek(self):
        current = self.current
        return self.code[current] if current < self.end else None

    def peek_next(self):
        current = self.current + 1
        return self.code[current] if current < self.end else None

    def match(self, expected):
        current = self.current
        code = self.code
        if current >= self.end or not code.startswith(expected, current):
            return False
        self.current = current + len(expected)
        return True

    def tokenize(self):
        previous_token = None
        is_at_end = self.is_at_end
        scan_token = self.scan_token

        while not is_at_end():
            self.start = self.current
            previous_token = scan_token(previous_token)
            if previous_token:
                yield previous_token
        yield Token(Tok.EOF)

    def is_digit(self, char):
        return char is not None and char.isdigit()

    def is_alpha(self, char):
        if char is None:
            return False
        return char.isalpha() or char in self._ALPHA_EXTRAS

    def is_alphanumeric(self, char):
        if char is None:
            return False
        return self.is_digit(char) or self.is_alpha(char)

    def is_operator(self, char):
        return char in self._OPERATORS_SET if char else False

    def is_comment(self, char):
        if char != "R":
            return False
        current = self.current
        code = self.code
        return (code.startswith("EM", current) and
                not code.startswith("EM_BLOCK", current))

    def is_comment_block(self, char):
        if char != "R":
            return False
        return self.code.startswith("EM_BLOCK", self.current)

    def number(self):
        peek = self.peek
        is_digit = self.is_digit
        advance = self.advance

        while is_digit(peek()):
            advance()

        # Check for decimal
        p = peek()
        if p == "." and is_digit(self.peek_next()):
            advance()
            while is_digit(peek()):
                advance()

        return self.token(Tok.NUMBER, self.code[self.start:self.current])

    def string(self):
        # Skip the first space between STRING or STRINGLN and the string
        self.start += 1
        code = self.code
        current = self.current
        end = self.end

        # Fast forward to newline
        while current < end and code[current] != "\n":
            current += 1
        self.current = current

        return self.token(Tok.STRING, code[self.start:current].strip())

    def kbd_platform(self):
        self.start += 1
        code = self.code
        current = self.current
        end = self.end

        # Fast forward to space
        while current < end and code[current] != " ":
            current += 1
        self.current = current

        return self.token(Tok.RD_KBD_PLATFORM, code[self.start:current].strip())

    def kbd_language(self):
        self.start += 1
        code = self.code
        current = self.current
        end = self.end

        # Fast forward to newline
        while current < end and code[current] != "\n":
            current += 1
        self.current = current

        return self.token(Tok.RD_KBD_LANGUAGE, code[self.start:current].strip())

    def identifier(self):
        peek = self.peek
        is_alphanumeric = self.is_alphanumeric
        advance = self.advance
        code = self.code

        while is_alphanumeric(peek()):
            advance()

        identifier = code[self.start:self.current]
        keywords = self._KEYWORDS
        keyword = keywords.get(identifier)

        # Check for ELSE IF
        if keyword == Tok.ELSE and peek() == " ":
            current = self.current
            end = self.end
            # Skip spaces
            while current < end and code[current] == " ":
                current += 1
            self.current = current

            if self.match("IF"):
                return self.token(Tok.ELSE_IF, "ELSE IF")

        # Check for keypresses (all uppercase identifiers without $ or #)
        if keyword is None and "$" not in identifier and "#" not in identifier:
            if self._has_isupper:
                # Use fast built-in method
                if identifier.isupper():
                    return self.token(Tok.KEYPRESS, identifier)
            else:
                # CircuitPython fallback: manual check
                is_upper = True
                for c in identifier:
                    if "a" <= c <= "z":
                        is_upper = False
                        break
                if is_upper:
                    return self.token(Tok.KEYPRESS, identifier)

        return self.token(keyword if keyword else Tok.IDENTIFIER, identifier)

    def column(self):
        return self.start - self.line_start + 1

    def advance_while(self, condition):
        peek = self.peek
        advance = self.advance
        is_at_end = self.is_at_end

        while not is_at_end():
            p = peek()
            if not condition(p):
                break
            advance()

    def unexpected_character(self, char):
        return SyntaxError(
            "Unexpected character: '" + char + "' at line " +
            str(self.line) + ", column " + str(self.column())
        )

    def unexpected_none(self):
        return SyntaxError(
            "Unexpected None character at line " + str(self.line) +
            ", column " + str(self.column())
        )

    def operator(self):
        prev = self.previous()
        curr = self.peek()
        operators = self._OPERATORS

        # Try two-character operator first
        if prev and curr:
            double_char = prev + curr
            if double_char in operators:
                self.advance()
                return self.token(operators[double_char], double_char)

        # Try single-character operator
        if prev in operators:
            return self.token(operators[prev], prev)

        if prev is None:
            raise self.unexpected_none()
        raise self.unexpected_character(prev)

    def skip_comment(self):
        self.match("EM")  # Consume "EM"
        code = self.code
        current = self.current
        end = self.end

        # Fast forward to newline
        while current < end and code[current] != "\n":
            current += 1
        self.current = current

        if current < end and code[current] == "\n":
            self.advance()
            self.eol()

    def skip_comment_block(self):
        self.match("EM_BLOCK")  # Consume "EM_BLOCK"
        match = self.match

        while not match("END_REM"):
            self.skip_comment()

        if self.peek() == "\n":
            self.advance()
            self.eol()

    def token(self, tok_type, value=""):
        return Token(tok_type, value, self.line, self.column())

    def eol(self):
        self.line += 1
        self.line_start = self.current
        return Token(Tok.EOL)

    def scan_token(self, previous):
        char = self.advance()

        # Handle empty lines
        if char == "\n" and self.start == self.line_start:
            self.eol()
            return None

        if char == "\n":
            return self.eol()

        # Context-dependent parsing based on previous token
        if previous:
            prev_type = previous.type
            if prev_type in self._STRING_TOKEN_TYPES:
                return self.string()
            elif prev_type == Tok.RD_KBD:
                return self.kbd_platform()
            elif prev_type == Tok.RD_KBD_PLATFORM:
                return self.kbd_language()

        # Character type dispatch
        if self.is_operator(char):
            return self.operator()
        elif self.is_digit(char):
            return self.number()
        elif self.is_comment_block(char):
            return self.skip_comment_block()
        elif self.is_comment(char):
            return self.skip_comment()
        elif self.is_alpha(char):
            return self.identifier()
        elif char and char.isspace():
            return None

        raise self.unexpected_character(char)
