from pprint import pprint
from termcolor import colored

from tokenizer import Tokenizer, Tokens, Token, TokenType, TRUTHY, TYPES
from utils import RunType, FutureImplementation
from papervars import Int, Float, String, Bool

import error


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

                    # Is raw int
                    if self.tokens.next(4).get().token == TokenType.INT_DATA:
                        get_input = input(self.access_item(4))
                        self.vars_in_mem[name] = Int(get_input)

                # Set int as another int (redefinition)
                elif self.tokens.next(3).get().token == TokenType.VAR_NAME:
                    var = self.vars_in_mem[self.remove_dot(self.access_item(3))].data
                    self.vars_in_mem[name] = Int(var)

    def parse_float(self):
        if self.tokens.next().get().token == TokenType.VAR_NAME:
            name = self.remove_dot(self.access_item(1))
            if self.tokens.next(2).get().token == TokenType.EQUAL:

                # Set a raw float
                if self.tokens.next(3).get().token == TokenType.FLOAT_DATA:
                    self.vars_in_mem[name] = Float(self.access_item(3))

                # Get value from input, set as float
                elif self.tokens.next(3).get().token == TokenType.INPUT:

                    # Is raw float
                    if self.tokens.next(4).get().token == TokenType.STRING_DATA:
                        get_input = input(self.access_item(4))
                        self.vars_in_mem[name] = Float(get_input)

                # Set int as another float (redefinition)
                elif self.tokens.next(3).get().token == TokenType.VAR_NAME:
                    var = self.vars_in_mem[self.remove_dot(self.access_item(3))].data
                    self.vars_in_mem[name] = Float(var)

    def parse_bool(self):
        if self.tokens.next().get().token == TokenType.VAR_NAME:
            name = self.remove_dot(self.access_item(1))
            if self.tokens.next(2).get().token == TokenType.EQUAL:

                # Set a raw bool
                bool_val = self.tokens.next(3).get().token
                if bool_val == TokenType.TRUE or bool_val == TokenType.FALSE:
                    bool_data = True if self.access_item(3) in TRUTHY else False
                    self.vars_in_mem[name] = Bool(bool_data)

                # Get value from input, set as bool
                elif self.tokens.next(3).get().token == TokenType.INPUT:

                    # Is raw bool
                    bool_val = self.tokens.next(4).get().token
                    if self.tokens.next(4).get().token == TokenType.STRING_DATA:
                        get_input = input(self.access_item(4))
                        bool_data = True if get_input in TRUTHY else False
                        self.vars_in_mem[name] = Bool(bool_data)

                # Set int as another bool (redefinition)
                elif self.tokens.next(3).get().token == TokenType.VAR_NAME:
                    var = self.vars_in_mem[self.remove_dot(self.access_item(3))].data
                    bool_data = True if var in TRUTHY else False
                    self.vars_in_mem[name] = Bool(bool_val)

    def parse_func(self):
        if self.tokens.next().get().token == TokenType.VAR_NAME:
            if self.tokens.next(2).get().token == TokenType.LEFT_PAREN:
                args = []
                index = 3
                should_parse_args = True
                while should_parse_args:
                    if (type_ := self.tokens.next(index).get().token) in TYPES:
                        if self.tokens.next(index + 1).get().token == TokenType.COLON:
                            if self.tokens.next(index + 2).get().token == TokenType.VAR_NAME:
                                args.append({"type": type_, "name": self.access_item(index + 2)})
                            else:
                                error.PaperSyntaxError()
                        else:
                            error.PaperSyntaxError()
                    if self.tokens.next(index + 3).get().token == TokenType.RIGHT_PAREN:
                        break
                    index += 3

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
