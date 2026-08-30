from typing import Any
lazy from .provider import ValueProvider


class Condition:
    def check(self, context: Any = None) -> bool:  #type: ignore
        pass

    def _getValue(self, value: Any, context: Any = None):
        if isinstance(value, ValueProvider):
            return value.get(context)
        else:
            return value


class Equal(Condition):
    def __init__(self, leftValue:  Any, rightValue:  Any):
        self.leftValue = leftValue
        self.rightValue = rightValue

    def check(self, context: Any = None):
    
        return self._getValue(self.leftValue, context) == self._getValue(self.rightValue, context)

    def __str__(self):
        return f"{self.leftValue} == {self.rightValue}"

