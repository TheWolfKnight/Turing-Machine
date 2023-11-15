
class Token(object):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class JKey(Token):
    def __init__(self, value: str):
        super().__init__(value)

    def get_type(self):
        return type(JKey)


class JInt(Token):
    def __init__(self, value: int):
        super().__init__(value)

    def get_type(self):
        return type(JInt)


class JFloat(Token):
    def __init__(self, value: float):
        super().__init__(value)

    def get_type(self):
        return type(JFloat)


class JBool(Token):
    def __init__(self, value: bool):
        super().__init__(value)

    def get_type(self):
        return type(JBool)


class JString(Token):
    def __init__(self, value: str):
        super().__init__(value)

    def get_type(self):
        return type(JString)


class JListStart(Token):
    def __init__(self, value: chr):
        super().__init__(value)

    def get_type(self):
        return type(JListStart)


class JListEnd(Token):
    def __init__(self, value: chr):
        super().__init__(value)

    def get_type(self):
        return type(JListEnd)


class JObjectStart(Token):
    def __init__(self, value: chr):
        super().__init__(value)

    def get_type(self):
        return type(JObjectStart)


class JObjectEnd(Token):
    def __init__(self, value: chr):
        super().__init__(value)

    def get_type(self):
        return type(JObjectEnd)
