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
