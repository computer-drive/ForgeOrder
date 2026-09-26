from .reference import Reference, Computed, ReferenceWithValue

from .component import Component

class Document:

    def __init__(self):
        self.data: list[Component] = []

        self.needFormatReference: list[Reference] = []

    def add(self, *components: Component):
        self.data.extend(components)

    def _ref(self, referenceClass: type[Reference], name: str):
        ref = referenceClass(name)

        self.needFormatReference.append(ref)

        return ref


    @property
    def ref(self):
        return lambda x: self._ref(Reference, x)

    @property
    def computed(self):
        return lambda x: self._ref(Computed, x)

    @property
    def value(self):
        return ReferenceWithValue


    def __iadd__(self, other: list[Component] | Component):
        if isinstance(other, list):
            self.add(*other)
        else:
            self.add(other)

        return self


    def format(self, **kwargs):
        for ref in self.needFormatReference:
            ref.setValue(**kwargs)

    def __repr__(self):
        return f'''Document:{'\n'.join([repr(c) for c in self.data])}'''

if __name__ == "__main__":
    from .component import Text

    doc = Document()
    v = doc.value
    ref = doc.ref

    doc += Text(ref("hello"))

    doc.format(hello="hello")

    print(repr(doc))

    