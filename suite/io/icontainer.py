# author: Kaan Eraslan
# license: see, LICENSE
# purpose: io for containers in multiple formats

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString
from suite.dtype.primitive import ConstantString

from suite.dtype.container import BasePair, BaseTuple
from suite.dtype.container import Pair, SingleConstraintPair
from suite.dtype.container import DoubleConstraintPair
from suite.dtype.container import NestedPair
from suite.dtype.container import ConstraintNestedPair
from suite.dtype.container import ConstraintNestedSingleConstraintPair
from suite.dtype.container import StringTuple, SingleConstraintTuple
from suite.dtype.container import NonNumericTuple
from suite.dtype.container import PairTuple
from suite.dtype.container import SinglePairTuple
from suite.dtype.container import UniformPairTuple
from suite.dtype.container import MixedPair
from suite.dtype.container import SingleConstraintMixedPair
from suite.dtype.container import UniformMixedPair
from suite.dtype.container import NonNumericMixedPair
from suite.dtype.container import UniformNonNumericMixedPair

from suite.io.iprimitive import ConstraintStringIo
from suite.io.iprimitive import NonNumericStringIo

from lxml import etree
import json
import yaml
import dill


class ContainerIo:
    "Base Class for all container io"

    def __init__(self, container, containerType):

        check = True
        try:
            citer = iter(container)
        except TypeError:
            check = False
        #
        assert check
        assert isinstance(container, containerType)
        self.container = container
        self.containerType = containerType


class ContainerXmlIo(ContainerIo):
    "Container input output"

    def __init__(self, container, containerType):
        super().__init__(container, containerType)

    def member_to_element(self, member) -> etree.Element:
        raise NotImplementedError

    def to_element(self):
        raise NotImplementedError

    @classmethod
    def from_element(self, element: etree.Element):
        raise NotImplementedError


class ContainerJsonIo(ContainerIo):
    "Container input output json"

    def __init__(self, container, containerType):
        super().__init__(container, containerType)

    def to_dict(self):
        raise NotImplementedError

    def member_to_dict(self, member) -> dict:
        raise NotImplementedError

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_json(self, jsonstr: str):
        raise NotImplementedError

    def toJSON(self):
        return self.to_json()


class ContainerIoBuilder:
    "Generic io builder using supported formats"
    SUPPORTED = ["xml", "json"]

    def __init__(self, container):
        self.container = container

    class XmlIo(ContainerXmlIo):
        pass

    class JsonIo(ContainerJsonIo):
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

    def __str__(self):
        return (
            "IO builder for "
            + self.container.__class__.__name__
            + " "
            + str(self.container)
        )


class PairIo(ContainerIoBuilder):
    "Pair io"

    def __init__(self, pair: Pair):
        assert pair.isValid()
        self.pair = pair

    class XmlIo(ContainerXmlIo):
        "pair xml io"

        def __init__(self, pair):
            super().__init__(pair, Pair)

        def member_to_element(self, member):
            "transform member to element"
            el = etree.Element("primitive")

        def to_element(self):
            "transform pair to xml"
            str1 = self.container.arg1
            str2 = self.container.arg2
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            subel1 = etree.Element("member")
            subel2 = etree.Element("member")
            members = etree.Element("members")
            subel1.text = str1
            subel2.text = str2
            members.append(subel1)
            members.append(subel2)
            el.append(members)
            return el

        @classmethod
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            assert el.tag == "pair"
            assert el.get("class") == "Pair"
            members = el[0]
            arg1 = members[0]
            arg2 = members[1]
            pair = Pair(arg1.text, arg2.text)
            assert pair.isValid()
            return pair

    class JsonIo(ContainerJsonIo):
        "pair json io"

        def __init__(self, pair):
            super().__init__(pair, Pair)

        def to_dict(self):
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            member1 = {}
            member2 = {}
            member1["type"] = "member"
            member1["value"] = str1
            member2["type"] = "member"
            member2["value"] = str2
            pdict["members"] = [member1, member2]
            return pdict

        @classmethod
        def from_json(self, jsonstr: str):
            "obtain pair from json object"
            objdict = json.loads(jsonstr)
            assert objdict["type"] == "pair"
            assert objdict["class"] == "Pair"
            members = objdict["members"]
            member1 = members[0]
            member2 = members[1]
            assert member1["type"] == "member"
            assert member2["type"] == "member"
            pair = Pair(member1["value"], member2["value"])
            assert pair.isValid()
            return pair

    def getIoInstance(self, render_format: str):
        "io for pair given format"
        return self.getIoClass(render_format)(self.pair)


class SingleConstraintPairIo(ContainerIoBuilder):
    "Single Constraint Pair io"

    def __init__(self, pair: SingleConstraintPair):
        assert pair.isValid()
        self.pair = pair

    class XmlIo(ContainerXmlIo):
        "constraint Pair Io xml io"

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def member_to_element(self, member):
            ""
            cstr = member
            cstrio = ConstraintStringIo(cstr)
            ioinst = cstrio.getIoInstance("xml")
            el = ioinst.to_element()
            return el

        def to_element(self):
            "transform pair to xml"
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            myfn = dill.dumps(self.container.constfn)
            el.set("constraint", myfn.hex())
            members = etree.Element("members")
            el1 = self.member_to_element(self.container.arg1)
            el2 = self.member_to_element(self.container.arg2)
            members.append(el1)
            members.append(el2)
            el.append(members)
            return el

        @classmethod
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            assert el.tag == "pair"
            assert el.get("class") == "SingleConstraintPair"
            members = el[0]
            iocls1 = ConstraintStringIo.getIoClass("xml")
            arg1 = iocls1.from_element(members[0])
            arg2 = iocls1.from_element(members[1])
            pair = SingleConstraintPair(arg1, arg2)
            assert pair.isValid()
            return pair

    class JsonIo(ContainerJsonIo):
        "pair json io"

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def member_to_dict(self, member) -> dict:
            ""
            cstr = member
            cstrio = ConstraintStringIo(cstr)
            ioinst = cstrio.getIoInstance("json")
            return ioinst.to_dict()

        def to_dict(self):
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            myfn = dill.dumps(self.container.constfn)
            pdict["constraint"] = myfn.hex()
            member1 = self.member_to_dict(self.container.arg1)
            member2 = self.member_to_dict(self.container.arg2)
            pdict["members"] = [member1, member2]
            return pdict

        @classmethod
        def from_json(self, jsonstr: str):
            "obtain pair from json object"
            objdict = json.loads(jsonstr)
            assert objdict["type"] == "pair"
            assert objdict["class"] == "SingleConstraintPair"
            members = objdict["members"]
            member1 = members[0]
            member2 = members[1]
            iocls = ConstraintStringIo.getIoClass("json")
            cstr1 = iocls.from_json(json.dumps(member1))
            cstr2 = iocls.from_json(json.dumps(member2))
            pair = SingleConstraintPair(cstr1, cstr2)
            assert pair.isValid()
            return pair

    def getIoInstance(self, render_format: str):
        "io for pair given format"
        return self.getIoClass(render_format)(self.pair)


class DoubleConstraintPairIo(ContainerIoBuilder):
    "Double Constraint Pair io"

    def __init__(self, pair: DoubleConstraintPair):
        assert pair.isValid()
        self.pair = pair

    class XmlIo(ContainerXmlIo):
        "constraint double constraint xml io"

        def __init__(self, pair):
            super().__init__(pair, DoubleConstraintPair)

        def arg2element(self, isFirst=True):
            ""
            if isFirst:
                cstr = self.container.arg1
            else:
                cstr = self.container.arg2
            cstrio = ConstraintStringIo(cstr)
            ioinst = cstrio.getIoInstance("xml")
            el = ioinst.to_element()
            return el

        def to_element(self):
            "transform pair to xml"
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            myfn = dill.dumps(self.container.constfn)
            el.set("constraint", myfn.hex())
            members = etree.Element("members")
            el1 = self.arg2element(isFirst=True)
            el2 = self.arg2element(isFirst=False)
            members.append(el1)
            members.append(el2)
            el.append(members)
            return el

        @classmethod
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            assert el.tag == "pair"
            assert el.get("class") == "SingleConstraintPair"
            members = el[0]
            iocls1 = ConstraintStringIo.getIoClass("xml")
            arg1 = iocls1.from_element(members[0])
            arg2 = iocls1.from_element(members[1])
            pair = SingleConstraintPair(arg1, arg2)
            assert pair.isValid()
            return pair

    class JsonIo(ContainerJsonIo):
        "pair json io"

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def arg2dict(self, isFirst=True):
            ""
            if isFirst:
                cstr = self.container.arg1
            else:
                cstr = self.container.arg2
            cstrio = ConstraintStringIo(cstr)
            ioinst = cstrio.getIoInstance("json")
            return ioinst.to_dict()

        def to_dict(self):
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            myfn = dill.dumps(self.container.constfn)
            pdict["constraint"] = myfn.hex()
            member1 = self.arg2dict(isFirst=True)
            member2 = self.arg2dict(isFirst=False)
            pdict["members"] = [member1, member2]
            return pdict

        @classmethod
        def from_json(self, jsonstr: str):
            "obtain pair from json object"
            objdict = json.loads(jsonstr)
            assert objdict["type"] == "pair"
            assert objdict["class"] == "SingleConstraintPair"
            members = objdict["members"]
            member1 = members[0]
            member2 = members[1]
            iocls = ConstraintStringIo.getIoClass("json")
            cstr1 = iocls.from_json(json.dumps(member1))
            cstr2 = iocls.from_json(json.dumps(member2))
            pair = SingleConstraintPair(cstr1, cstr2)
            assert pair.isValid()
            return pair

    def getIoInstance(self, render_format: str):
        "io for pair given format"
        return self.getIoClass(render_format)(self.pair)
