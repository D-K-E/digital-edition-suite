# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from lxml import etree
import json
import yaml

from suite.dtype.primitive import ConstraintString, NonNumericString
from suite.io.iprimitive import ConstraintStringIo
from suite.io.iprimitive import NonNumericStringIo


class TestIo(unittest.TestCase):
    "test io modules"

    def setUp(self):
        "setup small data"

        def lfn(x: str):
            return x.islower()

        self.mycstr = ConstraintString("my valid constraint string", lfn)
        self.mynnstr = NonNumericString("my valid non numeric string")

    def test_constraint_str_xml(self):
        crenderer = ConstraintStringIo(self.mycstr)
        renderer = crenderer.getIo("xml")
        default = renderer.renderDefault()
        cmpel = etree.Element("primitive", constraint="lfn")
        cmpel.set("class", "constraint" + renderer.cnameSep + "string")
        cmpel.text = self.mycstr.cstr
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_constraint_str_html(self):
        crenderer = ConstraintStringIo(self.mycstr)
        renderer = crenderer.getIo("html")
        default = renderer.renderDefault()
        cmpel = etree.Element("div")
        cmpel.set("data-class", "constraint" + renderer.cnameSep + "string")
        cmpel.set("data-type", "primitive")
        cmpel.set("data-constraint", "lfn")
        cmpel.text = self.mycstr.cstr
        self.assertEqual(default.text, cmpel.text)
        self.assertEqual(default.attrib, cmpel.attrib)

    def test_constraint_str_json(self):
        crenderer = ConstraintStringIo(self.mycstr)
        renderer = crenderer.getIo("json")
        default = renderer.toJSON()
        defrepr = renderer.renderDefault()
        cmpd = {}
        cmpd["class"] = "constraint" + renderer.cnameSep + "string"
        cmpd["type"] = "primitive"
        cmpd["value"] = self.mycstr.cstr
        cmpd["constraint"] = "lfn"
        reprstr = json.dumps(cmpd, ensure_ascii=False, indent=2, sort_keys=True)
        self.assertEqual(default, reprstr)
        self.assertEqual(defrepr, cmpd)

    def test_constraint_str_yaml(self):
        crenderer = ConstraintStringIo(self.mycstr)
        renderer = crenderer.getIo("yaml")
        defrepr = renderer.renderDefault()
        cmpd = {}
        cname = "constraint" + renderer.cnameSep + "string"
        cmpd["class"] = cname
        cmpd["type"] = "!Primitive"
        cmpd["value"] = self.mycstr.cstr
        cmpd["constraint"] = "lfn"
        self.assertEqual(cmpd, defrepr)
        cmpcls = """
        --- !Primitive
        class: {0}
        value: {1}
        constraint: lfn
        """.format(
            cname, self.mycstr.cstr
        )
        # myobj = yaml.load(cmpcls)
        pdb.set_trace()
        mydump = yaml.dump(renderer)
        ndmp = renderer.to_yaml()
        self.assertEqual(cmpcls, mydump)


if __name__ == "__main__":
    unittest.main()
