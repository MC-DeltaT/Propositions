class Expression:
    pass


class KnownExpression(Expression):
    @staticmethod
    def from_value(v):
        if v:
            return T
        else:
            return F


class FalseType(KnownExpression):
    def __eq__(self, other) -> bool:
        return isinstance(other, FalseType)

    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return "F"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"

    def __hash__(self) -> int:
        return hash(False)


class TrueType(KnownExpression):
    def __eq__(self, other) -> bool:
        return isinstance(other, TrueType)

    def __bool__(self) -> bool:
        return True

    def __str__(self) -> str:
        return "T"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"

    def __hash__(self) -> int:
        return hash(True)


T = TrueType()
F = FalseType()


class UnknownExpression(Expression):
    pass


class Variable(UnknownExpression):
    def __init__(self, name: str) -> None:
        if len(name) == 0:
            raise ValueError("name must not be empty.")
        if not name.isalpha():
            raise ValueError("name must contain only letters.")
        self.name = name

    def substitute(self, **variables: KnownExpression) -> KnownExpression:
        if self.name in variables:
            return variables[self.name]
        else:
            raise TypeError("Value of variable {} not specified.".format(self.name))

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "Variable(name={})".format(self.name)
