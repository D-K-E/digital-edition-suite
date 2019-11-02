# author: Kaan Eraslan
# license: see, LICENSE
# purpose: io for primitives in multiple formats

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import ConstantString
from suite.dtype.primitive import NonNumericString
from suite.dtype.primitive import PrimitiveMaker

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


class PrimitiveIoBuilder:
    "Base Io builder for available primitive io objects"
    SUPPORTED = ["xml", "json"]

    class XmlIo:
        pass

    class JsonIo:
        pass

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


class ConstantStringIo(PrimitiveIoBuilder):
    "Io builder for constant string primitive"

    def __init__(self, mystr: ConstantString):
        super().__init__()
        assert mystr.isValid()
        self.constr = mystr

    class XmlIo(PrimitiveXmlIo):
        def __init__(self, mystr: ConstantString):
            super().__init__(mystr, ConstantString)

        def to_element(self) -> etree.Element:
            "io default representation for constant string"
            root = etree.Element("primitive")
            root.text = str(self.primitive)
            root.set("class", self.primitiveType.__name__)
            return root

        @classmethod
        def from_element(cls, el: etree.Element) -> ConstantString:
            "from element"
            assert el.get("class") == "ConstantString"
            elstr = el.text
            maker = PrimitiveMaker("constant string")
            constr = maker.make(mystr=elstr)
            return constr

    class JsonIo(PrimitiveJsonIo):
        def __init__(self, mystr: ConstantString):
            super().__init__(mystr, ConstantString)

        def to_dict(self):
            "render as a dict"
            pdict = {}
            pdict["class"] = self.primitiveType.__name__
            pdict["type"] = "primitive"
            pdict["value"] = str(self.primitive)
            return pdict

        @classmethod
        def from_dict(cls, cdict: dict) -> ConstantString:
            "render constant string from dict"
            assert cdict["class"] == "ConstantString"
            assert cdict["type"] == "primitive"
            maker = PrimitiveMaker("constant string")
            constr = maker.make(mystr=cdict["value"])
            return constr

        @classmethod
        def from_json(cls, jsonstr: str) -> ConstantString:
            "obtain from constant string"
            obdict = json.loads(jsonstr)
            return cls.from_dict(obdict)

    def getIoInstance(self, render_format: str):
        "render constraint string in given format"
        return self.getIoClass(render_format)(self.constr)

    def __repr__(self):
        return "Io builder for: " + repr(self.constr)


class ConstraintStringIo(PrimitiveIoBuilder):
    "Io for a constraint string in given format"
    SUPPORTED = ["xml", "json"]

    def __init__(self, cstr: ConstraintString):
        assert cstr.isValid()
        self.cstr = cstr

    class XmlIo(PrimitiveXmlIo):
        "Io Constraint String as Xml"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        @staticmethod
        def text_to_constant_string(text: str) -> ConstantString:
            "transform string to constant string"
            maker = PrimitiveMaker("constant string")
            return maker.make(mystr=text)

        def to_element(self):
            "render default representation for constraint string"
            root = etree.Element("primitive")
            root.text = str(self.primitive)
            root.set("class", self.primitiveType.__name__)
            myfn = dill.dumps(self.primitive.fn)
            root.set("constraint", myfn.hex())
            return root

        @classmethod
        def from_element(cls, element: etree.Element):
            ""
            assert element.get("class") == "ConstraintString"
            assert element.tag == "primitive"
            myfn = bytes.fromhex(element.get("constraint"))
            myfn = dill.loads(myfn)
            cstr = element.text
            constr = cls.text_to_constant_string(cstr)
            maker = PrimitiveMaker("constraint string")
            return maker.make(mystr=constr, fnc=myfn)

    class JsonIo(PrimitiveJsonIo):
        "Render Constraint String as Json"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        @classmethod
        def constant_string_to_dict(cls, constring: ConstraintString):
            "transform constant string to dict"
            constr = constring.cstr
            consio = ConstantStringIo(constr)
            ionst = consio.getIoInstance("json")
            jstr = ionst.to_json()
            return json.loads(jstr)

        def to_dict(self):
            "Default representation in python dict"
            pdict = {}
            pdict["class"] = self.primitiveType.__name__
            pdict["constraint"] = dill.dumps(self.primitive.fn).hex()
            pdict["type"] = "primitive"
            pdict["value"] = self.constant_string_to_dict(self.primitive)
            return pdict

        @classmethod
        def dict_to_constant_string(cls, consdict: dict):
            "transform dict representation to constant string"
            consio = ConstantStringIo
            iocls = consio.getIoClass("json")
            constr = iocls.from_dict(consdict)
            return constr

        @classmethod
        def from_dict(cls, cdict: dict) -> ConstraintString:
            "transform dict to ConstraintString"
            assert cdict["class"] == "ConstraintString"
            assert cdict["type"] == "primitive"
            myfn = bytes.fromhex(cdict["constraint"])
            myfnc = dill.loads(myfn)
            constrdict = cdict["value"]
            constr = cls.dict_to_constant_string(constrdict)
            maker = PrimitiveMaker("constraint string")
            return maker.make(mystr=constr, fnc=myfnc)

        @classmethod
        def from_json(cls, jsonstr: str):
            "construct object from json"
            objdict = json.loads(jsonstr)
            return cls.from_dict(objdict)

    def getIoInstance(self, render_format: str):
        "render constraint string in given format"
        return self.getIoClass(render_format)(self.cstr)

    def __repr__(self):
        return "Io builder for: " + repr(self.cstr)


class NonNumericStringIo(PrimitiveIoBuilder):
    "Render a non numeric in given format"
    SUPPORTED = ["xml", "json"]

    def __init__(self, nnstr: NonNumericString):
        assert nnstr.isValid()
        self.nnstr = nnstr

    class XmlIo(PrimitiveXmlIo):
        "Io Constraint String as Xml"

        def __init__(self, cstr: NonNumericString):
            super().__init__(cstr, NonNumericString)

        @staticmethod
        def text_to_constant_string(text: str) -> ConstantString:
            "transform string to constant string"
            maker = PrimitiveMaker("constant string")
            return maker.make(mystr=text)

        def to_element(self):
            "render default representation for constraint string"
            root = etree.Element("primitive")
            root.text = str(self.primitive)
            root.set("class", self.primitiveType.__name__)
            myfn = dill.dumps(self.primitive.fn)
            root.set("constraint", myfn.hex())
            return root

        @classmethod
        def from_element(cls, element: etree.Element):
            ""
            assert element.get("class") == "NonNumericString"
            assert element.tag == "primitive"
            cstr = element.text
            constr = cls.text_to_constant_string(cstr)
            maker = PrimitiveMaker("non numeric string")
            return maker.make(mystr=constr)

    class JsonIo(PrimitiveJsonIo):
        "Io Constraint String as Json"

        def __init__(self, cstr: NonNumericString):
            super().__init__(cstr, NonNumericString)

        @classmethod
        def constant_string_to_dict(cls, conststr: NonNumericString):
            "transform constant string of a constraint string to dict"
            constr = conststr.cstr
            consio = ConstantStringIo(constr)
            ionst = consio.getIoInstance("json")
            jstr = ionst.to_json()
            return json.loads(jstr)

        def to_dict(self):
            "Default representation in python dict"
            pdict = {}
            pdict["class"] = self.primitiveType.__name__
            pdict["constraint"] = dill.dumps(self.primitive.fn).hex()
            pdict["type"] = "primitive"
            pdict["value"] = self.constant_string_to_dict(self.primitive)
            return pdict

        @classmethod
        def dict_to_constant_string(cls, consdict: dict):
            "transform dict representation to constant string"
            consio = ConstantStringIo
            iocls = consio.getIoClass("json")
            constr = iocls.from_dict(consdict)
            assert constr.isValid()
            return constr

        @classmethod
        def from_json(cls, jsonstr: str):
            "construct object from json"
            objdict = json.loads(jsonstr)
            assert objdict["class"] == "NonNumericString"
            assert objdict["type"] == "primitive"
            constr = cls.dict_to_constant_string(objdict["value"])
            maker = PrimitiveMaker("non numeric string")
            return maker.make(mystr=constr)

    def getIoInstance(self, render_format: str):
        "render constraint string in given format"
        return self.getIoClass(render_format)(self.nnstr)

    def __repr__(self):
        return "Io builder for " + repr(self.cstr)
