from .lexer import Tok, Token


# EXPRESSIONS

class Expr:
    __slots__ = ()

    def __eq__(self, other):
        return repr(self) == repr(other)


class Binary(Expr):
    __slots__ = ('left', 'operator', 'right')

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return "EXPR(" + repr(self.left) + ", " + self.operator.value + ", " + repr(self.right) + ")"


class Unary(Expr):
    __slots__ = ('operator', 'right')

    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __repr__(self):
        return "EXPR(" + self.operator.value + ", " + repr(self.right) + ")"


class Literal(Expr):
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "LITERAL(" + str(self.value) + ")"


class Grouping(Expr):
    __slots__ = ('expression',)

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "GROUP(" + repr(self.expression) + ")"


class Variable(Expr):
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "VAR(" + str(self.name) + ")"


class Call(Expr):
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "CALL(" + str(self.name) + ")"


class Assign(Expr):
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "ASSIGN(" + str(self.name) + ", " + repr(self.value) + ")"


# STATEMENTS

class Stmt:
    __slots__ = ()

    def __eq__(self, other):
        return repr(self) == repr(other)


class KeyPressStmt(Stmt):
    __slots__ = ('keys', 'hold', 'release')

    def __init__(self, keys, hold=False, release=False):
        self.keys = keys
        self.hold = hold
        self.release = release

    def __repr__(self):
        return "KEYPRESS(" + str(self.keys) + ", HOLD=" + str(self.hold) + ", RELEASE=" + str(self.release) + ")"


class VarStmt(Stmt):
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "VAR_DECL(" + str(self.name) + ", " + repr(self.value) + ")"


class DelayStmt(Stmt):
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "DELAY(" + repr(self.value) + ")"


class StringStmt(Stmt):
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "PRINT_STR(" + repr(self.value) + ")"


class StringLnStmt(Stmt):
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "PRINT_STRLN(" + repr(self.value) + ")"


class KbdStmt(Stmt):
    __slots__ = ('platform', 'language')

    def __init__(self, platform, language):
        self.platform = platform
        self.language = language

    def __repr__(self):
        return "KBD(" + str(self.platform) + ", " + str(self.language) + ")"


class IfStmt(Stmt):
    __slots__ = ('condition', 'then_block', 'else_if_blocks', 'else_block')

    def __init__(self, condition, then_block, else_if_blocks=None, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_if_blocks = else_if_blocks if else_if_blocks is not None else []
        self.else_block = else_block if else_block is not None else []

    def __repr__(self):
        return "IF(" + repr(self.condition) + ", " + repr(self.then_block) + ", " + repr(self.else_if_blocks) + ", " + repr(self.else_block) + ")"


class WhileStmt(Stmt):
    __slots__ = ('condition', 'body')

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return "WHILE(" + repr(self.condition) + ", " + repr(self.body) + ")"


class ExpressionStmt(Stmt):
    __slots__ = ('expression',)

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "EXPR_STMT(" + repr(self.expression) + ")"


class FunctionStmt(Stmt):
    __slots__ = ('name', 'body')

    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return "FUNCTION(" + str(self.name) + ", " + repr(self.body) + ")"


class RandomCharStmt(Stmt):
    __slots__ = ('type',)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return "RANDOM_CHAR(" + str(self.type) + ")"


class RandomCharFromStmt(Stmt):
    __slots__ = ('type', 'value')

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "RANDOM_CHAR_FROM(" + str(self.type) + ", " + repr(self.value) + ")"


class WaitForButtonPressStmt(Stmt):
    __slots__ = ()

    def __repr__(self):
        return "WAIT_FOR_BUTTON_PRESS()"


class ButtonDefStmt(Stmt):
    __slots__ = ('body',)

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return "BUTTON_DEF(" + repr(self.body) + ")"


class LedGStmt(Stmt):
    __slots__ = ()

    def __repr__(self):
        return "LED_G()"


class LedRStmt(Stmt):
    __slots__ = ()

    def __repr__(self):
        return "LED_R()"


class LedBStmt(Stmt):
    __slots__ = ()

    def __repr__(self):
        return "LED_B()"


class LedOffStmt(Stmt):
    __slots__ = ()

    def __repr__(self):
        return "LED_OFF()"


class Parser:
    __slots__ = ('tokens', 'current', '_len_tokens')

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self._len_tokens = len(tokens)

    def parse(self):
        statements = []
        append = statements.append
        is_at_end = self.is_at_end
        declaration = self.declaration

        while not is_at_end():
            append(declaration())
        return statements

    def declaration(self):
        if self.match(Tok.VAR):
            return self.var_stmt()
        return self.statement()

    def statement(self):
        match = self.match

        if match(Tok.VAR):
            return self.var_stmt()
        elif match(Tok.PRINTSTRING):
            return self.string_stmt()
        elif match(Tok.PRINTSTRINGLN):
            return self.stringln_stmt()
        elif match(Tok.RD_KBD):
            return self.kbd_stmt()
        elif match(Tok.DELAY):
            return self.delay_stmt()
        elif match(Tok.IF):
            return self.if_stmt()
        elif match(Tok.WHILE):
            return self.while_stmt()
        elif match(Tok.FUNCTION):
            return self.function_stmt()
        elif match(Tok.KEYPRESS):
            return self.keypress_stmt()
        elif match(Tok.HOLD, Tok.RELEASE):
            return self.keypress_stmt()
        elif match(Tok.RANDOM_CHAR):
            return self.random_char_stmt()
        elif match(Tok.RANDOM_CHAR_FROM):
            return self.random_char_from_stmt()
        elif match(Tok.WAIT_FOR_BUTTON_PRESS):
            return self.wait_for_button_press_stmt()
        elif match(Tok.LED_G):
            return self.led_g_stmt()
        elif match(Tok.LED_R):
            return self.led_r_stmt()
        elif match(Tok.LED_B):
            return self.led_b_stmt()
        elif match(Tok.LED_OFF):
            return self.led_off_stmt()
        elif match(Tok.BUTTON_DEF):
            return self.button_def_stmt()
        elif match(Tok.ATTACKMODE):
            return self.skip_attackmode_stmt()

        return self.expression_stmt()

    def keypress_stmt(self):
        previous = self.previous()
        prev_type = previous.type
        hold = prev_type == Tok.HOLD
        release = prev_type == Tok.RELEASE
        keys = [] if (hold or release) else [previous]

        match = self.match
        prev = self.previous
        while match(Tok.KEYPRESS):
            keys.append(prev())

        self.consume_termination("Expected a line break after a keypress")
        return KeyPressStmt(keys, hold, release)

    def var_stmt(self):
        name = self.consume(Tok.IDENTIFIER, "Expected an identifier after VAR")
        self.consume(Tok.ASSIGN, "Expected '=' after identifier")
        initializer = self.expression()
        self.consume_termination("Expected a line break after variable initialization")
        return VarStmt(name, initializer)

    def string_stmt(self):
        value = self.consume(Tok.STRING, "Expected a string after STRING")
        self.consume_termination("Expected a line break after a string")
        return StringStmt(Literal(value.value))

    def stringln_stmt(self):
        value = self.consume(Tok.STRING, "Expected a string after STRINGLN")
        self.consume_termination("Expected a line break after a string")
        return StringLnStmt(Literal(value.value))

    def kbd_stmt(self):
        platform = self.consume(Tok.RD_KBD_PLATFORM, "Expected a platform after RD_KBD")
        language = self.consume(Tok.RD_KBD_LANGUAGE, "Expected a language after RD_KBD_PLATFORM")
        self.consume_termination("Expected a line break after a keyboard statement")
        return KbdStmt(platform, language)

    def delay_stmt(self):
        value = self.expression()
        self.consume_termination("Expected a line break after a delay duration")
        return DelayStmt(value)

    def if_stmt(self):
        condition = self.expression()
        self.consume(Tok.THEN, "Expected 'THEN'")
        self.consume(Tok.EOL, "Expected a line break after 'THEN'")
        then_block = self.block()

        match = self.match
        else_if_blocks = []
        while match(Tok.ELSE_IF):
            else_if_condition = self.expression()
            self.consume(Tok.THEN, "Expected 'THEN' after 'ELSE IF'")
            self.consume(Tok.EOL, "Expected a line break after 'THEN'")
            else_if_block = self.block()
            else_if_blocks.append(IfStmt(else_if_condition, else_if_block))

        else_block = []
        if match(Tok.ELSE):
            self.consume(Tok.EOL, "Expected a line break after 'ELSE'")
            else_block = self.block()

        self.consume(Tok.END_IF, "Expected 'END_IF'")
        self.consume_termination("Expected a line break after 'END_IF'")
        return IfStmt(condition, then_block, else_if_blocks, else_block)

    def while_stmt(self):
        condition = self.expression()
        self.consume(Tok.EOL, "Expected a line break after the condition")
        body = self.block()
        self.consume(Tok.END_WHILE, "Expected 'END_WHILE'")
        self.consume_termination("Expected a line break after 'END_WHILE'")
        return WhileStmt(condition, body)

    def function_stmt(self):
        name = self.consume(Tok.IDENTIFIER, "Expected an identifier after 'FUNCTION'")
        self.consume(Tok.LPAREN, "Expected '(' after function name")
        self.consume(Tok.RPAREN, "Expected ')' after function parameters")
        self.consume(Tok.EOL, "Expected a line break after the function parameters")
        body = self.block()
        self.consume(Tok.END_FUNCTION, "Expected 'END_FUNCTION'")
        self.consume_termination("Expected a line break after 'END_FUNCTION'")
        return FunctionStmt(name, body)

    def random_char_stmt(self):
        type_tok = self.previous()
        self.consume_termination("Expected a line break after '" + type_tok.value + "'")
        return RandomCharStmt(type_tok)

    def random_char_from_stmt(self):
        type_tok = self.previous()
        value = self.consume(Tok.STRING, "Expected a string after 'RANDOM_CHAR_FROM'")
        self.consume_termination("Expected a line break after '" + type_tok.value + "'")
        return RandomCharFromStmt(type_tok, Literal(value.value))

    def wait_for_button_press_stmt(self):
        self.consume_termination("Expected a line break after WAIT_FOR_BUTTON_PRESS")
        return WaitForButtonPressStmt()

    def button_def_stmt(self):
        self.consume(Tok.EOL, "Expected a line break after BUTTON_DEF")
        body = self.block()
        self.consume(Tok.END_BUTTON, "Expected END_BUTTON")
        self.consume_termination("Expected a line break after END_BUTTON")
        return ButtonDefStmt(body)

    def led_g_stmt(self):
        self.consume_termination("Expected a line break after LED_G")
        return LedGStmt()

    def led_r_stmt(self):
        self.consume_termination("Expected a line break after LED_R")
        return LedRStmt()

    def led_b_stmt(self):
        self.consume_termination("Expected a line break after LED_B")
        return LedBStmt()

    def led_off_stmt(self):
        self.consume_termination("Expected a line break after LED_OFF")
        return LedOffStmt()

    def skip_attackmode_stmt(self):
        check = self.check
        is_at_end = self.is_at_end
        advance = self.advance

        while not check(Tok.EOL) and not is_at_end():
            advance()
        self.consume_termination("Expected a line break after ATTACKMODE MODE")
        return None

    def block(self):
        statements = []
        append = statements.append
        check = self.check
        is_at_end = self.is_at_end
        statement = self.statement

        while (not check(Tok.END_IF) and not check(Tok.ELSE_IF) and 
               not check(Tok.ELSE) and not check(Tok.END_WHILE) and 
               not check(Tok.END_FUNCTION) and not check(Tok.END_BUTTON) and 
               not is_at_end()):
            append(statement())
        return statements

    def expression_stmt(self):
        expr = self.expression()
        self.consume_termination("Expected a line break after an expression")
        return ExpressionStmt(expr)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.logical()
        if self.match(Tok.ASSIGN):
            value = self.assignment()
            if type(expr) is Variable:
                return Assign(expr.name, value)
        return expr

    def logical(self):
        match = self.match
        previous = self.previous
        equality = self.equality

        expr = equality()
        while match(Tok.OP_AND, Tok.OP_OR):
            operator = previous()
            right = equality()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self):
        match = self.match
        previous = self.previous
        comparison = self.comparison

        expr = comparison()
        while match(Tok.OP_EQUAL, Tok.OP_NOT_EQUAL):
            operator = previous()
            right = comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        match = self.match
        previous = self.previous
        term = self.term

        expr = term()
        while match(Tok.OP_GREATER, Tok.OP_LESS, Tok.OP_GREATER_EQUAL, Tok.OP_LESS_EQUAL):
            operator = previous()
            right = term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        match = self.match
        previous = self.previous
        factor = self.factor

        expr = factor()
        while match(Tok.OP_PLUS, Tok.OP_MINUS):
            operator = previous()
            right = factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        match = self.match
        previous = self.previous
        unary = self.unary

        expr = unary()
        while match(Tok.OP_MULTIPLY, Tok.OP_DIVIDE, Tok.OP_MODULO):
            operator = previous()
            right = unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        match = self.match
        previous = self.previous

        if match(Tok.OP_NOT, Tok.OP_MINUS):
            operator = previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call()

    def call(self):
        expr = self.primary()
        name = self.previous()
        if self.match(Tok.LPAREN):
            self.consume(Tok.RPAREN, "Expected ')' after function call")
            return Call(name)
        return expr

    def primary(self):
        match = self.match
        previous = self.previous

        if match(Tok.FALSE):
            return Literal(False)
        if match(Tok.TRUE):
            return Literal(True)
        if match(Tok.NUMBER):
            return Literal(previous().value)
        if match(Tok.STRING):
            return Literal(previous().value)
        if match(Tok.IDENTIFIER):
            return Variable(previous())
        if match(Tok.LPAREN):
            expr = self.expression()
            self.consume(Tok.RPAREN, "Expected ')' after expression")
            return Grouping(expr)

        raise self.error(self.peek(), "Expected expression")

    def error(self, token, message):
        return SyntaxError(
            "Unexpected token " + str(token.type) + " at line " + 
            str(token.line) + ", column " + str(token.column) + ": " + message
        )

    def match(self, *types):
        check = self.check
        advance = self.advance

        for tok_type in types:
            if check(tok_type):
                advance()
                return True
        return False

    def check(self, tok_type):
        current = self.current
        if current >= self._len_tokens:
            return False
        return self.tokens[current].type == tok_type

    def advance(self):
        current = self.current
        if current < self._len_tokens:
            self.current = current + 1
        return self.tokens[current]

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def is_at_end(self):
        current = self.current
        return current >= self._len_tokens or self.tokens[current].type == Tok.EOF

    def consume(self, tok_type, message):
        if self.check(tok_type):
            return self.advance()
        peek = self.peek()
        raise SyntaxError(message, peek.line, peek.column)

    def consume_termination(self, message):
        if self.is_at_end() or self.check(Tok.EOL):
            return self.advance()
        peek = self.peek()
        raise SyntaxError(message, peek.line, peek.column)

    def synchronize(self):
        advance = self.advance
        is_at_end = self.is_at_end
        previous = self.previous
        peek = self.peek

        advance()
        while not is_at_end():
            if previous().type == Tok.EOL:
                return

            peek_type = peek().type
            if (peek_type == Tok.IF or peek_type == Tok.WHILE or 
                peek_type == Tok.PRINTSTRING or peek_type == Tok.PRINTSTRINGLN or 
                peek_type == Tok.DELAY or peek_type == Tok.FUNCTION or 
                peek_type == Tok.RETURN or peek_type == Tok.KEYPRESS):
                return
            advance()
