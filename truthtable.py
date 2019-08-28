from boolean import BooleanValue, F, T

from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union


__all__ = [
    "Input",
    "join_tables",
    "TruthTable",
    "value_combinations"
]


class Input:
    class UniqueTag:
        def __init__(self, value: Any) -> None:
            self.value = value

        def __str__(self) -> str:
            return str(self.value)

        def __repr__(self) -> str:
            return str(self.value)

    def __init__(self, tag: Optional[Any] = None, values: Optional[Set[BooleanValue]] = None) -> None:
        if values is None:
            self.values = {F, T}
        else:
            self.values = values
        if tag is None:
            self.tag = self.UniqueTag("<no_tag>")
        else:
            self.tag = tag

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Input) and self.tag == other.tag


class TruthTable:
    def __init__(self, inputs: Union[Sequence[Input], int], table: Mapping[Tuple[BooleanValue, ...], BooleanValue], name: Optional[str] = None) -> None:
        if isinstance(inputs, int):
            self.inputs = tuple(Input.UniqueTag("<{}>".format(i + 1)) for i in range(inputs))
        else:
            self.inputs = inputs
        self.table = table
        self.name = name

    @property
    def outputs(self) -> Set[BooleanValue]:
        return set(self.table.values())

    @property
    def distribution(self) -> Dict[BooleanValue, float]:
        return {value: sum(1 for v in self.table.values() if v == value) / len(self.table) for value in (F, T)}

    def __getitem__(self, inputs: Tuple[BooleanValue, ...]) -> BooleanValue:
        return self.table[inputs]

    def print(self) -> None:
        in_divider = " | "
        out_divider = " || "
        headers = [str(i.tag) for i in self.inputs]
        header = in_divider.join(headers) + out_divider + ("<out>" if self.name is None else self.name)
        print(header)
        for inputs, output in self.table.items():
            cols: List[str] = []
            for i, value in enumerate(inputs):
                s = str(value)
                s = " " * (len(headers[i]) - len(s)) + s
                cols.append(s)
            row = in_divider.join(cols) + out_divider + str(output)
            print(row)


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
