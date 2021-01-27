import error


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
        try:
            super().__init__(int(data), "Int")
        except:
            error.PaperTypeError()


class Float(Var):
    def __init__(self, data):
        try:
            super().__init__(float(data), "Float")
        except:
            error.PaperTypeError()


class Bool(Var):
    def __init__(self, data):
        try:
            super().__init__(bool(data), "Bool")
        except:
            error.PaperTypeError()
