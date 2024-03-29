# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from suite.dtype.primitive import PrimitiveMaker
from suite.dtype.primitive import ConstantString
from suite.dtype.primitive import NonNumericString
from suite.dtype.primitive import ConstraintString


class TestPrimitive(unittest.TestCase):
    def setUp(self):
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.assetdir = os.path.join(self.testdir, "assets")

    def test_primitive_maker_choice(self):
        check = False
        try:
            pmaker = PrimitiveMaker("weird choice")
            pmaker.make(mystr="my string")
        except ValueError:
            check = True
        self.assertEqual(check, True)

    def test_primitive_maker_from_type(self):
        "test making object from type"
        pmaker = PrimitiveMaker
        check = False
        try:
            pmaker.from_type(int, mystr=252)
        except ValueError:
            check = True
        self.assertTrue(check)
        check = True
        try:
            pmaker.from_type(ConstantString, mystr="here is a string")
        except TypeError or ValueError:
            check = False
        self.assertTrue(check)
        check = False
        try:
            pmaker.from_type(ConstraintString, mystr="here is a string")
        except TypeError:
            check = True
        self.assertTrue(check)
        check = True
        try:
            mystr = pmaker.from_type(ConstantString, mystr="a str")

            def lfn(x):
                return x.constr.islower()

            pmaker.from_type(ConstraintString, mystr=mystr, fnc=lfn)
        except TypeError:
            check = True
        self.assertTrue(check)

    def test_primitive_maker_from_str(self):
        pmaker = PrimitiveMaker("constant string")
        cmaker = PrimitiveMaker("constraint string")
        check = True
        try:
            constr = pmaker.from_string(mystr="a str")
        except ValueError or TypeError:
            check = False
        self.assertTrue(check)

        def lfn(x):
            return x.constr.islower()

        check = True
        try:
            constr = cmaker.from_string(mystr="another str", fnc=lfn)
        except ValueError or TypeError:
            check = False
        self.assertTrue(check)

    def test_primitive_maker_constant_string(self):
        pmaker = PrimitiveMaker("char")
        check = False
        try:
            pmaker.make_constant_string(1235)
        except TypeError:
            check = True
        self.assertTrue(check)
        check = False
        try:
            pmaker.make_constant_string(1235.05)
        except TypeError:
            check = True
        self.assertTrue(check)
        check = False
        try:
            pmaker.make_constant_string(True)
        except TypeError:
            check = True
        self.assertTrue(check)

    def test_constant_string(self):
        "test for constant string primitive"
        pmaker = PrimitiveMaker("constant string")
        myconstr1 = pmaker.make(mystr="my true constant string and unicode š")
        myconstr2 = pmaker.make(mystr="my true constant string and unicode š")
        myconstr3 = pmaker.make(mystr="my true constant string and unicode ḫ")
        self.assertEqual(True, myconstr1.isValid())
        self.assertEqual(False, myconstr1 == myconstr3)
        self.assertEqual(True, myconstr1 == myconstr2)

    def test_constraint_string(self):
        pmaker = PrimitiveMaker("constant string")

        def lfn(x: ConstantString):
            return x.constr.islower()

        costr1 = pmaker.make(mystr="my true string")
        costr2 = pmaker.make(mystr="MY False String")
        cstr1 = pmaker.from_type(primitiveType=ConstraintString, mystr=costr1, fnc=lfn)
        check = False
        try:
            cstr2 = pmaker.from_type(
                primitiveType=ConstraintString, mystr=costr2, fnc=lfn
            )
        except ValueError:
            check = True

        self.assertEqual(True, cstr1.isValid())
        self.assertEqual(True, check)

    def test_nonnumeric_string(self):
        pmaker = PrimitiveMaker("constant string")
        costr1 = pmaker.make(mystr="my true string")
        costr2 = pmaker.make(mystr="1 my another true string 1")
        costr3 = pmaker.make(mystr="123")
        costr4 = pmaker.make(mystr="123.45")
        costr5 = pmaker.make(mystr="123j")
        costr6 = pmaker.make(mystr="123/12335")

        pmaker = PrimitiveMaker("non numeric string")
        cstr1 = pmaker.make(mystr=costr1)
        cstr2 = pmaker.make(mystr=costr2)
        check = False
        try:
            cstr3 = pmaker.make(mystr=costr3)
        except ValueError:
            check = True
        self.assertEqual(True, check)
        check = False
        try:
            cstr4 = pmaker.make(mystr=costr4)
        except ValueError:
            check = True
        self.assertEqual(True, check)
        check = False
        try:
            cstr5 = pmaker.make(mystr=costr5)
        except ValueError:
            check = True
        self.assertEqual(True, check)
        check = False
        try:
            cstr6 = pmaker.make(mystr=costr6)
        except ValueError:
            check = True
        self.assertEqual(True, check)


if __name__ == "__main__":
    unittest.main()
