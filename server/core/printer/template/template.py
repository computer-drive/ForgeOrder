from .element import Element

from ..document.document import Document

class Template:
    def __init__(self):
        self.elements: list[Element] = []

    def __iadd__(self, other: Element):
        self.elements.append(other)

        return self

    def render(self, context: dict) -> Document:
        doc = Document()

        for element in self.elements:
            doc += element.render(context)

        return doc


if __name__ == '__main__':
    from .element import Text

    template = Template()

    template += Text("hello world{hello}")

    doc = template.render({"hello": "world"})
    print(doc)



    