from enum import Enum
import shlex
import re
from pprint import pprint
from termcolor import colored
from optparse import OptionParser


VERSION = 0.1

NUMBER_INT = re.compile('\d*')
NUMBER_FLOAT = re.compile('\d*\.\d*')


class FutureImplementation:
    def __init__(self, version_expected: int = 0):
        self.message = f"FutureImplementation"
        if version_expected != 0:
            self.message = f"{self.message} {version_expected}"

    def __repr__(self):
        return colored(self.message, "red")


class OrderedEnum(Enum):
    """Refrence https://docs.python.org/3/library/enum.html#orderedenum"""

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Var:
    def __init__(self, data, name):
        self.data = data
        self.name = name

    def __repr__(self):
        return f"{self.name}({self.data})"


class String(Var):
    def __init__(self, data):
        super().__init__(data, "String")

    def __repr__(self):
        return f"String(\"{self.data}\")"


class Int(Var):
    def __init__(self, data):
        super().__init__(int(data), "Int")


class Float(Var):
    def __init__(self, data):
        super().__init__(float(data), "Float")


class Bool(Var):
    def __init__(self, data):
        super().__init__(float(data), "Bool")


class PaperError:
    def __init__(self, message, string):
        self.message = message
        self.string = string

    def __str__(self):
        return self.string

    def raise_error(self):
        print(self.message)
        exit()


class PaperValueError(PaperError):
    message = "Value error"
    string = "PaperValueError"

    def __init__(self):
        super().__init__(PaperValueError.message, PaperValueError.string)


class PaperTypeError(PaperError):
    message = "Type error"
    string = "PaperTypeError"

    def __init__(self):
        super().__init__(PaperValueError.message, PaperValueError.string)


class PaperSyntaxError(PaperError):
    message = "Syntax error"
    string = "PaperSyntaxError"

    def __init__(self):
        super().__init__(PaperValueError.message, PaperValueError.string)


class TokenType(OrderedEnum):
    NONE = 0
    PRINT = 1
    INPUT = 2
    STRING = 3
    INT = 4
    EQUAL = 5
    STRING_DATA = 6
    INT_DATA = 7
    VAR_NAME = 8
    FLOAT = 9
    BOOL = 10
    FALSE = 11
    TRUE = 12
    FUNC = 13
    RETURN = 14
    BREAK = 15
    STOP = 16


class RunType(OrderedEnum):
    NORMAL = 0
    VERBOSE = 1
    DEBUG = 2
    STEP_THROUGH_DEBUG = 3


class Token:
    def __init__(self, token: TokenType):
        self.token = TokenType(token)

    def __repr__(self):
        return f"Token({self.token})"


class Tokens:
    def __init__(self, tokens: list = [], index: int = 0):
        self.tokens = tokens
        self.index = index

    def get(self):
        return self.tokens[self.index]

    def get_type(self):
        return self.tokens[self.index].token

    def add(self, token: TokenType):
        self.tokens.append(token)

    def next(self, amount: int = 1):
        return Tokens(self.tokens, self.index + amount)

    def last(self, amount: int = 1):
        return Tokens(self.tokens, self.index - amount)

    def __repr__(self):
        return f"Tokens(tokens=[\"{self.tokens[self.index]}\", ...])"


class Tokenizer:
    def __init__(self, filename: str):
        self.filename = filename
        self.items: list = []
        self.tokens = Tokens()
        self.lines = self.get_file_lines()

    def get_file_lines(self):
        with open(self.filename) as file:
            return file.readlines()

    def get_token_type(self, item: str):
        if item == "print":
            token = Token(TokenType.PRINT)

        elif item == "input":
            token = Token(TokenType.INPUT)

        elif item == "string":
            token = Token(TokenType.STRING)

        elif item == "int":
            token = Token(TokenType.INT)

        elif item == "float":
            token = Token(TokenType.FLOAT)

        elif item == "bool":
            token = Token(TokenType.BOOL)

        elif item == "True":
            token = Token(TokenType.TRUE)

        elif item == "False":
            token = Token(TokenType.FALSE)

        elif item == "func":
            token = Token(TokenType.FUNC)

        elif item == "return":
            token = Token(TokenType.RETURN)

        elif item == "break":
            token = Token(TokenType.BREAK)

        elif item == "stop":
            token = Token(TokenType.STOP)

        elif item == "=":
            token = Token(TokenType.EQUAL)

        elif item[0] == "\"" and item[-1] == item[0]:
            token = Token(TokenType.STRING_DATA)

        elif NUMBER_INT.match(item).group(0) != "":
            token = Token(TokenType.INT_DATA)

        elif item[0] == ".":
            token = Token(TokenType.VAR_NAME)

        else:
            token = Token(TokenType.NONE)

        return token

    def tokenize_each_line(self):
        for line in self.lines:
            items = shlex.shlex(line, punctuation_chars=True)
            self.tokenize_each_item(items)

    def tokenize_each_item(self, items: list):
        for item in items:
            self.items.append(item)
            token = self.get_token_type(item)
            self.tokens.add(token)

    def tokenize(self):
        self.tokenize_each_line()

    def __repr__(self):
        return f"Tokenizer(items=[\"{self.items[0]}\", ...], \
            lines=[\"{self.lines[0].strip()}\", ...], tokens=Tokens())"


class Parser:
    def __init__(self, tokens: Tokens, items: list, mode: RunType = RunType.NORMAL):
        self.tokens = tokens
        self.items = items
        self.vars_in_mem: dict = {}

        self.mode = mode

    def remove_quotes(self, string: str):
        return string[1:-1]

    def remove_dot(self, var: str):
        return var[1:]

    def access_item(self, num: int):
        return self.items[self.tokens.index + num]

    def parse_print(self):
        # Print a raw string
        if self.tokens.next().get().token == TokenType.STRING_DATA:
            print(self.remove_quotes(self.access_item(1)))

        # Print var
        if self.tokens.next().get().token == TokenType.VAR_NAME:
            print(self.vars_in_mem[self.remove_dot(self.access_item(1))].data)

    def parse_string(self):
        if self.tokens.next().get().token == TokenType.VAR_NAME:
            name = self.remove_dot(self.access_item(1))
            if self.tokens.next(2).get().token == TokenType.EQUAL:

                # Set a raw string
                if self.tokens.next(3).get().token == TokenType.STRING_DATA:
                    self.vars_in_mem[name] = String(self.access_item(3))

                # Get value from input, set as string
                elif self.tokens.next(3).get().token == TokenType.INPUT:

                    # Is raw string
                    if self.tokens.next(4).get().token == TokenType.STRING_DATA:
                        get_input = input(self.remove_quotes(self.access_item(4)))
                        self.vars_in_mem[name] = String(get_input)

                    # Is var
                    elif self.tokens.next(4).get().token == TokenType.VAR_NAME:
                        get_input = input(
                            self.vars_in_mem[self.remove_dot(self.access_item(4))].data
                        )
                        self.vars_in_mem[name] = String(get_input)

                # Set int as another int (redefinition)
                elif self.tokens.next(3).get().token == TokenType.VAR_NAME:
                    var = self.vars_in_mem[self.remove_dot(self.access_item(3))].data
                    self.vars_in_mem[name] = String(var)

    def parse_int(self):
        if self.tokens.next().get().token == TokenType.VAR_NAME:
            name = self.remove_dot(self.access_item(1))
            if self.tokens.next(2).get().token == TokenType.EQUAL:

                # Set a raw int
                if self.tokens.next(3).get().token == TokenType.INT_DATA:
                    self.vars_in_mem[name] = Int(self.access_item(3))

                # Get value from input, set as int
                elif self.tokens.next(3).get().token == TokenType.INPUT:

                    # Is raw string
                    if self.tokens.next(4).get().token == TokenType.INT_DATA:
                        get_input = input(self.access_item(4))
                        self.vars_in_mem[name] = Int(get_input)

                # Set int as another int (redefinition)
                elif self.tokens.next(3).get().token == TokenType.VAR_NAME:
                    var = self.vars_in_mem[self.remove_dot(self.access_item(3))].data
                    self.vars_in_mem[name] = Int(var)

    def parse_float(self):
        print(FutureImplementation(0.2))

    def parse_bool(self):
        print(FutureImplementation(0.2))

    def parse_func(self):
        print(FutureImplementation())

    def parse_stop(self):
        exit()

    def parse_item(self):
        token = self.tokens.get().token

        # Starts with print
        if token == TokenType.PRINT:
            self.parse_print()

        # Starts with string
        elif token == TokenType.STRING:
            self.parse_string()

        # Starts with int
        elif token == TokenType.INT:
            self.parse_int()

        # Starts with float
        elif token == TokenType.FLOAT:
            self.parse_float()

        # Starts with bool
        elif token == TokenType.BOOL:
            self.parse_bool()

        # Starts with func
        elif token == TokenType.FUNC:
            self.parse_func()

        # Starts with stop
        elif token == TokenType.STOP:
            self.parse_stop()

        self.tokens.index += 1

    def show_token(self, index: int):
        print(colored(self.tokens.tokens[index].token, "green"))

    def show_mem(self):
        pprint(self.vars_in_mem)

    def parse(self):
        index = 0
        while index < len(self.tokens.tokens):

            if self.mode >= RunType.VERBOSE:
                self.show_token(index)

            if self.mode >= RunType.STEP_THROUGH_DEBUG:
                self.show_mem()

            self.parse_item()
            index += 1

        if self.mode >= RunType.DEBUG and self.mode is not RunType.STEP_THROUGH_DEBUG:
            self.show_mem()

    def __repr__(self):
        return f"Parser(mode={self.mode}, tokens=Tokens())"


def option_parse():
    parser = OptionParser()
    parser.add_option(
        "-m",
        "--mode",
        dest="mode",
        default=False,
        help="The mode of running",
    )
    options, args = parser.parse_args()
    filename = args[0]
    mode = RunType(int(options.mode)) if options.mode else RunType.NORMAL
    return filename, mode


if __name__ == "__main__":
    filename, mode = option_parse()
    tokenizer = Tokenizer(filename)
    tokenizer.tokenize()

    parser = Parser(tokenizer.tokens, tokenizer.items, mode=mode)
    parser.parse()
