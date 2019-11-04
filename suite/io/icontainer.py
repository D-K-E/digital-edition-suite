# author: Kaan Eraslan
# license: see, LICENSE
# purpose: io for containers in multiple formats

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString
from suite.dtype.primitive import ConstantString
from suite.dtype.primitive import PrimitiveMaker

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
from suite.dtype.container import ContainerMaker

from suite.io.iprimitive import ConstantStringIo
from suite.io.iprimitive import ConstraintStringIo
from suite.io.iprimitive import NonNumericStringIo

from lxml import etree
import json
import dill


class _ContainerIo:
    "Base Class for all container io"

    def __init__(self, container, containerType):

        check = True
        try:
            citer = iter(container)
        except TypeError:
            check = False
        #
        if not check:
            raise ValueError("Container is not iterable")
        if not isinstance(container, containerType):
            raise TypeError(
                "Container:"
                + str(container)
                + " is not an instance of given container type: "
                + containerType.__name__
            )
        self.container = container
        self.containerType = containerType

    @classmethod
    def check_value_error(cls, objval: str, wantedVal: str, messPrefix: str):
        if objval != wantedVal:
            raise ValueError(messPrefix + objval + " it must be: " + wantedVal)
        return

    def add_members_to_parent(self, parent, members):
        ""
        for member in members:
            parent.append(member)
        return parent


class _ContainerXmlIo(_ContainerIo):
    "Container input output"

    def __init__(self, container, containerType):
        super().__init__(container, containerType)

    def member_to_element(self, member) -> etree.Element:
        raise NotImplementedError

    def to_element(self):
        raise NotImplementedError

    @classmethod
    def element_to_member(cls, member: etree.Element):
        raise NotImplementedError

    @classmethod
    def from_element(cls, element: etree.Element):
        raise NotImplementedError


class _ContainerJsonIo(_ContainerIo):
    "Container input output json"

    def __init__(self, container, containerType):
        super().__init__(container, containerType)

    def to_dict(self):
        raise NotImplementedError

    def member_to_dict(self, member) -> dict:
        raise NotImplementedError

    @classmethod
    def dict_to_member(cls, member: dict):
        raise NotImplementedError

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_json(self, jsonstr: str):
        raise NotImplementedError

    def toJSON(self):
        return self.to_json()

    @classmethod
    def from_dict(self, adict: dict):
        raise NotImplementedError


class _ContainerIoBuilder:
    "Generic io builder using supported formats"
    SUPPORTED = ["xml", "json"]

    def __init__(self, container):
        if not container.isValid():
            raise ValueError("Container: " + str(container) + " is not valid")
        self.container = container

    class XmlIo(_ContainerXmlIo):
        pass

    class JsonIo(_ContainerJsonIo):
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

    def __repr__(self):
        return (
            "IO builder for "
            + self.container.__class__.__name__
            + " "
            + repr(self.container)
        )


class PairIo(_ContainerIoBuilder):
    "Pair io"

    def __init__(self, pair: Pair):
        super().__init__(pair)

    class XmlIo(_ContainerXmlIo):
        "pair xml io"
        cmaker = ContainerMaker("pair")
        pmaker = PrimitiveMaker(choice="constant string")
        primitiveIo = ConstantStringIo.getIoClass("xml")

        def __init__(self, pair):
            super().__init__(pair, Pair)

        def member_to_element(self, member: ConstantString) -> etree.Element:
            "transform member to element"
            consio = self.primitiveIo(member)
            return consio.to_element()

        @classmethod
        def element_to_member(cls, el: etree.Element):
            "transform element to member"
            return cls.primitiveIo.from_element(el)

        def to_element(self):
            "transform pair to xml"
            str1 = self.container.arg1
            str2 = self.container.arg2
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            el1 = self.member_to_element(str1)
            el2 = self.member_to_element(str2)
            self.add_members_to_parent(el, [el1, el2])
            return el

        @classmethod
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            eltag = el.tag
            elclass = el.get("class")
            cls.check_value_error(eltag, "pair", "Given element tag: ")
            cls.check_value_error(elclass, "Pair", "Given element class: ")
            arg1 = cls.element_to_member(el[0])
            arg2 = cls.element_to_member(el[1])
            pair = cls.cmaker.make(arg1=arg1, arg2=arg2)
            return pair

    class JsonIo(_ContainerJsonIo):
        "pair json io"
        cmaker = ContainerMaker("pair")
        pmaker = PrimitiveMaker(choice="constant string")
        primitiveIo = ConstantStringIo.getIoClass("json")

        def __init__(self, pair):
            super().__init__(pair, Pair)

        def member_to_dict(self, member: ConstantString) -> dict:
            consio = self.primitiveIo(member)
            ioinst = consio.getIoInstance("json")
            return ioinst.to_dict()

        @classmethod
        def dict_to_member(cls, cdict: dict) -> ConstantString:
            return cls.primitiveIo.from_dict(cdict)

        def to_dict(self) -> dict:
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            member1 = self.member_to_dict(str1)
            member2 = self.member_to_dict(str2)
            pdict["members"] = []
            self.add_members_to_parent(pdict["members"], [member1, member2])
            return pdict

        @classmethod
        def from_json(cls, jsonstr: str):
            "obtain pair from json object"
            objdict = json.loads(jsonstr)
            return cls.from_dict(objdict)

        @classmethod
        def from_dict(cls, cdict: dict):
            "obtain pair from dict"
            objtype = cdict.get("type", "")
            objclass = cdict.get("class", "")
            cls.check_value_error(objtype, "pair", "Given object type: ")
            cls.check_value_error(objclass, "Pair", "Given object class: ")
            members = cdict["members"]
            member1 = cls.dict_to_member(members[0])
            member2 = cls.dict_to_member(members[1])
            pair = cls.cmaker.make(arg1=member1, arg2=member2)
            return pair

    def getIoInstance(self, render_format: str):
        "io for pair given format"
        return self.getIoClass(render_format)(self.container)


class SingleConstraintPairIo(_ContainerIoBuilder):
    "Single Constraint Pair io"

    def __init__(self, pair: SingleConstraintPair):
        super().__init__(pair)

    class XmlIo(_ContainerXmlIo):
        "constraint Pair Io xml io"
        cmaker = ContainerMaker("single constraint pair")
        pmaker = PrimitiveMaker(choice="constraint string")
        primitiveIo = ConstraintStringIo.getIoClass("xml")

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def member_to_element(self, member):
            ""
            return self.primitiveIo(member).to_element()

        @classmethod
        def element_to_member(cls, el: etree.Element):
            return cls.primitiveIo.from_element(el)

        def to_element(self):
            "transform pair to xml"
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            myfn = dill.dumps(self.container.constfn)
            el.set("constraint", myfn.hex())
            el1 = self.member_to_element(self.container.arg1)
            el2 = self.member_to_element(self.container.arg2)
            self.add_members_to_parent(el, [el1, el2])
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

    class JsonIo(_ContainerJsonIo):
        "pair json io"
        cmaker = ContainerMaker("single constraint pair")
        pmaker = PrimitiveMaker(choice="constraint string")
        primitiveIo = ConstraintStringIo.getIoClass("json")

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def member_to_dict(self, member) -> dict:
            ""
            cstrio = self.primitiveIo(member)
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


class DoubleConstraintPairIo(_ContainerIoBuilder):
    "Double Constraint Pair io"

    def __init__(self, pair: DoubleConstraintPair):
        assert pair.isValid()
        self.pair = pair

    class XmlIo(_ContainerXmlIo):
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

    class JsonIo(_ContainerJsonIo):
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
