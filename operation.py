from expression import Expression
from truthtable import TruthTable
from value import BooleanValue, F, T

from abc import ABC, abstractmethod
from typing import Set


class UnaryOperation(Expression, ABC):
    @property
    @abstractmethod
    def truth(self) -> TruthTable:
        pass

    def __init__(self, rhs: Expression) -> None:
        self.rhs = rhs

    def values(self) -> Set[BooleanValue]:
        rhs_values = self.rhs.values()
        restriction = [rhs_values]
        return self.truth.restrict(restriction).outputs()


class Negation(UnaryOperation):
    @property
    def truth(self) -> TruthTable:
        return TruthTable((
            ((F,), T),
            ((T,), F)
        ))


class BinaryOperation(Expression, ABC):
    @property
    @abstractmethod
    def truth(self) -> TruthTable:
        pass

    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def values(self) -> Set[BooleanValue]:
        lhs_values = self.lhs.values()
        rhs_values = self.rhs.values()
        restriction = [lhs_values, rhs_values]
        return self.truth.restrict(restriction).outputs()


class Conjunction(BinaryOperation):
    @property
    def truth(self) -> TruthTable:
        return TruthTable((
            ((F, F), F),
            ((F, T), F),
            ((T, F), F),
            ((T, T), T)
        ))


class Disjunction(BinaryOperation):
    @property
    def truth(self) -> TruthTable:
        return TruthTable((
            ((F, F), F),
            ((F, T), T),
            ((T, F), T),
            ((T, T), T)
        ))


class ExclDisjunction(BinaryOperation):
    @property
    def truth(self) -> TruthTable:
        return TruthTable((
            ((F, F), F),
            ((F, T), T),
            ((T, F), T),
            ((T, T), F)
        ))


class Implication(BinaryOperation):
    @property
    def truth(self) -> TruthTable:
        return TruthTable((
            ((F, F), T),
            ((F, T), T),
            ((T, F), F),
            ((T, T), T)
        ))


class Biconditional(BinaryOperation):
    @property
    def truth(self) -> TruthTable:
        return TruthTable((
            ((F, F), T),
            ((F, T), F),
            ((T, F), F),
            ((T, T), T)
        ))
