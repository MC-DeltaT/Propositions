import expression
import operation
import boolean

from abc import ABC, abstractmethod
import re
from typing import List, Sequence, Union


__all__ = [
    "InvalidSyntax",
    "parse"
]


class Token(ABC):
    def __init__(self, source: str, start_pos: int, end_pos: int) -> None:
        if start_pos < 0:
            raise ValueError("start_pos must be >= 0.")
        if end_pos < start_pos:
            raise ValueError("start_pos must be <= end_pos.")
        self.source = source
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.string = source[start_pos:end_pos]

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.string


class StartOfTokens(Token):
    @property
    def description(self) -> str:
        return "start of string"


class EndOfTokens(Token):
    @property
    def description(self) -> str:
        return "end of string"


class SimpleExpression(Token, ABC):
    @property
    @abstractmethod
    def expr(self) -> expression.SimpleExpression:
        pass


class BooleanLiteral(SimpleExpression):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._expr = expression.Literal(str_to_boolean(self.string))

    @property
    def description(self) -> str:
        return "literal"

    @property
    def expr(self) -> expression.SimpleExpression:
        return self._expr


class Variable(SimpleExpression):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._expr = expression.Variable(self.string)

    @property
    def description(self) -> str:
        return "variable"

    @property
    def expr(self) -> expression.SimpleExpression:
        return self._expr


class Operator(Token, ABC):
    pass


class UnaryOperator(Operator):
    @property
    def description(self) -> str:
        return "unary operator"


class BinaryOperator(Operator):
    @property
    def description(self) -> str:
        return "binary operator"


class OpenParenthesis(Token):
    @property
    def description(self) -> str:
        return "opening parenthesis"


class CloseParenthesis(Token):
    @property
    def description(self) -> str:
        return "closing parenthesis"


class OperatorInfo:
    def __init__(self, precedence: int, cls: type) -> None:
        self.precedence = precedence
        self.cls = cls


class InvalidSyntax(ValueError):
    def __init__(self, pos: int, message: str):
        self.pos = pos
        self.message = message

    def __str__(self):
        return "At position {}: {}".format(self.pos, self.message)


# A list of regexes defining the allowed tokens, and their associated classes.
token_regexes = [
    (r"\(", OpenParenthesis),
    (r"\)", CloseParenthesis),
    ("[TF]", BooleanLiteral),
    ("~", UnaryOperator),
    ("<->|->|[&|+]", BinaryOperator),
    (r"[a-z]+", Variable)
]


# A sequence of 2 consecutive tokens must be one of these to be valid.
valid_sequences = (
    (StartOfTokens, EndOfTokens),
    (StartOfTokens, SimpleExpression),
    (StartOfTokens, OpenParenthesis),
    (StartOfTokens, UnaryOperator),
    (SimpleExpression, BinaryOperator),
    (SimpleExpression, CloseParenthesis),
    (SimpleExpression, EndOfTokens),
    (UnaryOperator, SimpleExpression),
    (UnaryOperator, OpenParenthesis),
    (UnaryOperator, UnaryOperator),
    (BinaryOperator, SimpleExpression),
    (BinaryOperator, UnaryOperator),
    (BinaryOperator, OpenParenthesis),
    (OpenParenthesis, OpenParenthesis),
    (OpenParenthesis, SimpleExpression),
    (OpenParenthesis, UnaryOperator),
    (CloseParenthesis, BinaryOperator),
    (CloseParenthesis, CloseParenthesis),
    (CloseParenthesis, EndOfTokens),
)


# Maps operator strings to their precedence and class.
operator_info = {
    "~": OperatorInfo(4, operation.Negation),
    "&": OperatorInfo(3, operation.Conjunction),
    "|": OperatorInfo(3, operation.Disjunction),
    "+": OperatorInfo(2, operation.ExclDisjunction),
    "->": OperatorInfo(1, operation.Implication),
    "<->": OperatorInfo(0, operation.Biconditional)
}


def parse(expr: str) -> Union[expression.Expression, None]:
    tokens = parse_tokens(expr)
    check_syntax(tokens)
    postfix = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix)
    return result


def parse_tokens(expr: str) -> List[Token]:
    tokens: List[Token] = [StartOfTokens(expr, 0, 0)]
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        else:
            matched = False
            j = 0
            while not matched and j < len(token_regexes):
                regex, cls = token_regexes[j]
                match = re.match(regex, expr[i:])
                if match:
                    start_pos = i + match.start()
                    end_pos = i + match.end()
                    token = cls(expr, start_pos, end_pos)
                    tokens.append(token)
                    matched = True
                    i = end_pos
                j += 1
            if not matched:
                raise InvalidSyntax(i, "Invalid token.")
    tokens.append(EndOfTokens(expr, len(expr), len(expr)))
    return tokens


def str_to_boolean(s: str) -> boolean.BooleanValue:
    if s == "T":
        return boolean.T
    elif s == "F":
        return boolean.F
    else:
        raise AssertionError("Didn't expect string \"{}\".".format(s))


def check_syntax(tokens: Sequence[Token]) -> None:
    assert len(tokens) >= 2
    prev_token = tokens[0]
    for token in tokens[1:]:
        if not is_token_allowed(prev_token, token):
            raise InvalidSyntax(token.start_pos, "Unexpected {} after {}.".format(token.description, prev_token.description))
        prev_token = token


def infix_to_postfix(tokens: Sequence[Token]) -> List[Token]:
    postfix: List[Token] = []
    operators: List[Union[Operator, OpenParenthesis]] = []
    assert len(tokens) >= 2
    for token in tokens[1:-1]:
        if isinstance(token, OpenParenthesis):
            operators.append(token)

        elif isinstance(token, CloseParenthesis):
            try:
                while not isinstance(operators[-1], OpenParenthesis):
                    postfix.append(operators.pop())
            except ValueError:
                raise InvalidSyntax(token.start_pos, "Unmatched closing parenthesis.")
            operators.pop()

        elif isinstance(token, UnaryOperator):
            operators.append(token)

        elif isinstance(token, BinaryOperator):
            while operators and not isinstance(operators[-1], OpenParenthesis) and operator_precedence(operators[-1]) >= operator_precedence(token):
                postfix.append(operators.pop())
            operators.append(token)

        elif isinstance(token, SimpleExpression):
            postfix.append(token)

        else:
            raise AssertionError("Didn't expect type `{}`.".format(type(token)))

    while operators:
        token = operators.pop()
        if isinstance(token, OpenParenthesis):
            raise InvalidSyntax(token.start_pos, "Unmatched opening parenthesis.")
        postfix.append(token)

    return postfix


# Checks if the occurrence of token directly after prev_token is valid.
def is_token_allowed(prev_token: Token, token: Token) -> bool:
    # Set of token types that are allowed to occur after the previous token.
    allowed = map(lambda t: t[1],
                  filter(lambda t: isinstance(prev_token, t[0]),
                      valid_sequences))
    return any(map(lambda cls: isinstance(token, cls), allowed))


def operator_precedence(token: Operator) -> int:
    assert token.string in operator_info
    return operator_info[token.string].precedence


def evaluate_unary_operator(op: Operator, arg: expression.Expression) -> expression.Expression:
    assert op.string in operator_info
    return operator_info[op.string].cls(arg)


def evaluate_binary_operator(op: Operator, lhs: expression.Expression, rhs: expression.Expression) -> expression.Expression:
    assert op.string in operator_info
    return operator_info[op.string].cls(lhs, rhs)


def evaluate_postfix(postfix: List[Token]) -> Union[expression.Expression, None]:
    if len(postfix) == 0:
        return None
    operands: List[expression.Expression] = []
    for token in postfix:
        if isinstance(token, UnaryOperator):
            assert len(operands) >= 1
            arg = operands.pop()
            result = evaluate_unary_operator(token, arg)
            operands.append(result)
        elif isinstance(token, BinaryOperator):
            assert len(operands) >= 2
            rhs = operands.pop()
            lhs = operands.pop()
            result = evaluate_binary_operator(token, lhs, rhs)
            operands.append(result)
        elif isinstance(token, SimpleExpression):
            operands.append(token.expr)
        else:
            raise AssertionError("Didn't expect type `{}`.".format(type(token)))
    assert len(operands) == 1
    assert isinstance(operands[-1], expression.Expression)
    return operands.pop()
