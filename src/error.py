from termcolor import colored


class PaperError:
    def __init__(self, message, string):
        self.message = message
        self.string = string
        self.raise_error()

    def __str__(self):
        return self.string

    def raise_error(self):
        print(colored(self.message, "red"))
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
        super().__init__(PaperTypeError.message, PaperTypeError.string)


class PaperSyntaxError(PaperError):
    message = "Syntax error"
    string = "PaperSyntaxError"

    def __init__(self):
        super().__init__(PaperSyntaxError.message, PaperSyntaxError.string)


class PaperArgumentError(PaperError):
    message = "Argument error"
    string = "PaperArgumentError"

    def __init__(self):
        super().__init__(PaperArgumentError.message, PaperArgumentError.string)


class PaperWarning:
    def __init__(self, message, string):
        self.message = message
        self.string = string
        self.show_warning()

    def __str__(self):
        return self.string

    def show_warning(self):
        print(colored(self.message, "yellow"))


class PaperNoneTokenWarning(PaperWarning):
    message = "None type warning"
    string = "PaperNoneTokenWarning"

    def __init__(self):
        super().__init__(PaperNoneTokenWarning.message, PaperNoneTokenWarning.string)
