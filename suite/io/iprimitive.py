# author: Kaan Eraslan
# license: see, LICENSE
# purpose: render primitive in given format

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString

from lxml import etree
import json
import yaml


class GenericYamlMapping:
    def __init__(self, params: dict):
        self.__dict__.update(params)

    @staticmethod
    def to_yaml(dumper, data):
        tagname = data.__dict__.pop("tag")
        style = data.__dict__.pop("style")
        return dumper.represent_mapping(tagname, data.__dict__)


class GenericYamlSequence:
    def __init__(self, params: dict):
        self.__dict__.update(params)

    @staticmethod
    def to_yaml(dumper, data):
        tagname = data["tag"]
        values = data["values"]
        return dumper.represent_sequence(tagname, values)


class PrimitiveIo:
    "Base class for all primitive renderers"

    def __init__(self, primitive, primitiveType, classNameSep="-"):
        assert isinstance(primitive, primitiveType)
        self.primitive = primitive
        self.cnameSep = classNameSep


class PrimitiveXmlIo(PrimitiveIo):
    "render primitive in xml format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def to_element(self) -> etree.Element:
        raise NotImplementedError

    def from_element(self, el: etree.Element):
        raise NotImplementedError

    def __str__(self):
        return "Xml Io for primitive: " + str(self.primitive)


class PrimitiveJsonIo(PrimitiveIo):
    "Render Primitive in json format"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def toJSON(self):
        raise NotImplementedError

    def __str__(self):
        return "Json Renderer for primitive: " + str(self.primitive)


class PrimitiveYamlIo(PrimitiveIo):
    "Render primitive in yaml format"
    yaml_tag = "!Primitive"

    def __init__(self, primitive, primitiveType):
        super().__init__(primitive, primitiveType)

    def to_yaml(self):
        "dump primitive object to yaml"
        raise NotImplementedError

    def from_yaml(self):
        "read primitive object from yaml"
        raise NotImplementedError

    def __str__(self):
        return "Yaml Renderer for primitive: " + str(self.primitive)


class ConstraintStringIo:
    "Io for a constraint string in given format"
    SUPPORTED = ["xml", "yaml", "json"]

    def __init__(self, cstr: ConstraintString):
        self.cstr = cstr

    class XmlIo(PrimitiveXmlIo):
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

    class JsonIo(PrimitiveJsonIo):
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
            return json.dumps(
                self.renderDefault(), indent=2, ensure_ascii=False, sort_keys=True
            )

    class YamlIo(PrimitiveYamlIo):
        "Render Constraint String as Yaml"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderDefault(self):
            "Default representation in python dict"
            pdict = {}
            pdict["class"] = "constraint" + self.cnameSep + "string"
            pdict["constraint"] = self.primitive.fn.__name__
            pdict["value"] = self.primitive.cstr
            pdict["type"] = self.yaml_tag
            return pdict

        def to_yaml(self):
            vdict = self.renderDefault()
            vdict.pop("type")
            vdict["tag"] = self.yaml_tag
            vdict["style"] = None
            gmap = GenericYamlMapping(vdict)
            yaml.add_representer(
                GenericYamlMapping, GenericYamlMapping.to_yaml, Dumper=yaml.SafeDumper
            )
            return yaml.safe_dump(gmap, allow_unicode=True)

    def getIo(self, render_format: str):
        "render constraint string in given format"
        render_format = render_format.lower()
        if render_format == self.SUPPORTED[0]:
            return self.XmlIo(self.cstr)
        elif render_format == self.SUPPORTED[1]:
            return self.YamlIo(self.cstr)
        elif render_format == self.SUPPORTED[2]:
            return self.JsonIo(self.cstr)
        else:
            raise ValueError(
                render_format + " not in supported formats: " + ",".join(self.SUPPORTED)
            )

    def __str__(self):
        return "Renderer builder for constraint string: " + str(self.cstr)


class NonNumericStringIo:
    "Render a non numeric in given format"
    SUPPORTED = ["xml", "yaml", "json"]

    def __init__(self, nnstr: NonNumericString):
        self.nnstr = nnstr

    class XmlIo(PrimitiveXmlIo):
        "Render Constraint String as Xml"

        def __init__(self, cstr: NonNumericString):
            super().__init__(cstr, NonNumericString)

        def renderInElement(self, tagname: str):
            "render string in xml element"
            root = etree.Element(tagname)
            root.text = self.primitive.cstr
            cname = "non" + self.cnameSep + "numeric" + self.cnameSep + "string"
            root.set("class", cname)
            root.set("constraint", self.primitive.fn.__name__)
            return root

        def renderDefault(self):
            "render default representation for constraint string"
            return self.renderInElement("primitive")

    class JsonIo(PrimitiveJsonIo):
        "Render Constraint String as Json"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderDefault(self):
            "Default representation in python dict"
            pdict = {}
            cname = "non" + self.cnameSep + "numeric" + self.cnameSep + "string"
            pdict["class"] = cname
            pdict["constraint"] = self.primitive.fn.__name__
            pdict["type"] = "primitive"
            pdict["value"] = self.primitive.cstr
            return pdict

        def toJSON(self):
            "render default representation as json"
            return json.dumps(
                self.renderDefault(), indent=2, ensure_ascii=False, sort_keys=True
            )

    class YamlIo(PrimitiveYamlIo):
        "Render Constraint String as Yaml"

        def __init__(self, cstr: ConstraintString):
            super().__init__(cstr, ConstraintString)

        def renderDefault(self):
            "Default representation in python dict"
            pdict = {}
            cname = "non" + self.cnameSep + "numeric" + self.cnameSep + "string"
            pdict["class"] = cname
            pdict["constraint"] = self.primitive.fn.__name__
            pdict["value"] = self.primitive.cstr
            pdict["type"] = self.yaml_tag
            return pdict

        def __repr__(self):
            "reproduce yaml"
            pdict = self.renderDefault()
            mess = "(class={0}, constraint={1}, value={2})".format(
                pdict["class"], pdict["constraint"], pdict["value"]
            )
            return mess

    def getIo(self, render_format: str):
        "render constraint string in given format"
        render_format = render_format.lower()
        if render_format == self.SUPPORTED[0]:
            return self.XmlIo(self.nnstr)
        elif render_format == self.SUPPORTED[1]:
            return self.YamlIo(self.nnstr)
        elif render_format == self.SUPPORTED[2]:
            return self.JsonIo(self.nnstr)
        else:
            raise ValueError(
                render_format + " not in supported formats: " + ",".join(self.SUPPORTED)
            )
