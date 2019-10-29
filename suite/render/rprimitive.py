# author: Kaan Eraslan
# license: see, LICENSE
# purpose: render primitive in given format

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString

from lxml import etree
import json


class PrimitiveRenderer:
    "Base class for all primitive renderers"

    def __init__(self, primitive, primitiveType, classNameSep="-"):
        assert isinstance(primitive, primitiveType)
        self.primitive = primitive
        self.cnameSep = classNameSep


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
        return self.renderInElement("a")

    def renderInParagraph(self):
        return self.renderInElement("p")

    def renderInDiv(self):
        return self.renderInElement("div")


class PrimitiveJsonRenderer(PrimitiveRenderer):
    "Render Primitive in json format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def toJSON(self):
        raise NotImplementedError


class ConstraintStringRenderer:
    "Renders a constraint string in given format"

    class XmlRenderer(PrimitiveXmlRenderer):
        "Render Constraint String as Xml"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderInElement(self, tagname: str):
            "render string in xml element"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            root.set("class", "constraint" + self.cnameSep + "string")
            root.set("constraint", self.primitive.fn.__name__)
            return root

        def renderDefault(self):
            "render default representation for constraint string"
            return self.renderInElement("primitive")

    class HtmlRenderer(PrimitiveHtmlRenderer):
        "Render Constraint String as Html"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderInElement(self, tagname: str):
            "render constraint string in tag"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            root.set("data-class", "constraint" + self.cnameSep + "string")
            root.set("data-constraint", self.primitive.fn.__name__)
            root.set("data-type", "primitive")
            return root

        def renderDefault(self):
            return self.renderInDiv()

    class JsonRenderer(PrimitiveJsonRenderer):
        "Render Constraint String as Json"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderDefault(self):
            "Default representation in python dict"
            pdict = {}
            pdict["class"] = "constraint" + self.cnameSep + "string"
            pdict["constraint"] = self.primitive.fn.__name__
            pdict["type"] = "primitive"
            pdict["value"] = self.primitive.cstr
            return pdict

        def toJSON(self):
            "render default representation as json"
            return json.dumps(self.renderDefault(), indent=2, ensure_ascii=False)
