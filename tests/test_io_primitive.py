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
from suite.dtype.primitive import ConstantString
from suite.io.iprimitive import ConstraintStringIo
from suite.io.iprimitive import NonNumericStringIo
from suite.io.iprimitive import ConstantStringIo


class TestIoIPrimitive(unittest.TestCase):
    "test io primitive module"

    def setUp(self):
        "setup small data"

        def lfn(x: ConstantString):
            return x.constr.islower()

        mcons = ConstantString("my valid constraint string")
        self.mycstr = ConstraintString(mcons, lfn)
        self.myfn = dill.dumps(self.mycstr.fn)
        mncons = ConstantString("my valid non numeric string")
        self.mynnstr = NonNumericString(mncons)
        self.mynnfn = dill.dumps(self.mynnstr.fn)
        self.myconstr = ConstantString("my valid constant string")
        self.myconstio = ConstantStringIo(self.myconstr)

    def test_constant_str_to_xml(self):
        cstrio = ConstantStringIo(self.myconstr)
        ioinst = cstrio.getIoInstance("xml")
        default = ioinst.to_element()
        cmpel = etree.Element("primitive")
        cmpel.set("class", "ConstantString")
        cmpel.text = str(self.myconstr)
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_constant_str_to_json(self):
        cstrio = ConstantStringIo(self.myconstr)
        ioinst = cstrio.getIoInstance("json")
        defjson = ioinst.to_json()
        defdict = ioinst.to_dict()
        cmpd = {}
        cmpd["class"] = "ConstantString"
        cmpd["type"] = "primitive"
        cmpd["value"] = str(self.myconstr)
        cmpstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(cmpd, defdict)
        self.assertEqual(cmpstr, defjson)

    def test_constant_str_from_json(self):
        consio = ConstantStringIo
        jio = ConstantStringIo.getIoClass("json")
        cmpd = {}
        cmpd["class"] = "ConstantString"
        cmpd["type"] = "primitive"
        cmpd["value"] = str(self.myconstr)
        cmpstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        myconst = jio.from_json(cmpstr)
        self.assertEqual(myconst, self.myconstr)

    def test_constant_str_from_xml(self):
        xmlio = ConstantStringIo.getIoClass("xml")
        cmpel = etree.Element("primitive")
        cmpel.set("class", "ConstantString")
        cmpel.text = str(self.myconstr)
        cstr = xmlio.from_element(cmpel)
        self.assertEqual(cstr, self.myconstr)

    def test_constraint_str_to_xml(self):
        cstrio = ConstraintStringIo(self.mycstr)
        ioinst = cstrio.getIoInstance("xml")
        default = ioinst.to_element()
        cmpel = etree.Element("primitive", constraint=self.myfn.hex())
        cmpel.set("class", "ConstraintString")
        cmpel.text = str(self.mycstr)
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_constraint_str_to_json(self):
        cstrio = ConstraintStringIo(self.mycstr)
        consio = ConstantStringIo(self.mycstr.cstr)
        cionst = consio.getIoInstance("json")
        ioinst = cstrio.getIoInstance("json")
        default = ioinst.to_json()
        dicrepr = ioinst.to_dict()
        cmpd = {}
        cmpd["class"] = "ConstraintString"
        cmpd["type"] = "primitive"
        cmpd["value"] = cionst.to_dict()
        cmpd["constraint"] = self.myfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(default, reprstr)
        self.assertEqual(dicrepr, cmpd)

    def test_constraint_str_from_json(self):
        ""
        jio = ConstraintStringIo.getIoClass("json")
        consio = ConstantStringIo(self.mycstr.cstr)
        ioinst = consio.getIoInstance("json")
        consjson = ioinst.to_json()
        cmpd = {}
        cmpd["class"] = "ConstraintString"
        cmpd["type"] = "primitive"
        cmpd["value"] = json.loads(consjson)
        cmpd["constraint"] = self.myfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        cstr = jio.from_json(reprstr)
        self.assertEqual(self.mycstr, cstr)

    def test_constraint_str_from_xml(self):
        xmlio = ConstraintStringIo.getIoClass("xml")
        cmpel = etree.Element("primitive", constraint=self.myfn.hex())
        cmpel.set("class", "ConstraintString")
        cmpel.text = str(self.mycstr)
        cstr = xmlio.from_element(cmpel)
        self.assertEqual(cstr, self.mycstr)

    def test_non_numeric_string_to_xml(self):
        nnstrio = NonNumericStringIo(self.mynnstr)
        ioinst = nnstrio.getIoInstance("xml")
        default = ioinst.to_element()
        cmpel = etree.Element("primitive", constraint=self.mynnfn.hex())
        cmpel.set("class", "NonNumericString")
        cmpel.text = str(self.mynnstr)
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_non_numeric_string_to_json(self):
        consio = ConstantStringIo(self.mynnstr.cstr)
        ioinst = consio.getIoInstance("json")
        consjson = ioinst.to_json()
        cstrio = NonNumericStringIo(self.mynnstr)
        ioinst = cstrio.getIoInstance("json")
        default = ioinst.to_json()
        dicrepr = ioinst.to_dict()
        cmpd = {}
        cmpd["class"] = "NonNumericString"
        cmpd["type"] = "primitive"
        cmpd["value"] = json.loads(consjson)
        cmpd["constraint"] = self.mynnfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(default, reprstr)
        self.assertEqual(dicrepr, cmpd)

    def test_non_numeric_string_from_json(self):
        ""
        consio = ConstantStringIo(self.mynnstr.cstr)
        ioinst = consio.getIoInstance("json")
        consjson = ioinst.to_json()
        jio = NonNumericStringIo.getIoClass("json")
        cmpd = {}
        cmpd["class"] = "NonNumericString"
        cmpd["type"] = "primitive"
        cmpd["value"] = json.loads(consjson)
        cmpd["constraint"] = self.mynnfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        nnstr = jio.from_json(reprstr)
        self.assertEqual(self.mynnstr, nnstr)

    def test_non_numeric_string_from_xml(self):
        xmlio = NonNumericStringIo.getIoClass("xml")
        cmpel = etree.Element("primitive", constraint=self.mynnfn.hex())
        cmpel.set("class", "NonNumericString")
        cmpel.text = str(self.mynnstr)
        nnstr = xmlio.from_element(cmpel)
        self.assertEqual(nnstr, self.mynnstr)


if __name__ == "__main__":
    unittest.main()
