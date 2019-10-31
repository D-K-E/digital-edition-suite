# author: Kaan Eraslan
# license: see, LICENSE
# purpose: io for primitives in multiple formats

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString

from lxml import etree
import json
import yaml
import pickle
import dill


class PrimitiveIo:
    "Base class for all primitive io"

    def __init__(self, primitive, primitiveType, classNameSep="-"):
        assert isinstance(primitive, primitiveType)
        self.primitive = primitive
        self.primitiveType = primitiveType


class PrimitiveXmlIo(PrimitiveIo):
    "io primitive in xml format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def to_element(self) -> etree.Element:
        raise NotImplementedError

    @classmethod
    def from_element(self, el: etree.Element):
        raise NotImplementedError

    def __str__(self):
        return "Xml Io for primitive: " + str(self.primitive)


class PrimitiveJsonIo(PrimitiveIo):
    "Io Primitive in json format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def to_dict(self):
        raise NotImplementedError

    def to_json(self):
        objdict = self.to_dict()
        return json.dumps(objdict, ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_json(self, jsonstr: str):
        raise NotImplementedError

    def toJSON(self):
        return self.to_json()

    def __str__(self):
        return "Json Renderer for primitive: " + str(self.primitive)


class ConstraintStringIo:
    "Io for a constraint string in given format"
    SUPPORTED = ["xml", "json"]

    def __init__(self, cstr: ConstraintString):
        assert cstr.isValid()
        self.cstr = cstr

    class XmlIo(PrimitiveXmlIo):
        "Io Constraint String as Xml"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderInElement(self, tagname: str):
            "render string in xml element"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            root.set("class", self.primitiveType.__name__)
            myfn = dill.dumps(self.primitive.fn)
            root.set("constraint", myfn.hex())
            return root

        def to_element(self):
            "render default representation for constraint string"
            return self.renderInElement("primitive")

        @classmethod
        def from_element(cls, element: etree.Element):
            ""
            assert element.get("class") == "ConstraintString"
            assert element.tag == "primitive"
            myfn = bytes.fromhex(element.get("constraint"))
            myfn = dill.loads(myfn)
            cstr = element.text
            cstr = ConstraintString(cstr, constraint=myfn)
            assert cstr.isValid()
            return cstr

    class JsonIo(PrimitiveJsonIo):
        "Render Constraint String as Json"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def to_dict(self):
            "Default representation in python dict"
            pdict = {}
            pdict["class"] = self.primitiveType.__name__
            pdict["constraint"] = dill.dumps(self.primitive.fn).hex()
            pdict["type"] = "primitive"
            pdict["value"] = self.primitive.cstr
            return pdict

        @classmethod
        def from_json(cls, jsonstr: str):
            "construct object from json"
            objdict = json.loads(jsonstr)
            assert objdict["class"] == "ConstraintString"
            assert objdict["type"] == "primitive"
            myfn = bytes.fromhex(objdict["constraint"])
            myfn = dill.loads(myfn)
            cstr = ConstraintString(objdict["value"], myfn)
            assert cstr.isValid()
            return cstr

    def getIoInstance(self, render_format: str):
        "render constraint string in given format"
        return self.getIoClass(render_format)(self.cstr)

    @classmethod
    def getIoClass(cls, render_format: str):
        render_format = render_format.lower()
        if render_format == cls.SUPPORTED[0]:
            return cls.XmlIo
        elif render_format == cls.SUPPORTED[1]:
            return cls.JsonIo
        else:
            raise ValueError(
                render_format + " not in supported formats: " + ",".join(cls.SUPPORTED)
            )

    def __str__(self):
        return "Renderer builder for constraint string: " + str(self.cstr)


class NonNumericStringIo:
    "Render a non numeric in given format"
    SUPPORTED = ["xml", "json"]

    def __init__(self, nnstr: NonNumericString):
        assert nnstr.isValid()
        self.nnstr = nnstr

    class XmlIo(PrimitiveXmlIo):
        "Io Constraint String as Xml"

        def __init__(self, cstr: NonNumericString):
            super().__init__(cstr, NonNumericString)

        def renderInElement(self, tagname: str):
            "render string in xml element"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            root.set("class", self.primitiveType.__name__)
            myfn = dill.dumps(self.primitive.fn)
            root.set("constraint", myfn.hex())
            return root

        def to_element(self):
            "render default representation for constraint string"
            return self.renderInElement("primitive")

        @classmethod
        def from_element(cls, element: etree.Element):
            ""
            assert element.get("class") == "NonNumericString"
            assert element.tag == "primitive"
            cstr = element.text
            nnstr = NonNumericString(cstr)
            assert nnstr.isValid()
            return nnstr

    class JsonIo(PrimitiveJsonIo):
        "Io Constraint String as Json"

        def __init__(self, cstr: NonNumericString):
            super().__init__(cstr, NonNumericString)

        def to_dict(self):
            "Default representation in python dict"
            pdict = {}
            pdict["class"] = self.primitiveType.__name__
            pdict["constraint"] = dill.dumps(self.primitive.fn).hex()
            pdict["type"] = "primitive"
            pdict["value"] = self.primitive.cstr
            return pdict

        @classmethod
        def from_json(cls, jsonstr: str):
            "construct object from json"
            objdict = json.loads(jsonstr)
            assert objdict["class"] == "NonNumericString"
            assert objdict["type"] == "primitive"
            nnstr = NonNumericString(objdict["value"])
            assert nnstr.isValid()
            return nnstr

    def getIoInstance(self, render_format: str):
        "render constraint string in given format"
        return self.getIoClass(render_format)(self.nnstr)

    @classmethod
    def getIoClass(cls, render_format: str):
        render_format = render_format.lower()
        if render_format == cls.SUPPORTED[0]:
            return cls.XmlIo
        elif render_format == cls.SUPPORTED[1]:
            return cls.JsonIo
        else:
            raise ValueError(
                render_format + " not in supported formats: " + ",".join(cls.SUPPORTED)
            )

    def __str__(self):
        return "Renderer builder for constraint string: " + str(self.cstr)
