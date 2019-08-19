from expression import Expression, KnownExpression, F, T, UnknownExpression
from truthtable import TruthTable


class UnaryOperation(UnknownExpression):
    def __init__(self, rhs: UnknownExpression) -> None:
        self.rhs = rhs


class Negation(UnaryOperation):
    truth = TruthTable([
        ((F(),), T()),
        ((T(),), F())
    ])


class BinaryOperation(UnknownExpression):
    def __init__(self, lhs: UnknownExpression, rhs: UnknownExpression) -> None:
        self.lhs = lhs
        self.rhs = rhs


class Conjunction(BinaryOperation):
    truth = TruthTable([
        ((F(), F()), F()),
        ((F(), T()), F()),
        ((T(), F()), F()),
        ((T(), T()), T())
    ])


class Disjunction(BinaryOperation):
    truth = TruthTable([
        ((F(), F()), F()),
        ((F(), T()), T()),
        ((T(), F()), T()),
        ((T(), T()), T())
    ])


class ExclDisjunction(BinaryOperation):
    truth = TruthTable([
        ((F(), F()), F()),
        ((F(), T()), T()),
        ((T(), F()), T()),
        ((T(), T()), F())
    ])


class Implication(BinaryOperation):
    truth = TruthTable([
        ((F(), F()), T()),
        ((F(), T()), T()),
        ((T(), F()), F()),
        ((T(), T()), T())
    ])


class Biconditional(BinaryOperation):
    truth = TruthTable([
        ((F(), F()), T()),
        ((F(), T()), F()),
        ((T(), F()), F()),
        ((T(), T()), T())
    ])


def negation(rhs: Expression) -> Expression:
    if isinstance(rhs, KnownExpression):
        return KnownExpression.from_value(not rhs)
    else:
        assert isinstance(rhs, UnknownExpression)
        return Negation(rhs)


def conjunction(lhs: Expression, rhs: Expression) -> Expression:
    if isinstance(lhs, KnownExpression) and isinstance(rhs, KnownExpression):
        return KnownExpression.from_value(lhs and rhs)
    elif isinstance(lhs, F) or isinstance(rhs, F):
        return F()
    else:
        assert isinstance(lhs, UnknownExpression)
        assert isinstance(rhs, UnknownExpression)
        return Conjunction(lhs, rhs)


def disjunction(lhs: Expression, rhs: Expression) -> Expression:
    if isinstance(lhs, KnownExpression) and isinstance(rhs, KnownExpression):
        return KnownExpression.from_value(lhs or rhs)
    elif isinstance(lhs, T) or isinstance(rhs, T):
        return T()
    else:
        assert isinstance(lhs, UnknownExpression)
        assert isinstance(rhs, UnknownExpression)
        return Disjunction(lhs, rhs)


def excl_disjunction(lhs: Expression, rhs: Expression) -> Expression:
    if isinstance(lhs, KnownExpression) and isinstance(rhs, KnownExpression):
        return KnownExpression.from_value(lhs or rhs)
    else:
        assert isinstance(lhs, UnknownExpression)
        assert isinstance(rhs, UnknownExpression)
        return ExclDisjunction(lhs, rhs)


# def implication(lhs: Expression, rhs: Expression) -> Expression:
#     ...


# def biconditional(lhs: Expression, rhs: Expression) -> Expression:
#     ...
