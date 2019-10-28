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


class PrimitiveHtmlRenderer(PrimitiveRenderer):
    "Render primitive in html format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def renderInTag(self, tagname: str):
        raise NotImplementedError

    def renderInLink(self):
        return self.renderInTag("a")

    def renderInParagraph(self):
        return self.renderInTag("p")


class PrimitiveJsonRenderer(PrimitiveRenderer):
    "Render Primitive in json format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)


class ConstraintStringRenderer:
    "Renders a constraint string in given format"
    class HtmlRenderer(PrimitiveHtmlRenderer):
        "Render Constraint String as Html"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderInTag(self, tagname: str):
            "render constraint string in tag"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            root.set("data-class", "constraint-string")
            root.set("data-constraint", self.primitive.fn.__name__)
            return root
