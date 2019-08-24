from value import BooleanValue

from typing import FrozenSet, List, Mapping, Optional, Sequence, Set, Tuple, Union


__all__ = [
    "TruthTable"
]


Inputs = Tuple[BooleanValue, ...]
ValueRestriction = Union[Set[BooleanValue], None]
Output = BooleanValue
Row = Tuple[Inputs, Output]


class TruthTable:
    def __init__(self, rows: Sequence[Row]) -> None:
        self._check(rows)
        self.num_inputs = len(rows[0][0])
        self.table = self._create_table(rows)
        self.hashtable = self._create_hashtable(rows)

    def lookup(self, inputs: Inputs) -> BooleanValue:
        if len(inputs) != self.num_inputs:
            raise ValueError("Expected {} inputs but got {}.".format(self.num_inputs, len(inputs)))
        try:
            return self.hashtable[inputs]
        except KeyError:
            raise ValueError("Input of {} does not map to any output.".format(inputs))

    def restrict(self, input_restrict: Optional[Sequence[ValueRestriction]] = None, output_restrict: ValueRestriction = None):
        if len(input_restrict) != self.num_inputs:
            raise ValueError("Expected {} inputs but got {}.".format(self.num_inputs, len(input_restrict)))
        new_rows: List[Row] = []
        for row in self.table:
            match = True
            if output_restrict is not None and row[1] not in output_restrict:
                match = False
            for i, i_r in zip(row[0], input_restrict):
                if i_r is not None and i not in i_r:
                    match = False
            if match:
                new_rows.append(row)
        if not new_rows:
            raise ValueError("Restriction would eliminate all rows from table.")
        return TruthTable(new_rows)

    def outputs(self) -> Set[BooleanValue]:
        return {row[1] for row in self.table}

    def could_output(self, value: BooleanValue) -> bool:
        return value in self.outputs()

    def __eq__(self, other):
        return isinstance(other, TruthTable) and self.table == other.table

    @staticmethod
    def _check(rows: Sequence[Row]) -> None:
        if len(rows) < 1:
            raise ValueError("Truth table must have at least 1 row.")
        prev_row = rows[0]
        for row in rows[1:]:
            if len(row[0]) != len(prev_row[0]):
                raise ValueError("Rows must have the same length.")
            prev_row = row

    @staticmethod
    def _create_table(rows: Sequence[Row]) -> FrozenSet[Row]:
        return frozenset(rows)

    @staticmethod
    def _create_hashtable(rows: Sequence[Row]) -> Mapping[Inputs, Output]:
        return {row[0]: row[1] for row in rows}
