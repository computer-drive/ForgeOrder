from .component import Component

class Document:

    def __init__(self):
        self.components: list[Component] = []

    def __iadd__(self, other: Component):
        self.components.append(other)

        return self

    def __repr__(self):
        return f"Document(components={self.components})"

        