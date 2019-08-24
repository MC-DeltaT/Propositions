from abc import ABC, abstractmethod


__all__ = [
    "BooleanValue",
    "F",
    "FalseType",
    "from_bool",
    "T",
    "TrueType"
]


class BooleanValue(ABC):
    @property
    @abstractmethod
    def value(self) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    def __bool__(self) -> bool:
        return self.value

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class FalseType(BooleanValue):
    @property
    def value(self) -> bool:
        return False

    def __eq__(self, other) -> bool:
        return isinstance(other, FalseType)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return "F"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


class TrueType(BooleanValue):
    @property
    def value(self) -> bool:
        return True

    def __eq__(self, other) -> bool:
        return isinstance(other, TrueType)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return "T"

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


F = FalseType()
T = TrueType()


def from_bool(value) -> BooleanValue:
    if value:
        return T
    else:
        return F
