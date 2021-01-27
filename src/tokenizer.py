import shlex
import re

from utils import OrderedEnum
import error


NUMBER_INT = re.compile('^\d*$')
NUMBER_FLOAT = re.compile('^\d*\.\d*$')

TRUTHY = ["TRUE", "True", "T", "1"]


class TokenType(OrderedEnum):
    NONE = 0
    PRINT = 1
    INPUT = 2
    STRING = 3
    INT = 4
    EQUAL = 5
    STRING_DATA = 6
    INT_DATA = 7
    FLOAT_DATA = 8
    VAR_NAME = 9
    FLOAT = 10
    BOOL = 11
    FALSE = 12
    TRUE = 13
    FUNC = 14
    RETURN = 15
    BREAK = 16
    STOP = 17
    TERN = 18
    IF = 19
    ELSIF = 20
    ELSE = 21
    WHILE = 22
    UNTIL = 23
    NOT = 24
    RIGHT_PAREN = 25
    LEFT_PAREN = 26
    COLON = 27
    SEMI_COLON = 28
    RIGHT_SQUIGGLY_BRACKET = 29
    LEFT_SQUIGGLY_BRACKET = 30
    RIGHT_SQUARE_BRACKET = 31
    LEFT_SQUARE_BRACKET = 32


TYPES = [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING]


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

        elif item == "?":
            token = Token(TokenType.TERN)

        elif item == "if":
            token = Token(TokenType.IF)

        elif item == "elsif":
            token = Token(TokenType.ELSIF)

        elif item == "else":
            token = Token(TokenType.ELSE)

        elif item == "while":
            token = Token(TokenType.WHILE)

        elif item == "until":
            token = Token(TokenType.UNTIL)

        elif item == "not":
            token = Token(TokenType.NOT)

        elif item == ")":
            token = Token(TokenType.RIGHT_PAREN)

        elif item == "(":
            token = Token(TokenType.LEFT_PAREN)

        elif item == ":":
            token = Token(TokenType.COLON)

        elif item == ";":
            token = Token(TokenType.SEMI_COLON)

        elif item == "}":
            token = Token(TokenType.RIGHT_SQUIGGLY_BRACKET)

        elif item == "{":
            token = Token(TokenType.LEFT_SQUIGGLY_BRACKET)

        elif item == "]":
            token = Token(TokenType.RIGHT_SQUARE_BRACKET)

        elif item == "[":
            token = Token(TokenType.LEFT_SQUARE_BRACKET)

        elif item[0] == "\"" and item[-1] == item[0]:
            token = Token(TokenType.STRING_DATA)

        elif NUMBER_INT.match(item):
            token = Token(TokenType.INT_DATA)

        elif NUMBER_FLOAT.match(item):
            token = Token(TokenType.FLOAT_DATA)

        elif item[0] == ".":
            token = Token(TokenType.VAR_NAME)

        elif (
            item[0:2].upper() == "AS"[0] + "D"
            and item[-2].upper() == "ASD"[0]
            and item[-1].upper() == "M"
        ):
            error.PaperSyntaxError()

        else:
            token = Token(TokenType.NONE)
            error.PaperNoneTokenWarning()

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
