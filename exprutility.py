from boolean import BooleanValue
from expression import Expression, literal_f, literal_t, Variable
from operation import binary_operations, unary_operations

import random


__all__ = [
    "random_expression",
    "random_expression_with_value"
]


def random_expression(max_vars: int, max_depth: int) -> Expression:
    if not 0 <= max_vars <= 26:
        raise ValueError("max_vars must be >= 0 and <= 26.")
    if max_depth <= 0:
        raise ValueError("max_depth must be > 0.")

    variables = random.choices([Variable(c) for c in "abcdefghijklmnopqrstuvwxyz"], k=max_vars)
    literals = [literal_f, literal_t]

    def _random_expression(depth=0):
        r = random.randint(1, 100)
        simple_cutoff = round((depth / max_depth) * 100)
        if r <= simple_cutoff:
            if max_vars == 0 or random.randint(0, 1) == 0:
                return random.choice(literals)
            else:
                return random.choice(variables)
        elif r <= simple_cutoff + ((100 - simple_cutoff) / 3):
            return random.choice(unary_operations)(_random_expression(depth + 1))
        else:
            return random.choice(binary_operations)(_random_expression(depth + 1), _random_expression(depth + 1))

    return _random_expression()


def random_expression_with_value(max_vars: int, max_depth: int, value: BooleanValue) -> Expression:
    while True:
        expr = random_expression(max_vars, max_depth)
        try:
            if expr.exact_value == value:
                return expr
        except ValueError:
            pass
