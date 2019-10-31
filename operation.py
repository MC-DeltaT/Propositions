from boolean import F, T
from expression import CompoundExpression, Expression, SimpleExpression
from truthtable import join_tables, TruthTable
from utility import cached_property


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


class Operation(CompoundExpression):
    join: TruthTable = None


class UnaryOperation(Operation):
    symbol: str = None

    def __init__(self, rhs: Expression) -> None:
        self.rhs = rhs

    @cached_property
    def truth(self) -> TruthTable:
        table = join_tables(self.join, (self.rhs.truth,))
        table.name = str(self)
        return table

    def __str__(self) -> str:
        if isinstance(self.rhs, SimpleExpression) or isinstance(self.rhs, UnaryOperation):
            return f"{self.symbol}{self.rhs}"
        else:
            return f"({self.symbol}{self.rhs})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rhs={repr(self.rhs)})"


class Identity(UnaryOperation):
    symbol = ""

    join = TruthTable(1, {
            (F,): F,
            (T,): T
        })


class Negation(UnaryOperation):
    symbol = "~"

    join = TruthTable(1, {
            (F,): T,
            (T,): F
        }, symbol)


class BinaryOperation(Operation):
    symbol: str = None

    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    @cached_property
    def truth(self) -> TruthTable:
        table = join_tables(self.join, (self.lhs.truth, self.rhs.truth))
        table.name = str(self)
        return table

    def __str__(self) -> str:
        return f"({self.lhs} {self.symbol} {self.rhs})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lhs={repr(self.lhs)}, rhs={repr(self.rhs)})"


class Conjunction(BinaryOperation):
    symbol = "&"

    join = TruthTable(2, {
            (F, F): F,
            (F, T): F,
            (T, F): F,
            (T, T): T
        }, symbol)


class Disjunction(BinaryOperation):
    symbol = "|"

    join = TruthTable(2, {
            (F, F): F,
            (F, T): T,
            (T, F): T,
            (T, T): T
        }, symbol)


class ExclDisjunction(BinaryOperation):
    symbol = "+"

    join = TruthTable(2, {
            (F, F): F,
            (F, T): T,
            (T, F): T,
            (T, T): F
        }, symbol)


class Implication(BinaryOperation):
    symbol = "->"

    join = TruthTable(2, {
            (F, F): T,
            (F, T): T,
            (T, F): F,
            (T, T): T
        }, symbol)


class Biconditional(BinaryOperation):
    symbol = "<->"

    join = TruthTable(2, {
            (F, F): T,
            (F, T): F,
            (T, F): F,
            (T, T): T
        }, symbol)


unary_operations = (
    Identity,
    Negation
)

binary_operations = (
    Biconditional,
    Conjunction,
    Disjunction,
    ExclDisjunction,
    Implication
)
