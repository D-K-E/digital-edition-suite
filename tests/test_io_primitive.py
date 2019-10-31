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


class TestIoIPrimitive(unittest.TestCase):
    "test io primitive module"

    def setUp(self):
        "setup small data"

        def lfn(x: str):
            return x.islower()

        self.mycstr = ConstraintString("my valid constraint string", lfn)
        self.myfn = dill.dumps(self.mycstr.fn)
        self.mynnstr = NonNumericString("my valid non numeric string")
        self.mynnfn = dill.dumps(self.mynnstr.fn)

    def test_constraint_str_to_xml(self):
        cstrio = ConstraintStringIo(self.mycstr)
        ioinst = cstrio.getIoInstance("xml")
        default = ioinst.to_element()
        cmpel = etree.Element("primitive", constraint=self.myfn.hex())
        cmpel.set("class", "ConstraintString")
        cmpel.text = self.mycstr.cstr
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_constraint_str_to_json(self):
        cstrio = ConstraintStringIo(self.mycstr)
        ioinst = cstrio.getIoInstance("json")
        default = ioinst.to_json()
        dicrepr = ioinst.to_dict()
        cmpd = {}
        cmpd["class"] = "ConstraintString"
        cmpd["type"] = "primitive"
        cmpd["value"] = self.mycstr.cstr
        cmpd["constraint"] = self.myfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(default, reprstr)
        self.assertEqual(dicrepr, cmpd)

    def test_constraint_str_from_json(self):
        ""
        jio = ConstraintStringIo.getIoClass("json")
        cmpd = {}
        cmpd["class"] = "ConstraintString"
        cmpd["type"] = "primitive"
        cmpd["value"] = self.mycstr.cstr
        cmpd["constraint"] = self.myfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        cstr = jio.from_json(reprstr)
        self.assertEqual(self.mycstr, cstr)

    def test_constraint_str_from_xml(self):
        xmlio = ConstraintStringIo.getIoClass("xml")
        cmpel = etree.Element("primitive", constraint=self.myfn.hex())
        cmpel.set("class", "ConstraintString")
        cmpel.text = self.mycstr.cstr
        cstr = xmlio.from_element(cmpel)
        self.assertEqual(cstr, self.mycstr)

    def test_non_numeric_string_to_xml(self):
        nnstrio = NonNumericStringIo(self.mynnstr)
        ioinst = nnstrio.getIoInstance("xml")
        default = ioinst.to_element()
        cmpel = etree.Element("primitive", constraint=self.mynnfn.hex())
        cmpel.set("class", "NonNumericString")
        cmpel.text = self.mynnstr.cstr
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_non_numeric_string_to_json(self):
        cstrio = NonNumericStringIo(self.mynnstr)
        ioinst = cstrio.getIoInstance("json")
        default = ioinst.to_json()
        dicrepr = ioinst.to_dict()
        cmpd = {}
        cmpd["class"] = "NonNumericString"
        cmpd["type"] = "primitive"
        cmpd["value"] = self.mynnstr.cstr
        cmpd["constraint"] = self.mynnfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(default, reprstr)
        self.assertEqual(dicrepr, cmpd)

    def test_non_numeric_string_from_json(self):
        ""
        jio = NonNumericStringIo.getIoClass("json")
        cmpd = {}
        cmpd["class"] = "NonNumericString"
        cmpd["type"] = "primitive"
        cmpd["value"] = self.mynnstr.cstr
        cmpd["constraint"] = self.mynnfn.hex()
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        nnstr = jio.from_json(reprstr)
        self.assertEqual(self.mynnstr, nnstr)

    def test_non_numeric_string_from_xml(self):
        xmlio = NonNumericStringIo.getIoClass("xml")
        cmpel = etree.Element("primitive", constraint=self.mynnfn.hex())
        cmpel.set("class", "NonNumericString")
        cmpel.text = self.mynnstr.cstr
        nnstr = xmlio.from_element(cmpel)
        self.assertEqual(nnstr, self.mynnstr)


if __name__ == "__main__":
    unittest.main()
