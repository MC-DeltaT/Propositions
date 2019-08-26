from truthtable import Input, TruthTable
from value import BooleanValue, F, T

from abc import ABC, abstractmethod
from typing import Set


__all__ = [
    "CompoundExpression",
    "Expression",
    "Literal",
    "SimpleExpression",
    "Variable"
]


class Expression(ABC):
    @property
    @abstractmethod
    def truth(self) -> TruthTable:
        pass

    @property
    def values(self) -> Set[BooleanValue]:
        return self.truth.outputs()

    def could_be(self, value: BooleanValue) -> bool:
        return self.truth.could_output(value)


class SimpleExpression(Expression, ABC):
    pass


class CompoundExpression(Expression, ABC):
    pass


class Literal(SimpleExpression):
    def __init__(self, value: BooleanValue) -> None:
        self.value = value

    @property
    def truth(self) -> TruthTable:
        return TruthTable((Input(self.value, {self.value}),), {
            (self.value,): self.value
        })


class Variable(SimpleExpression):
    def __init__(self, name: str) -> None:
        if len(name) == 0:
            raise ValueError("name must not be empty.")
        if not name.isalpha():
            raise ValueError("name must contain only letters.")
        self.name = name

    @property
    def truth(self) -> TruthTable:
        return TruthTable((Input(self),), {
            (F,): F,
            (T,): T
        })

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "Variable(name={})".format(self.name)
