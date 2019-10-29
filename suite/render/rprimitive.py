# author: Kaan Eraslan
# license: see, LICENSE
# purpose: render primitive in given format

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString

from lxml import etree


class PrimitiveRenderer:
    "Base class for all primitive renderers"

    def __init__(self, primitive, primitiveType):
        assert isinstance(primitive, primitiveType)
        self.primitive = primitive


class PrimitiveXmlRenderer(PrimitiveRenderer):
    "render primitive in xml format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def renderInElement(self, tagname: str):
        raise NotImplementedError


class PrimitiveHtmlRenderer(PrimitiveXmlRenderer):
    "Render primitive in html format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def renderInLink(self):
        return self.renderInTag("a")

    def renderInParagraph(self):
        return self.renderInTag("p")


class PrimitiveJsonRenderer(PrimitiveRenderer):
    "Render Primitive in json format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def toJSON(self):
        raise NotImplementedError


class ConstraintStringRenderer:
    "Renders a constraint string in given format"

    class HtmlRenderer(PrimitiveHtmlRenderer):
        "Render Constraint String as Html"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderInElement(self, tagname: str):
            "render constraint string in tag"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            root.set("data-class", "constraint-string")
            root.set("data-constraint", self.primitive.fn.__name__)
            root.set("data-type", "primitive")
            return root

    class JsonRenderer(PrimitiveJsonRenderer):
        "Render Constraint String as Json"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)
