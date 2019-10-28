# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from suite.dtype.primitive import ConstraintString, NonNumericString


class TestPrimitive(unittest.TestCase):

    def setUp(self):
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.assetdir = os.path.join(self.testdir, "assets")

    def test_constraint_string(self):
        def lfn(x: str): return x.islower()
        cstr1 = ConstraintString("my true string", lfn)
        cstr2 = ConstraintString("MY False String", lfn)
        self.assertEqual(True, cstr1.isValid())
        self.assertEqual(False, cstr2.isValid())

    def test_nonnumeric_string(self):
        cstr1 = NonNumericString("my true string")
        cstr2 = NonNumericString("1 my another true string 1")
        cstr3 = NonNumericString("123")
        cstr4 = NonNumericString("123.45")
        cstr5 = NonNumericString("123j")
        cstr6 = NonNumericString("123/1235")
        self.assertEqual(True, cstr1.isValid())
        self.assertEqual(True, cstr2.isValid())
        self.assertEqual(False, cstr3.isValid())
        self.assertEqual(False, cstr4.isValid())
        self.assertEqual(False, cstr5.isValid())
        self.assertEqual(False, cstr6.isValid())


if __name__ == "__main__":
    unittest.main()
