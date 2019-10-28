# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from suite.dtype.primitive import NonNumericString
from suite.dtype.container import SingleConstraintTuple
from suite.dtype.container import NonNumericTuple
from suite.dtype.container import UniformNonNumericMixedPair

from suite.dtype.structure import SimpleStructure
from suite.dtype.structure import CombinedStructure
from suite.dtype.structure import LinkStructure


class TestModel(unittest.TestCase):
    "test container.py"

    def setUp(self):
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.assetdir = os.path.join(self.testdir, "assets")

    def test_simple_structure(self):
        "simple structure"
        idstr = NonNumericString("My String 2")
        value = "𐎠𐎭𐎠 𐏐 𐏃𐎹"
        definition = "adā : hya"
        ss = SimpleStructure(idstr=idstr,
                             value=value,
                             definition=definition)
        self.assertEqual(True, ss.isValid())

    def test_combined_structure(self):
        "combined structure"
        idstr = NonNumericString("my-string-2")
        value = "𐎠𐎭𐎠 𐏐 𐏃𐎹"
        definition = "adā : hya"
        id2 = NonNumericString("relation-2")
        mystr1 = NonNumericString("word-1")
        mystr2 = NonNumericString("word-2")
        mystr3 = NonNumericString("word-3")
        mset = frozenset([mystr1, mystr2, mystr3])
        tpl = NonNumericTuple(mset)
        cstruct = CombinedStructure(id1=idstr,
                                    value=value,
                                    definition=definition,
                                    id2=id2,
                                    values=tpl)
        self.assertEqual(True, cstruct.isValid())

    def test_link_structure(self):
        ""
        idstr = NonNumericString("my-string-2")
        id2a = NonNumericString("relation-2")
        mystr1 = NonNumericString("word-1")
        mystr2 = NonNumericString("word-2")
        mystr3 = NonNumericString("word-3")
        mset = frozenset([mystr1, mystr2, mystr3])
        tpl1 = NonNumericTuple(mset)
        p1 = UniformNonNumericMixedPair(id2a,
                                        tpl1)
        id2b = NonNumericString("relation-3")
        mystr4 = NonNumericString("word-4")
        mystr5 = NonNumericString("word-5")
        mystr6 = NonNumericString("word-6")
        mset = frozenset([mystr1, mystr2, mystr3])
        tpl2 = NonNumericTuple(mset)
        p2 = UniformNonNumericMixedPair(id2b,
                                        tpl2)
        link1 = LinkStructure(idstr,
                              frozenset([p1, p2]))
        self.assertEqual(True, link1.isValid())
        id2c = NonNumericString("relation-3")
        mystr6 = NonNumericString("word-7")
        mset = frozenset([mystr1, mystr2, mystr6])
        tpl2 = NonNumericTuple(mset)
        p3 = UniformNonNumericMixedPair(id2c,
                                        tpl2)
        link2 = LinkStructure(idstr,
                              frozenset([p1, p2, p3]))
        self.assertEqual(False, link2.isValid())


if __name__ == "__main__":
    unittest.main()
