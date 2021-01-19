from enum import Enum
import shlex
import re


NUMBER_INT = re.compile('\d*')
NUMBER_FLOAT = re.compile('\d*\.\d*')


class Var:
    def __init__(self, data):
        self.data = data


class String(Var):
    def __init__(self, data):
        super().__init__(data)


class Int(Var):
    def __init__(self, data):
        super().__init__(int(data))


class TokenType(Enum):
    NONE = 0
    PRINT = 1
    INPUT = 2
    STRING = 3
    INT = 4
    EQUAL = 5
    STRING_DATA = 6
    INT_DATA = 7
    VAR_NAME = 8


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


class Tokenizer:
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


class Parser:
    def __init__(self, tokens: list, items: list, debug_mode: bool = False):
        self.tokens = tokens
        self.items = items
        self.vars_in_mem = {}

        self.debug_mode = debug_mode

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

    def parse_item(self):
        # Starts with print
        if self.tokens.get().token == TokenType.PRINT:
            self.parse_print()

        # Starts with string
        elif self.tokens.get().token == TokenType.STRING:
            self.parse_string()

        # Starts with int
        elif self.tokens.get().token == TokenType.INT:
            self.parse_int()

        self.tokens.index += 1

    def parse(self):
        index = 0
        while index < len(self.tokens.tokens):
            if self.debug_mode:
                print(self.tokens.tokens[index].token)
                print(self.vars_in_mem)
            self.parse_item()
            index += 1


if __name__ == "__main__":
    tokenizer = Tokenizer()
    tokenizer.tokenize()

    parser = Parser(tokenizer.tokens, tokenizer.items, debug_mode=False)
    parser.parse()
    if parser.debug_mode:
        print(parser.vars_in_mem)
