from value import BooleanValue, T, F

from abc import ABC, abstractmethod
from typing import Set


class Expression(ABC):
    @abstractmethod
    def values(self) -> Set[BooleanValue]:
        pass

    def could_be(self, value: BooleanValue) -> bool:
        return value in self.values()


class Literal(Expression):
    def __init__(self, value: BooleanValue) -> None:
        self.value = value

    def values(self) -> Set[BooleanValue]:
        return {self.value}


class Variable(Expression):
    def __init__(self, name: str) -> None:
        if len(name) == 0:
            raise ValueError("name must not be empty.")
        if not name.isalpha():
            raise ValueError("name must contain only letters.")
        self.name = name

    def values(self) -> Set[BooleanValue]:
        return {T, F}

    def substitute(self, **variables: Literal) -> Literal:
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
