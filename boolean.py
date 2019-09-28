from typing import Any


__all__ = [
    "BooleanValue",
    "F",
    "FalseType",
    "from_bool",
    "T",
    "TrueType"
]


class BooleanValue:
    value: bool = None

    def __bool__(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


class FalseType(BooleanValue):
    value = False

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, FalseType)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return "F"


class TrueType(BooleanValue):
    value = True

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TrueType)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return "T"


F = FalseType()
T = TrueType()


def from_bool(value) -> BooleanValue:
    if value:
        return T
    else:
        return F
