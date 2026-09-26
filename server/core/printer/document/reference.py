from typing import TypeVar, Generic, Callable, Any

T = TypeVar("T")

MISSING = sentinel("MISSING")

class Reference(Generic[T]):

    def __init__(self, name: str, context: dict | None = None):
        self.value: T | MISSING = MISSING
        self.name = name

        self.subReference: Reference | None = None

    def getValue(self) -> T:
        if self.subReference is not None:
            return self.subReference.getValue()
        
        if self.value is not MISSING:
            return self.value 
        else:
            raise ValueError(f"Reference {self.name} has no value.")

    def setValue(self, **kwargs):
        if self.name in kwargs:
            self.value = kwargs[self.name]

    def setValueFromParent(self, parentValue: Any) -> None:
        raise NotImplemented

    def __getattr__(self, attr: str):
        newReference = AttributeReferEnce(self.name, attr)
        self.subReference = newReference
        return newReference

    def __repr__(self):
        return f'Reference({self.name})'

    def __getitem__(self, key):
        newReference = ItemReference(self.name, key)
        self.subReference = newReference
        return newReference


class ReferenceWithValue(Reference):

    def __init__(self, value: T):
        self.name = "HAS_VALUE"
        self.value = value

    def __repr__(self):
        return f'ReferenceWithValue({self.value})'


class AttributeReferEnce(Reference):
    def __init__(self, name: str, attr: str):
        super().__init__(name)

        self.attr = attr

    def setValue(self, **kwargs):
        if self.name in kwargs:
            self.setValueFromParent(kwargs[self.name])

    def setValueFromParent(self, parentValue: Any):
        obj = getattr(parentValue[self.name], self.attr, MISSING)

        if obj is not MISSING:
            self.value = obj

    def __repr__(self):
        return f'AttributeReferEnce({self.name}, {self.attr})'



class ItemReference(Reference):
    def __init__(self, name: str, attr: str):
        super().__init__(name)
        self.attr = attr

    def setValue(self, **kwargs):
        if self.name in kwargs:
            self.setValueFromParent(kwargs[self.name])

    def setValueFromParent(self, parentValue: Any):
        try:
            obj = parentValue[self.attr]
            self.value = obj
        except (KeyError, TypeError):
            pass

    def __repr__(self):
        return f'ItemReference({self.name}, {self.attr})'
            
            

class Computed(Reference):
    def __init__(self, name: str, func: Callable):
        super().__init__(name)
        self.func = func

    def setValue(self, **kwargs):
        if self.name in kwargs:
            return self.setValueFromParent(kwargs[self.name])

    def setValueFromParent(self, parentValue: Any):
        self.value = self.func(parentValue)

    def __repr__(self):
        return f'Computed({self.name}, {self.func})'

