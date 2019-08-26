from value import BooleanValue, F, T

from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union


__all__ = [
    "Input",
    "join_tables",
    "TruthTable",
    "value_combinations"
]


class Input:
    def __init__(self, tag: Optional[Any] = None, values: Optional[Set[BooleanValue]] = None) -> None:
        if values is None:
            self.values = {F, T}
        else:
            self.values = values
        if tag is None:
            self.tag = object()
        else:
            self.tag = tag

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Input) and self.tag == other.tag


class TruthTable:
    def __init__(self, inputs: Union[Sequence[Input], int], table) -> None:
        if isinstance(inputs, int):
            self.inputs = tuple(Input() for _ in range(inputs))
        else:
            self.inputs = inputs
        self.table = table

    def outputs(self) -> Set[BooleanValue]:
        return set(self.table.values())

    def could_output(self, value: BooleanValue) -> bool:
        return value in self.outputs()

    def __getitem__(self, inputs: Tuple[BooleanValue, ...]) -> BooleanValue:
        return self.table[inputs]


def join_tables(join_op: TruthTable, tables: Sequence[TruthTable]) -> TruthTable:
    input_vars = tuple(table.inputs for table in tables)

    input_var_indices: List[List[int]] = [[] for _ in input_vars]
    res_vars = []
    for variables, indices in zip(input_vars, input_var_indices):
        for var in variables:
            if var in res_vars:
                indices.append(res_vars.index(var))
            else:
                res_vars.append(var)
                indices.append(len(res_vars) - 1)

    res_tt: Dict[Tuple[BooleanValue, ...], BooleanValue] = {}
    for new_inputs in value_combinations(res_vars):
        base_inputs = (tuple(new_inputs[i] for i in indices) for indices in input_var_indices)
        base_outputs = tuple(tt[inputs] for tt, inputs in zip(tables, base_inputs))
        output = join_op[base_outputs]
        res_tt[new_inputs] = output

    return TruthTable(tuple(res_vars), res_tt)


def value_combinations(inputs: Sequence[Input]) -> List[Tuple[BooleanValue, ...]]:
    var_values = [list(var.values) for var in inputs]
    indices = [0] * len(inputs)
    result: List[Tuple[BooleanValue, ...]] = []
    while True:
        combo = tuple(values[idx] for values, idx in zip(var_values, indices))
        result.append(combo)
        carry = True
        for i in reversed(range(len(inputs))):
            if carry:
                indices[i] = (indices[i] + 1) % len(var_values[i])
                if indices[i] != 0:
                    carry = False
                    break
        if carry:
            break
    return result
