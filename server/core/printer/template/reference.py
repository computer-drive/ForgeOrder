from typing import Callable, TypeVar, Generic, cast 

MISSING = sentinel("MISSING")

T = TypeVar("T")

class Ref(Generic[T]):
    def __init__(self, name: str):
        self.members = name.split(".")

    def render(self, context: dict) -> T | MISSING:
        data = context
        for member in self.members:
            if member in data:
                data = data[member]
            else:
                return MISSING
            
        return data #type: ignore

    def __getattr__(self, name):
        self.members.append(name)
        return self

    def __getitem__(self, name):
        self.members.append(name)
        return self

class Value(Ref[T]):
    def __init__(self, value: T):
        self.value: T = value

    def render(self, context: dict) -> T:
        if isinstance(self.value, str):
            return cast(T, self.value.format(**context))
        else:
            return self.value
    

class Computed(Ref[T]):
    def __init__(self, name: str, func: Callable):
        super().__init__(name)
        self.func = func

    def render(self, context: dict):
        data = super().render(context)

        if data is MISSING:
            return MISSING
        
        return self.func(data)




    
    