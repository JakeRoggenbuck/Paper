from enum import Enum
import shlex


class TokenType(Enum):
    NONE = 0
    PRINT = 1
    INPUT = 2
    STRING = 3
    INT = 4
    EQUAL = 5
    STRING_DATA = 6
    VAR_NAME = 7


class Token:
    def __init__(self, token: int):
        self.token = TokenType(token)


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
        return f"tokens[{self.index}] = TokenType({self.get()})"


class Parser:
    def __init__(self):
        self.items = []
        self.tokens = Tokens()
        self.lines = self.get_file_lines()

    def get_file_lines(self):
        with open("file.txt") as file:
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

        elif item == "=":
            token = Token(TokenType.EQUAL)

        elif item[0] == "\"" and item[-1] == item[0]:
            token = Token(TokenType.STRING_DATA)

        elif item[0] == ".":
            token = Token(TokenType.VAR_NAME)

        else:
            token = Token(TokenType.NONE)

        return token

    def parse_each_line(self):
        for line in self.lines:
            items = shlex.shlex(line, punctuation_chars=True)
            self.parse_each_item(items)

    def parse_each_item(self, items: list):
        for item in items:
            self.items.append(item)
            token = self.get_token_type(item)
            self.tokens.add(token)

    def parse(self):
        self.parse_each_line()


class Runner:
    def __init__(self, tokens: list, items: list):
        self.tokens = tokens
        self.items = items

    def run(self):
        index = 0
        while index < len(self.tokens.tokens):
            token = self.tokens.tokens[index].token
            data = self.items[index]
            print(f"{token}:\t{data}")
            index += 1


if __name__ == "__main__":
    parser = Parser()
    parser.parse()
    runner = Runner(parser.tokens, parser.items)
    runner.run()
