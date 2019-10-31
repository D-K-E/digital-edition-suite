# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from lxml import etree
import json
import dill

from suite.dtype.primitive import ConstraintString, NonNumericString
from suite.io.iprimitive import ConstraintStringIo
from suite.io.iprimitive import NonNumericStringIo
from suite.io.icontainer import PairIo, SingleConstraintPairIo

from suite.dtype.container import Pair
from suite.dtype.container import SingleConstraintPair


class TestIoContainer(unittest.TestCase):
    "test io container module"

    def setUp(self):
        "setup small data"

        def lfn(x: str):
            return x.islower()

        self.mycstr = ConstraintString("my valid constraint string", lfn)
        self.myfn = dill.dumps(self.mycstr.fn)
        self.mynnstr = NonNumericString("my valid non numeric string")
        self.mynnfn = dill.dumps(self.mynnstr.fn)
        self.pair = Pair("mystr1", "mystr2")
        mystr1 = ConstraintString("my true string", lfn)
        mystr2 = ConstraintString("my another true string", lfn)
        self.scpair1 = SingleConstraintPair(str1=mystr1, str2=mystr2)

    def test_pair_io_to_xml(self):
        "test pair io"
        pio = PairIo(self.pair)
        ionst = pio.getIoInstance("xml")
        el1 = ionst.to_element()
        el = etree.Element("pair")
        el.set("class", Pair.__name__)
        subel1 = etree.Element("member")
        subel2 = etree.Element("member")
        members = etree.Element("members")
        subel1.text = self.pair.arg1
        subel2.text = self.pair.arg2
        members.append(subel1)
        members.append(subel2)
        el.append(members)
        self.assertEqual(el.tag, el1.tag)
        self.assertEqual(el.text, el1.text)
        self.assertEqual(el.attrib, el1.attrib)

    def test_pair_io_to_json(self):
        "test pair io"
        pio = PairIo(self.pair)
        ionst = pio.getIoInstance("json")
        el1 = ionst.to_json()
        mydict = ionst.to_dict()
        pdict = {}
        pdict["class"] = Pair.__name__
        pdict["type"] = "pair"
        member1 = {}
        member2 = {}
        member1["type"] = "member"
        member1["value"] = self.pair.arg1
        member2["type"] = "member"
        member2["value"] = self.pair.arg2
        pdict["members"] = [member1, member2]
        pjson = json.dumps(pdict, ensure_ascii=True, indent=2, sort_keys=True)
        self.assertEqual(pjson, el1)
        self.assertEqual(pdict, mydict)

    def test_pair_io_from_xml(self):
        "test pair io"
        pio = PairIo(self.pair)
        ionst = pio.getIoClass("xml")
        el = etree.Element("pair")
        el.set("class", Pair.__name__)
        subel1 = etree.Element("member")
        subel2 = etree.Element("member")
        members = etree.Element("members")
        subel1.text = self.pair.arg1
        subel2.text = self.pair.arg2
        members.append(subel1)
        members.append(subel2)
        el.append(members)

        el1 = ionst.from_element(el)
        self.assertEqual(el1, self.pair)

    def test_pair_io_from_json(self):
        "test pair io"
        pio = PairIo(self.pair)
        ionst = pio.getIoClass("json")
        pdict = {}
        pdict["class"] = Pair.__name__
        pdict["type"] = "pair"
        member1 = {}
        member2 = {}
        member1["type"] = "member"
        member1["value"] = self.pair.arg1
        member2["type"] = "member"
        member2["value"] = self.pair.arg2
        pdict["members"] = [member1, member2]
        pjson = json.dumps(pdict, ensure_ascii=True, indent=2, sort_keys=True)
        mypair = ionst.from_json(pjson)
        self.assertEqual(mypair, self.pair)

    def test_single_constraint_pair_io_to_xml(self):
        "test pair io"

        def arg2element(myarg):
            ""
            cstrio = ConstraintStringIo(myarg)
            ioinst = cstrio.getIoInstance("xml")
            el = ioinst.to_element()
            return el

        pio = SingleConstraintPairIo(self.scpair1)
        ionst = pio.getIoInstance("xml")
        el1 = ionst.to_element()
        el = etree.Element("pair")
        el.set("class", SingleConstraintPair.__name__)
        myfn = dill.dumps(self.scpair1.constfn)
        el.set("constraint", myfn.hex())

        members = etree.Element("members")
        sel1 = arg2element(self.scpair1.arg1)
        sel2 = arg2element(self.scpair1.arg2)
        members.append(sel1)
        members.append(sel2)
        el.append(members)
        self.assertEqual(el.tag, el1.tag)
        self.assertEqual(el.text, el1.text)
        self.assertEqual(el.attrib, el1.attrib)

    def test_single_constraint_pair_io_to_json(self):
        "test pair io"

        def arg2dict(myarg):
            ""
            cstrio = ConstraintStringIo(myarg)
            ioinst = cstrio.getIoInstance("json")
            return ioinst.to_dict()

        pio = SingleConstraintPairIo(self.scpair1)
        ionst = pio.getIoInstance("json")
        el1 = ionst.to_json()
        mydict = ionst.to_dict()
        pdict = {}
        pdict["class"] = SingleConstraintPair.__name__
        pdict["type"] = "pair"
        myfn = dill.dumps(self.scpair1.constfn)
        pdict["constraint"] = myfn.hex()
        member1 = arg2dict(self.scpair1.arg1)
        member2 = arg2dict(self.scpair1.arg2)
        pdict["members"] = [member1, member2]
        pjson = json.dumps(pdict, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(pdict, mydict)
        self.assertEqual(pjson, el1)

    def test_single_constraint_pair_io_from_xml(self):
        "test pair io"

        def arg2element(myarg):
            ""
            cstrio = ConstraintStringIo(myarg)
            ioinst = cstrio.getIoInstance("xml")
            el = ioinst.to_element()
            return el

        pio = SingleConstraintPairIo
        ionst = pio.getIoClass("xml")
        el = etree.Element("pair")
        el.set("class", SingleConstraintPair.__name__)
        myfn = dill.dumps(self.scpair1.constfn)
        el.set("constraint", myfn.hex())
        members = etree.Element("members")
        e1 = arg2element(self.scpair1.arg1)
        e2 = arg2element(self.scpair1.arg2)
        members.append(e1)
        members.append(e2)
        el.append(members)
        el1 = ionst.from_element(el)
        self.assertEqual(el1, self.scpair1)

    def test_single_constraint_pair_io_from_json(self):
        "test pair io"

        def arg2dict(myarg):
            ""
            cstrio = ConstraintStringIo(myarg)
            ioinst = cstrio.getIoInstance("json")
            return ioinst.to_dict()

        pio = SingleConstraintPairIo
        ionst = pio.getIoClass("json")
        pdict = {}
        pdict["class"] = SingleConstraintPair.__name__
        pdict["type"] = "pair"
        member1 = arg2dict(self.scpair1.arg1)
        member2 = arg2dict(self.scpair1.arg2)
        pdict["members"] = [member1, member2]
        pjson = json.dumps(pdict, ensure_ascii=True, indent=2, sort_keys=True)
        mypair = ionst.from_json(pjson)
        self.assertEqual(mypair, self.scpair1)


if __name__ == "__main__":
    unittest.main()
