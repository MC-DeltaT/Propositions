from expression import Expression
from truthtable import TruthTable
from value import F, T


class UnaryOperation(Expression):
    def __init__(self, rhs: Expression) -> None:
        self.rhs = rhs


class Negation(UnaryOperation):
    truth = TruthTable((
        ((F,), T),
        ((T,), F)
    ))


class BinaryOperation(Expression):
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs


class Conjunction(BinaryOperation):
    truth = TruthTable((
        ((F, F), F),
        ((F, T), F),
        ((T, F), F),
        ((T, T), T)
    ))


class Disjunction(BinaryOperation):
    truth = TruthTable((
        ((F, F), F),
        ((F, T), T),
        ((T, F), T),
        ((T, T), T)
    ))


class ExclDisjunction(BinaryOperation):
    truth = TruthTable((
        ((F, F), F),
        ((F, T), T),
        ((T, F), T),
        ((T, T), F)
    ))


class Implication(BinaryOperation):
    truth = TruthTable((
        ((F, F), T),
        ((F, T), T),
        ((T, F), F),
        ((T, T), T)
    ))


class Biconditional(BinaryOperation):
    truth = TruthTable((
        ((F, F), T),
        ((F, T), F),
        ((T, F), F),
        ((T, T), T)
    ))
