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
from typing import List, Dict


def dict_dump(mdict: dict):
    "dump dictionaries in homogeneous fashion"
    return json.dumps(mdict, ensure_ascii=False, indent=2, sort_keys=True)


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
        "Check if given object value correspond to wanted value"
        if objval != wantedVal:
            raise ValueError(messPrefix + objval + " it must be: " + wantedVal)
        return

    def add_members_to_parent(self, parent, members):
        "add members to parent set"
        for member in members:
            parent.append(member)
        return parent

    def member_to_dict(self, member) -> dict:
        "transform member to dict"
        raise NotImplementedError

    def dict_to_unit(self, mdict: dict):
        "transform dictionary to given serialization unit"
        raise NotImplementedError

    def member_to_unit(self, member):
        "transform member to serialization unit"
        mdict = self.member_to_dict(member)
        unit = self.dict_to_unit(mdict)
        return unit

    @classmethod
    def unit_to_dict(cls, unit):
        "transform serialization unit to dictionary"
        raise NotImplementedError

    @classmethod
    def dict_to_member(cls, mdict: dict):
        "transform dictionary to member type"
        raise NotImplementedError

    @classmethod
    def unit_to_member(cls, unit):
        "transform serialization unit into member type"
        mdict = cls.unit_to_dict(unit)
        member = cls.dict_to_member(mdict)
        return member

    @classmethod
    def check_container_unit(cls, cunit) -> bool:
        "check if given serialization unit conforms to expected container"
        raise NotImplementedError

    def to_dict(self) -> dict:
        "transform serialization container unit dictionary"
        raise NotImplementedError


class _ContainerXmlIo(_ContainerIo):
    "Container input output"
    cmaker = ContainerMaker("")
    pmaker = PrimitiveMaker("")
    primitiveIo = ConstantStringIo.getIoClass("xml")

    def __init__(self, container, containerType):
        super().__init__(container, containerType)

    @classmethod
    def element_to_dict(cls, el: etree.Element) -> dict:
        "transform element to dict"
        eldict = el.attrib
        eldict["text"] = el.text
        eldict["tag"] = el.tag
        return eldict

    @classmethod
    def unit_to_member(cls, el: etree.Element):
        "transform element to member"
        return cls.primitiveIo.from_element(el)

    def member_to_unit(self, member: ConstantString) -> etree.Element:
        "transform member to element"
        consio = self.primitiveIo(member)
        return consio.to_element()

    def member_to_dict(self, member: ConstantString) -> dict:
        "transform member to element"
        consio = self.primitiveIo(member)
        return consio.to_dict()


class _ContainerJsonIo(_ContainerIo):
    "Container input output json"
    cmaker = ContainerMaker("")
    pmaker = PrimitiveMaker("")
    primitiveIo = ConstantStringIo.getIoClass("json")

    def __init__(self, container, containerType):
        super().__init__(container, containerType)

    @classmethod
    def json_to_dict(cls, jsonstr: str) -> dict:
        return json.loads(jsonstr)

    def member_to_unit(self, member: ConstantString) -> dict:
        consio = self.primitiveIo(member)
        return consio.to_dict()

    @classmethod
    def unit_to_member(cls, cdict: dict):
        return cls.primitiveIo.from_dict(cdict)

    def to_json(self):
        return dict_dump(self.to_dict())

    def toJSON(self):
        return self.to_json()


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

        def to_element(self):
            "transform pair to xml"
            str1 = self.container.arg1
            str2 = self.container.arg2
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            el1 = self.member_to_unit(str1)
            el2 = self.member_to_unit(str2)
            self.add_members_to_parent(el, [el1, el2])
            return el

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
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            eltag = el.tag
            elclass = el.get("class")
            cls.check_value_error(eltag, "pair", "Given element tag: ")
            cls.check_value_error(elclass, "Pair", "Given element class: ")
            arg1 = cls.unit_to_member(el[0])
            arg2 = cls.unit_to_member(el[1])
            pair = cls.cmaker.make(arg1=arg1, arg2=arg2)
            return pair

    class JsonIo(_ContainerJsonIo):
        "pair json io"
        cmaker = ContainerMaker("pair")
        pmaker = PrimitiveMaker(choice="constant string")
        primitiveIo = ConstantStringIo.getIoClass("json")

        def __init__(self, pair):
            super().__init__(pair, Pair)

        def to_dict(self) -> dict:
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            member1 = self.member_to_unit(str1)
            member2 = self.member_to_unit(str2)
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
            member1 = cls.unit_to_member(members[0])
            member2 = cls.unit_to_member(members[1])
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

        def to_dict(self) -> dict:
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            pdict["constraint"] = dill.dumps(self.container.constfn).hex()
            member1 = self.member_to_dict(str1)
            member2 = self.member_to_dict(str2)
            pdict["members"] = []
            self.add_members_to_parent(pdict["members"], [member1, member2])
            return pdict

        @classmethod
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            eltag = el.tag
            elclass = el.get("class")
            cls.check_value_error(eltag, "pair", "Given element tag: ")
            cls.check_value_error(
                elclass, "SingleConstraintPair", "Given element class: "
            )
            arg1 = cls.unit_to_member(el[0])
            arg2 = cls.unit_to_member(el[1])
            pair = cls.cmaker.make(arg1=arg1, arg2=arg2)
            return pair

        @classmethod
        def from_dict(cls, cdict: dict):
            "obtain pair from dict"
            objtype = cdict.get("type", "")
            objclass = cdict.get("class", "")
            cls.check_value_error(objtype, "pair", "Given object type: ")
            cls.check_value_error(
                objclass, "DoubleConstraintPair", "Given object class: "
            )
            members = cdict["members"]
            member1 = cls.unit_to_member(members[0])
            member2 = cls.unit_to_member(members[1])
            pair = cls.cmaker.make(arg1=member1, arg2=member2)
            return pair

    class JsonIo(_ContainerJsonIo):
        "pair json io"
        cmaker = ContainerMaker("single constraint pair")
        pmaker = PrimitiveMaker(choice="constraint string")
        primitiveIo = ConstraintStringIo.getIoClass("json")

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def to_dict(self):
            "to dict pair"
            str1 = self.container.arg1
            str2 = self.container.arg2
            pdict = {}
            pdict["class"] = self.containerType.__name__
            pdict["type"] = "pair"
            myfn = dill.dumps(self.container.constfn)
            pdict["constraint"] = myfn.hex()
            member1 = self.member_to_unit(self.container.arg1)
            member2 = self.member_to_unit(self.container.arg2)
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
            cls.check_value_error(objtype, "pair", "Given element tag: ")
            cls.check_value_error(
                objclass, "SingleConstraintPair", "Given element class: "
            )
            members = cdict["members"]
            member1 = cls.unit_to_member(members[0])
            member2 = cls.unit_to_member(members[1])
            pair = cls.cmaker.make(arg1=member1, arg2=member2)
            return pair

    def getIoInstance(self, render_format: str):
        "io for pair given format"
        return self.getIoClass(render_format)(self.container)


class DoubleConstraintPairIo(_ContainerIoBuilder):
    "Double Constraint Pair io"

    def __init__(self, pair: DoubleConstraintPair):
        super().__init__(pair)

    class XmlIo(_ContainerXmlIo):
        "constraint double constraint xml io"
        cmaker = ContainerMaker("double constraint pair")
        pmaker = PrimitiveMaker(choice="constraint string")
        primitiveIo = ConstantStringIo.getIoClass("xml")

        def __init__(self, pair):
            super().__init__(pair, DoubleConstraintPair)

        def to_element(self):
            "transform pair to xml"
            str1 = self.container.arg1
            str2 = self.container.arg2
            el = etree.Element("pair")
            el.set("class", self.containerType.__name__)
            el1 = self.member_to_unit(str1)
            el2 = self.member_to_unit(str2)
            self.add_members_to_parent(el, [el1, el2])
            return el

        def to_dict(self):
            "transform pair to dict"
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
        def from_dict(cls, cdict: dict):
            "obtain pair from dict"
            objtype = cdict.get("type", "")
            objclass = cdict.get("class", "")
            cls.check_value_error(objtype, "pair", "Given object type: ")
            cls.check_value_error(
                objclass, "DoubleConstraintPair", "Given object class: "
            )
            members = cdict["members"]
            member1 = cls.unit_to_member(members[0])
            member2 = cls.unit_to_member(members[1])
            pair = cls.cmaker.make(arg1=member1, arg2=member2)
            return pair

        @classmethod
        def from_element(cls, el: etree.Element):
            "Obtain pair from element"
            eltag = el.tag
            elclass = el.get("class")
            cls.check_value_error(eltag, "pair", "Given element tag: ")
            cls.check_value_error(
                elclass, "DoubleConstraintPair", "Given element class: "
            )
            arg1 = cls.unit_to_member(el[0])
            arg2 = cls.unit_to_member(el[1])
            pair = cls.cmaker.make(arg1=arg1, arg2=arg2)
            return pair

            iocls1 = ConstraintStringIo.getIoClass("xml")
            arg1 = iocls1.from_element(members[0])
            arg2 = iocls1.from_element(members[1])
            pair = SingleConstraintPair(arg1, arg2)
            assert pair.isValid()
            return pair

    class JsonIo(_ContainerJsonIo):
        "pair json io"
        cmaker = ContainerMaker("double constraint pair")
        pmaker = PrimitiveMaker(choice="constraint string")
        primitiveIo = ConstantStringIo.getIoClass("json")

        def __init__(self, pair):
            super().__init__(pair, SingleConstraintPair)

        def to_dict(self):
            "transform pair to dict"
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
            cls.check_value_error(
                objclass, "DoubleConstraintPair", "Given object class: "
            )
            members = cdict["members"]
            member1 = cls.unit_to_member(members[0])
            member2 = cls.unit_to_member(members[1])
            pair = cls.cmaker.make(arg1=member1, arg2=member2)
            return pair

    def getIoInstance(self, render_format: str):
        "io for pair given format"
        return self.getIoClass(render_format)(self.container)
