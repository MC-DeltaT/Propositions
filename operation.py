from expression import CompoundExpression, Expression, SimpleExpression
from truthtable import join_tables, TruthTable
from boolean import F, T

from abc import ABC, abstractmethod


__all__ = [
    "Biconditional",
    "BinaryOperation",
    "binary_operations",
    "Conjunction",
    "Disjunction",
    "ExclDisjunction",
    "Identity",
    "Implication",
    "Negation",
    "Operation",
    "UnaryOperation",
    "unary_operations",
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
    @abstractmethod
    def symbol(self) -> str:
        pass

    @property
    def truth(self) -> TruthTable:
        table = join_tables(self.join, (self.rhs.truth,))
        table.name = str(self)
        return table

    def __str__(self) -> str:
        if isinstance(self.rhs, SimpleExpression) or isinstance(self.rhs, UnaryOperation):
            return "{}{}".format(self.symbol, self.rhs)
        else:
            return "({}{})".format(self.symbol, self.rhs)

    def __repr__(self) -> str:
        return "{}(rhs={})".format(self.__class__.__name__, repr(self.rhs))


class Identity(UnaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(1, {
            (F,): F,
            (T,): T
        })

    @property
    def symbol(self) -> str:
        return ""


class Negation(UnaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(1, {
            (F,): T,
            (T,): F
        }, self.symbol)

    @property
    def symbol(self) -> str:
        return "~"


class BinaryOperation(Operation, ABC):
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @property
    def truth(self) -> TruthTable:
        table = join_tables(self.join, (self.lhs.truth, self.rhs.truth))
        table.name = str(self)
        return table

    def __str__(self) -> str:
        return "({} {} {})".format(self.lhs, self.symbol, self.rhs)

    def __repr__(self) -> str:
        return "{}(lhs={}, rhs={})".format(self.__class__.__name__, repr(self.lhs), repr(self.rhs))


class Conjunction(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): F,
            (F, T): F,
            (T, F): F,
            (T, T): T
        }, self.symbol)

    @property
    def symbol(self) -> str:
        return "&"


class Disjunction(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): F,
            (F, T): T,
            (T, F): T,
            (T, T): T
        }, self.symbol)

    @property
    def symbol(self) -> str:
        return "|"


class ExclDisjunction(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): F,
            (F, T): T,
            (T, F): T,
            (T, T): F
        }, self.symbol)

    @property
    def symbol(self) -> str:
        return "+"


class Implication(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): T,
            (F, T): T,
            (T, F): F,
            (T, T): T
        }, self.symbol)

    @property
    def symbol(self) -> str:
        return "->"


class Biconditional(BinaryOperation):
    @property
    def join(self) -> TruthTable:
        return TruthTable(2, {
            (F, F): T,
            (F, T): F,
            (T, F): F,
            (T, T): T
        }, self.symbol)

    @property
    def symbol(self) -> str:
        return "<->"


unary_operations = [
    Identity,
    Negation
]

binary_operations = [
    Biconditional,
    Conjunction,
    Disjunction,
    ExclDisjunction,
    Implication
]
