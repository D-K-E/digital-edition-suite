# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from suite.dtype.primitive import PrimitiveMaker
from suite.dtype.primitive import ConstantString


class TestPrimitive(unittest.TestCase):
    def setUp(self):
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.assetdir = os.path.join(self.testdir, "assets")

    def test_primitive_maker_choice(self):
        pmaker = PrimitiveMaker()
        check = False
        try:
            pmaker.make(choice="weird choice", mystr="my string")
        except ValueError:
            check = True
        self.assertEqual(check, True)

    def test_primitive_maker_constant_string(self):
        pmaker = PrimitiveMaker()
        check = False
        try:
            pmaker.make_constant_string(1235)
        except AssertionError:
            check = True
        self.assertTrue(check)
        check = False
        try:
            pmaker.make_constant_string(1235.05)
        except AssertionError:
            check = True
        self.assertTrue(check)
        check = False
        try:
            pmaker.make_constant_string(True)
        except AssertionError:
            check = True
        self.assertTrue(check)

    def test_constant_string(self):
        "test for constant string primitive"
        pmaker = PrimitiveMaker()
        myconstr1 = pmaker.make(
            choice="constant string", mystr="my true constant string and unicode š"
        )
        myconstr2 = pmaker.make(
            choice="constant string", mystr="my true constant string and unicode š"
        )
        myconstr3 = pmaker.make(
            choice="constant string", mystr="my true constant string and unicode ḫ"
        )
        self.assertEqual(True, myconstr1.isValid())
        self.assertEqual(False, myconstr1 == myconstr3)
        self.assertEqual(True, myconstr1 == myconstr2)

    def test_constraint_string(self):
        pmaker = PrimitiveMaker()

        def lfn(x: ConstantString):
            return x.constr.islower()

        costr1 = pmaker.make(choice="constant string", mystr="my true string")
        costr2 = pmaker.make(choice="constant string", mystr="MY False String")
        cstr1 = pmaker.make(choice="constraint string", mystr=costr1, fnc=lfn)
        cstr2 = pmaker.make(choice="constraint string", mystr=costr2, fnc=lfn)
        self.assertEqual(True, cstr1.isValid())
        self.assertEqual(False, cstr2.isValid())

    def test_nonnumeric_string(self):
        pmaker = PrimitiveMaker()
        costr1 = pmaker.make(choice="constant string", mystr="my true string")
        costr2 = pmaker.make(
            choice="constant string", mystr="1 my another true string 1"
        )
        costr3 = pmaker.make(choice="constant string", mystr="123")
        costr4 = pmaker.make(choice="constant string", mystr="123.45")
        costr5 = pmaker.make(choice="constant string", mystr="123j")
        costr6 = pmaker.make(choice="constant string", mystr="123/12335")

        cstr1 = pmaker.make(choice="non numeric string", mystr=costr1)
        cstr2 = pmaker.make(choice="non numeric string", mystr=costr2)
        cstr3 = pmaker.make(choice="non numeric string", mystr=costr3)
        cstr4 = pmaker.make(choice="non numeric string", mystr=costr4)
        cstr5 = pmaker.make(choice="non numeric string", mystr=costr5)
        cstr6 = pmaker.make(choice="non numeric string", mystr=costr6)
        self.assertEqual(True, cstr1.isValid())
        self.assertEqual(True, cstr2.isValid())
        self.assertEqual(False, cstr3.isValid())
        self.assertEqual(False, cstr4.isValid())
        self.assertEqual(False, cstr5.isValid())
        self.assertEqual(False, cstr6.isValid())


if __name__ == "__main__":
    unittest.main()
