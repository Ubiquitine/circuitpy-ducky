import random
import time

from .button import Button
from .led import LED
from .keyboard import RasperDuckyKeyboard
from .parser import (
    KeyPressStmt,
    RandomCharStmt,
    VarStmt,
    Binary,
    Unary,
    Literal,
    Grouping,
    Variable,
    StringStmt,
    IfStmt,
    WhileStmt,
    Expr,
    Token,
    Tok,
    StringLnStmt,
    DelayStmt,
    FunctionStmt,
    Stmt,
    ExpressionStmt,
    Assign,
    Call,
    KbdStmt,
    RandomCharFromStmt,
    WaitForButtonPressStmt,
    ButtonDefStmt,
    LedGStmt,
    LedRStmt,
    LedBStmt,
    LedOffStmt,
)


class EvalTask:
    """Represents a task to evaluate an expression node"""
    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node


class BinaryOpTask:
    """Represents a binary operation waiting for its operands"""
    __slots__ = ('operator', 'left_value')

    def __init__(self, operator, left_value=None):
        self.operator = operator
        self.left_value = left_value


class UnaryOpTask:
    """Represents a unary operation waiting for its operand"""
    __slots__ = ('operator',)

    def __init__(self, operator):
        self.operator = operator


class AssignTask:
    """Represents an assignment waiting for its value"""
    __slots__ = ('var_name',)

    def __init__(self, var_name):
        self.var_name = var_name


class Interpreter:
    __slots__ = (
        'variables', 'functions', 'execution_stack', 'keyboard', 
        'button', 'led', 'eval_stack', 'value_stack', 'stmt_stack',
        'button_handler', 'button_wait_active', 'button_last_state',
        'button_ignore_until_released', '_BINARY_OPERATORS', '_UNARY_OPERATORS',
        '_RANDOM_CHAR_SETS'
    )

    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.execution_stack = []
        self.keyboard = RasperDuckyKeyboard("win", "us")
        self.button = Button()
        self.led = LED()
        self.eval_stack = []
        self.value_stack = []
        self.stmt_stack = []
        self.button_handler = None
        self.button_wait_active = False
        self.button_last_state = False
        self.button_ignore_until_released = False

        # Pre-cache operator lookups in instance for faster access
        self._BINARY_OPERATORS = {
            Tok.OP_PLUS: lambda l, r: l + r,
            Tok.OP_MINUS: lambda l, r: l - r,
            Tok.OP_MULTIPLY: lambda l, r: l * r,
            Tok.OP_DIVIDE: lambda l, r: l / r,
            Tok.OP_LESS: lambda l, r: l < r,
            Tok.OP_GREATER: lambda l, r: l > r,
            Tok.OP_LESS_EQUAL: lambda l, r: l <= r,
            Tok.OP_GREATER_EQUAL: lambda l, r: l >= r,
            Tok.OP_EQUAL: lambda l, r: l == r,
            Tok.OP_NOT_EQUAL: lambda l, r: l != r,
            Tok.OP_AND: lambda l, r: l and r,
            Tok.OP_OR: lambda l, r: l or r,
            Tok.OP_BITWISE_AND: lambda l, r: l & r,
            Tok.OP_BITWISE_OR: lambda l, r: l | r,
            Tok.OP_SHIFT_LEFT: lambda l, r: l << r,
            Tok.OP_SHIFT_RIGHT: lambda l, r: l >> r,
        }

        self._UNARY_OPERATORS = {
            Tok.OP_MINUS: lambda l: -l,
            Tok.OP_PLUS: lambda l: l,
            Tok.OP_NOT: lambda l: not l,
        }

        self._RANDOM_CHAR_SETS = {
            "RANDOM_LOWERCASE_LETTER": "abcdefghijklmnopqrstuvwxyz",
            "RANDOM_UPPERCASE_LETTER": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "RANDOM_LETTER": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "RANDOM_NUMBER": "0123456789",
            "RANDOM_SPECIAL": "!@#$%^&*()",
            "RANDOM_CHAR": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()",
        }

    def interpret(self, ast):
        """Stack-based interpreter to avoid recursion limits"""
        # Use slicing instead of list(reversed(...))
        stmt_stack = self.stmt_stack
        stmt_stack[:] = ast[::-1]

        # Cache method lookups
        pop_stmt = stmt_stack.pop
        poll = self._poll_button_handler
        execute = self._execute

        while stmt_stack:
            poll()
            node = pop_stmt()
            execute(node)

    def _execute(self, node):
        if node is None:
            return

        # Use type() for exact type checks (faster than isinstance in CircuitPython)
        node_type = type(node)

        if node_type is VarStmt:
            self._execute_var_declaration(node)
        elif node_type is IfStmt:
            self._execute_if_statement(node)
        elif node_type is WhileStmt:
            self._execute_while_statement(node)
        elif node_type is StringStmt:
            self._execute_print_string(node, False)
        elif node_type is StringLnStmt:
            self._execute_print_string(node, True)
        elif node_type is DelayStmt:
            self._execute_delay(node)
        elif node_type is Binary:
            self._evaluate(node)
        elif node_type is FunctionStmt:
            self.functions[node.name.value] = node.body
        elif node_type is KeyPressStmt:
            self._execute_keypress(node)
        elif node_type is KbdStmt:
            self.keyboard = RasperDuckyKeyboard(
                node.platform.value.lower(), node.language.value.lower()
            )
        elif node_type is ExpressionStmt:
            self._evaluate(node.expression)
        elif node_type is RandomCharStmt:
            self._execute_random_char(node)
        elif node_type is RandomCharFromStmt:
            self.keyboard.type_string(random.choice(str(node.value.value)))
        elif node_type is WaitForButtonPressStmt:
            self.button_wait_active = True
            self.button.wait_for_press()
            self.button_wait_active = False
            self.button_ignore_until_released = True
        elif node_type is LedGStmt:
            self.led.on((0, 255, 0))
        elif node_type is LedRStmt:
            self.led.on((255, 0, 0))
        elif node_type is LedBStmt:
            self.led.on((0, 0, 255))
        elif node_type is LedOffStmt:
            self.led.off()
        elif node_type is ButtonDefStmt:
            self.button_handler = node.body
        elif node_type is not Literal:
            raise RuntimeError("Unknown node type: " + str(node_type))

    def _execute_var_declaration(self, node):
        self.variables[node.name.value] = self._evaluate(node.value)

    def _execute_if_statement(self, node):
        if self._evaluate(node.condition):
            self._push_statements(node.then_block)
        else:
            for else_if in node.else_if_blocks:
                if self._evaluate(else_if.condition):
                    self._push_statements(else_if.then_block)
                    return
            self._push_statements(node.else_block)

    def _push_statements(self, statements):
        """Push statements onto execution stack in reverse order"""
        if statements:
            self.stmt_stack.extend(statements[::-1])

    def _execute_while_statement(self, node):
        if self._evaluate(node.condition):
            stmt_stack = self.stmt_stack
            stmt_stack.append(node)
            if node.body:
                stmt_stack.extend(node.body[::-1])

    def _substitute_variables(self, text):
        if not isinstance(text, str):
            return text

        # Avoid string concatenation in tight loops
        output = text
        variables = self.variables
        for full_name, val in variables.items():
            placeholder = "${" + full_name[1:] + "}"
            if placeholder in output:
                output = output.replace(placeholder, str(val))
        return output

    def _execute_print_string(self, node, newline):
        string = self._substitute_variables(node.value.value)
        self.execution_stack.append(string)

        keyboard = self.keyboard
        keyboard.type_string(string)
        if newline:
            keyboard.press_key("ENTER")
        keyboard.release_all()

    def _execute_delay(self, node):
        delay_val = self._evaluate(node.value)
        try:
            ms = int(delay_val)
        except:
            raise RuntimeError("DELAY expects a number, got: " + str(delay_val))
        time.sleep(ms * 0.001)

    def _execute_keypress(self, node):
        keyboard = self.keyboard
        if node.release:
            for key in node.keys:
                keyboard.release_key(key.value)
        else:
            for key in node.keys:
                keyboard.press_key(key.value)
            if not node.hold:
                keyboard.release_all()

    def _execute_random_char(self, node):
        node_type_value = node.type.value
        charsets = self._RANDOM_CHAR_SETS
        if node_type_value not in charsets:
            raise RuntimeError("Unknown random character set: " + node_type_value)
        self.keyboard.type_string(random.choice(charsets[node_type_value]))

    def _poll_button_handler(self):
        handler = self.button_handler
        if not handler:
            return
        if self.button_wait_active:
            return

        pressed = self.button.is_pressed()

        if self.button_ignore_until_released:
            if pressed:
                return
            self.button_ignore_until_released = False
            self.button_last_state = False
            return

        if pressed and not self.button_last_state:
            stmt_stack = self.stmt_stack
            for stmt in reversed(handler):
                stmt_stack.append(stmt)
        self.button_last_state = pressed

    def _evaluate(self, node):
        """Stack-based expression evaluator to avoid recursion limits"""
        eval_stack = self.eval_stack
        value_stack = self.value_stack

        eval_stack[:] = [EvalTask(node)]
        value_stack[:] = []

        # Cache lookups
        eval_pop = eval_stack.pop
        val_pop = value_stack.pop
        val_append = value_stack.append

        while eval_stack:
            task = eval_pop()
            task_type = type(task)

            if task_type is EvalTask:
                self._process_eval_task(task.node)
            elif task_type is BinaryOpTask:
                right = val_pop()
                left = val_pop()
                val_append(self._apply_operator(task.operator, left, right))
            elif task_type is UnaryOpTask:
                val_append(self._apply_unary_operator(task.operator, val_pop()))
            elif task_type is AssignTask:
                value = val_pop()
                self.variables[task.var_name] = value
                val_append(value)

        return val_pop() if value_stack else None

    def _process_eval_task(self, node):
        """Process an evaluation task by pushing work onto stacks"""
        node_type = type(node)
        eval_stack = self.eval_stack
        value_stack = self.value_stack

        if node_type is Literal:
            value_stack.append(int(node.value))
        elif node_type is Variable:
            name = node.name.value
            if name in self.variables:
                value_stack.append(self.variables[name])
            else:
                raise RuntimeError("Undefined variable: " + name)
        elif node_type is Binary:
            eval_stack.append(BinaryOpTask(node.operator))
            eval_stack.append(EvalTask(node.right))
            eval_stack.append(EvalTask(node.left))
        elif node_type is Unary:
            eval_stack.append(UnaryOpTask(node.operator))
            eval_stack.append(EvalTask(node.right))
        elif node_type is Grouping:
            eval_stack.append(EvalTask(node.expression))
        elif node_type is Assign:
            eval_stack.append(AssignTask(node.name.value))
            eval_stack.append(EvalTask(node.value))
        elif node_type is Call:
            self._push_statements(self.functions[node.name.value])
            value_stack.append(None)
        else:
            raise RuntimeError("Unknown node type for evaluation: " + str(node_type))

    def _apply_operator(self, operator, left, right):
        op_type = operator.type
        binary_ops = self._BINARY_OPERATORS
        if op_type in binary_ops:
            return binary_ops[op_type](left, right)
        elif operator.value == "=":
            return right
        else:
            raise RuntimeError("Unknown operator: " + operator.value)

    def _apply_unary_operator(self, operator, value):
        op_type = operator.type
        unary_ops = self._UNARY_OPERATORS
        if op_type in unary_ops:
            return unary_ops[op_type](value)
        else:
            raise RuntimeError("Unknown operator: " + operator.value)
