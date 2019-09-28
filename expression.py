from boolean import BooleanValue, F, T
from truthtable import Input, TruthTable
from utility import cached_property

from typing import Any, Set


__all__ = [
    "CompoundExpression",
    "Expression",
    "Literal",
    "literal_f",
    "literal_t",
    "SimpleExpression",
    "Variable"
]


class Expression:
    @cached_property
    def truth(self) -> TruthTable:
        return None

    @property
    def values(self) -> Set[BooleanValue]:
        return self.truth.outputs

    @property
    def is_exact(self) -> bool:
        return len(self.values) == 1

    @property
    def exact_value(self) -> BooleanValue:
        if not self.is_exact:
            raise ValueError("Expression is not exact.")
        return next(iter(self.values))

    @property
    def is_contradiction(self) -> bool:
        return self.is_exact and not bool(self.exact_value)

    @property
    def is_tautology(self) -> bool:
        return self.is_exact and bool(self.exact_value)

    def could_be(self, value: BooleanValue) -> bool:
        return value in self.values

    def probability(self, value: BooleanValue) -> float:
        return self.truth.distribution[value]


class SimpleExpression(Expression):
    pass


class CompoundExpression(Expression):
    pass


class Literal(SimpleExpression):
    def __init__(self, value: BooleanValue) -> None:
        self.value = value

    @cached_property
    def truth(self) -> TruthTable:
        return TruthTable((Input(self.value, {self.value}),), {
            (self.value,): self.value
        }, str(self))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Literal) and self.value == other.value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return "Literal(value={})".format(repr(self.value))


class Variable(SimpleExpression):
    def __init__(self, name: str) -> None:
        if len(name) == 0:
            raise ValueError("name must not be empty.")
        if not name.isalpha():
            raise ValueError("name must contain only letters.")
        self.name = name

    @cached_property
    def truth(self) -> TruthTable:
        return TruthTable((Input(self),), {
            (F,): F,
            (T,): T
        }, str(self))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "Variable(name={})".format(self.name)


literal_f = Literal(F)
literal_t = Literal(T)
