# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from suite.dtype.container import Pair, Array
from suite.dtype.container import ContainerMaker

from suite.dtype.primitive import ConstraintString
from suite.dtype.primitive import NonNumericString
from suite.dtype.primitive import ConstantString
from suite.dtype.primitive import PrimitiveMaker


class TestContainer(unittest.TestCase):
    "test container.py"

    def setUp(self):
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.assetdir = os.path.join(self.testdir, "assets")
        self.consMaker = PrimitiveMaker("constant string")
        self.constrMaker = PrimitiveMaker("constraint string")
        self.nnmaker = PrimitiveMaker("non numeric string")

    def test_pair(self):
        pmaker = ContainerMaker("pair")
        mystr1 = self.consMaker.make(mystr="mystr1")
        mystr2 = self.nnmaker.from_string(mystr="mystr2")
        mystr3 = self.consMaker.make(mystr="mystr3")
        check = True
        try:
            pair = pmaker.make(arg1=mystr1, arg2=mystr2)
        except ValueError or TypeError:
            check = False
        self.assertTrue(check, "either value or type error triggered")
        check = False
        try:
            pair = pmaker.make(arg1=mystr1, arg2=mystr3)
        except ValueError or TypeError:
            check = True
        self.assertTrue(check, "either value or type error should have been triggered")

    def test_array(self):
        pmaker = ContainerMaker("array")
        mystr1 = self.consMaker.make(mystr="mystr1")
        mystr2 = self.nnmaker.from_string(mystr="mystr2")
        mystr3 = self.consMaker.make(mystr="mystr3")
        check = True
        try:
            arr = pmaker.make(elements=[mystr1, mystr3])
        except ValueError or TypeError:
            check = False
        self.assertTrue(check, "either value or type error triggered")
        check = False
        try:
            arr = pmaker.make(elements=[mystr1, mystr2])
        except ValueError or TypeError:
            check = True
        self.assertTrue(check, "either value or type error should have been triggered")




if __name__ == "__main__":
    unittest.main()
