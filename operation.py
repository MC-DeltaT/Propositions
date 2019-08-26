from expression import CompoundExpression, Expression
from truthtable import TruthTable, join_tables
from value import F, T

from abc import ABC, abstractmethod


__all__ = [
    "Biconditional",
    "BinaryOperation",
    "Conjunction",
    "Disjunction",
    "ExclDisjunction",
    "Implication",
    "Negation",
    "Operation",
    "UnaryOperation",
]


class Operation(CompoundExpression, ABC):
    @property
    @abstractmethod
    def join(self) -> TruthTable:
        pass


class UnaryOperation(Operation, ABC):
    def __init__(self, rhs: Expression) -> None:
        self.rhs = rhs

    @property
    def truth(self) -> TruthTable:
        return join_tables(self.join, (self.rhs.truth,))


class Negation(UnaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(1, {
            (F,): T,
            (T,): F
        })


class BinaryOperation(Operation, ABC):
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    @property
    def truth(self) -> TruthTable:
        return join_tables(self.join, (self.lhs.truth, self.rhs.truth))


class Conjunction(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): F,
            (F, T): F,
            (T, F): F,
            (T, T): T
        })


class Disjunction(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): F,
            (F, T): T,
            (T, F): T,
            (T, T): T
        })


class ExclDisjunction(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): F,
            (F, T): T,
            (T, F): T,
            (T, T): F
        })


class Implication(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): T,
            (F, T): T,
            (T, F): F,
            (T, T): T
        })


class Biconditional(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): T,
            (F, T): F,
            (T, F): F,
            (T, T): T
        })
