import shlex
import re

from utils import OrderedEnum
import error


NUMBER_INT = re.compile('\d*')
NUMBER_FLOAT = re.compile('\d*\.\d*')


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
