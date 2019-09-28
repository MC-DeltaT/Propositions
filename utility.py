from typing import Any, Callable


__all__ = [
    "cached_property"
]


class cached_property:
    def __init__(self, fget: Callable[[Any], Any]) -> None:
        self.fget = fget

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            result = self.fget(obj)
            setattr(obj, self.fget.__name__, result)
            return result
