from typing import Any, Callable

from .exceptions import ContextAccessError
from .condition import Equal


class ValueProvider:
    def get(self, context: Any):
        raise NotImplementedError

    def __eq__(self, other): #type: ignore
        return Equal(self, other)


class Ref(ValueProvider):

    def __init__(self, name:str):
        self.name = name

    def get(self, context: Any):
        if hasattr(context, "get"):
            return context.get(self.name)
        else:
            raise ContextAccessError(context)
            raise ContextAccessError(context)

    # def __str__(self):
    #     return self.name

    def __repr__(self):
        return f"Ref({self.name})"


class Computed(ValueProvider):
    def __init__(self, func: Callable, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def get(self, context: Any=None):
        return self.func(*self.args, **self.kwargs)

    def __repr__(self):
        return f"Computed({self.func}, {self.args}, {self.kwargs})"