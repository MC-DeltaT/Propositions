from typing import Callable, Dict, Sequence, Tuple


class Variable:
    def __init__(self, name: str) -> None:
        if len(name) == 0:
            raise ValueError("name must not be empty.")
        if not name.isalpha():
            raise ValueError("name must contain only letters.")
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "%s(name=%r)" % (self.__class__.__name__, self.name)


class TruthTable:
    def __init__(self, inputs: Sequence[Variable], predicate: Callable[..., bool]) -> None:
        self.inputs = inputs
        self.num_inputs = len(inputs)
        self.predicate = predicate
        self.table = self._create_table()

    def eval(self, *input_values: bool) -> bool:
        if len(input_values) != len(self.inputs):
            raise TypeError("Expected {} input values but got {}.".format(len(self.inputs), len(input_values)))
        return self.table[tuple(input_values)]

    def __eq__(self, other):
        return isinstance(other, TruthTable) and self.table == other.table

    def _create_table(self) -> Dict[Tuple[bool, ...], bool]:
        table = {}
        n = 2 ** self.num_inputs
        for i in range(n):
            input_values = [bool(i // (2 ** j) % 2) for j in reversed(range(self.num_inputs))]
            res = self.predicate(*input_values)
            table[tuple(input_values)] = res
        return table


p = Variable("p")
q = Variable("q")
r = Variable("r")
s = Variable("s")
op = lambda p, q, r, s: (p or q) and not (r and s)

tt = TruthTable((p, q, r, s), op)

pass
