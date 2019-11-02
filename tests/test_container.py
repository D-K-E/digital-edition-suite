# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest
import os
import pdb

from suite.dtype.container import Pair, SingleConstraintPair
from suite.dtype.container import NestedPair, DoubleConstraintPair
from suite.dtype.container import ConstraintNestedPair
from suite.dtype.container import ConstraintNestedSingleConstraintPair
from suite.dtype.container import StringTuple
from suite.dtype.container import SingleConstraintTuple
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

    def test_pair(self):
        pmaker = ContainerMaker("pair")
        cmaker = PrimitiveMaker("constant string")
        mystr1 = cmaker.make(mystr="mystr1")
        mystr2 = cmaker.make(mystr="mystr2")
        pair = pmaker.make(arg1=mystr1, arg2=mystr2)
        cmpiter = set([mystr1, mystr2])
        piter = set([p for p in pair])
        self.assertEqual(True, pair.isValid())
        self.assertEqual(piter, cmpiter)
        check = False
        try:
            pmaker.make(arg1=1, arg2="mystr2")
        except AssertionError:
            check = True
        self.assertEqual(True, check)

    def test_single_constraint_pair(self):
        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        pmaker = PrimitiveMaker("constraint string")
        pcmaker = PrimitiveMaker("constant string")
        cstr1 = pcmaker.make(mystr="my true string")
        cstr2 = pcmaker.make(mystr="my another true string")
        mystr1 = pmaker.make(mystr=cstr1, fnc=lfn)
        mystr2 = pmaker.make(mystr=cstr2, fnc=lfn)
        cmaker = ContainerMaker("single constraint pair")
        check = True
        try:
            scpair1 = cmaker.make(arg1=mystr1, arg2=mystr2)
        except AssertionError:
            check = False
        self.assertEqual(True, check)


#   def test_double_constraint_pair(self):
#       def lfn(x: str):
#           return x.islower()

#       def nonlfn(x: str):
#           return not x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("My False String", nonlfn)
#       mystr4 = ConstraintString("my another true string", nonlfn)
#       scpair1 = DoubleConstraintPair(str1=mystr1, str2=mystr3)
#       scpair2 = DoubleConstraintPair(str1=mystr2, str2=mystr4)
#       self.assertEqual(True, scpair1.isValid())
#       self.assertEqual(False, scpair2.isValid())

#   def test_nested_pair(self):
#       pair = Pair("mystr1", "mystr2")
#       npair = NestedPair("my simple string", pair)
#       self.assertEqual(True, npair.isValid())
#       check = False
#       try:
#           NestedPair(123, pair)
#       except AssertionError:
#           check = True
#       self.assertEqual(True, check)

#   def test_constraint_nested_pair(self):
#       ""

#       def lfn(x: str):
#           return x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       pair = Pair("mystr1", "mystr2")
#       npair = ConstraintNestedPair(mystr1, pair)
#       self.assertEqual(True, npair.isValid())
#       mystr2 = ConstraintString("My True string", lfn)
#       mpair = ConstraintNestedPair(mystr2, pair)
#       self.assertEqual(False, mpair.isValid())

#   def test_constraint_nested_single_constraint_pair(self):
#       def lfn(x: str):
#           return x.islower()

#       def nonlfn(x: str):
#           return not x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("my false string", nonlfn)
#       mystr4 = ConstraintString("my True string", nonlfn)
#       scpair1 = SingleConstraintPair(str1=mystr1, str2=mystr2)
#       scpair2 = SingleConstraintPair(str1=mystr4, str2=mystr3)
#       cnscp1 = ConstraintNestedSingleConstraintPair(mystr4, scpair1)
#       cnscp2 = ConstraintNestedSingleConstraintPair(mystr3, scpair2)
#       self.assertEqual(True, cnscp1.isValid())
#       self.assertEqual(False, cnscp2.isValid())

#   def test_string_tuple(self):
#       mset1 = set(["m1", "m2", "m3"])
#       mset1 = frozenset(mset1)
#       mset2 = set([1, "m2", "m3"])
#       mset2 = frozenset(mset2)
#       tpl1 = StringTuple(mset1)
#       check = False
#       try:
#           StringTuple(mset2)
#       except AssertionError:
#           check = True
#       self.assertEqual(True, tpl1.isValid())
#       self.assertEqual(True, check)

#   def test_single_constraint_tuple(self):
#       def lfn(x: str):
#           return x.islower()

#       def nonlfn(x: str):
#           return not x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("my false string", nonlfn)
#       mset1 = set([mystr1, mystr2, mystr3])
#       mset1 = frozenset(mset1)
#       mset2 = set([mystr1, mystr2])
#       mset2 = frozenset(mset2)
#       tpl2 = SingleConstraintTuple(mset2)
#       check = False
#       try:
#           SingleConstraintTuple(mset1)
#       except AssertionError:
#           check = True
#       self.assertEqual(True, tpl2.isValid())
#       self.assertEqual(True, check)

#   def test_non_numeric_tuple(self):
#       mystr1 = NonNumericString("my true string")
#       mystr2 = NonNumericString("my another true string")
#       mystr3 = NonNumericString("my false string")
#       mset1 = set([mystr1, mystr2, mystr3])
#       mset1 = frozenset(mset1)
#       tpl2 = NonNumericTuple(mset1)
#       self.assertEqual(True, tpl2.isValid())

#   def test_pair_tuple(self):
#       pair1 = Pair("mystr1", "mystr2")
#       pair2 = Pair("mystr3", "mystr4")
#       pair3 = Pair("mystr5", "mystr6")
#       mset = frozenset([pair1, pair2, pair3])
#       ptpl = PairTuple(mset)
#       self.assertEqual(True, ptpl.isValid())

#   def test_single_pair_tuple(self):
#       def lfn(x: str):
#           return x.islower()

#       def nonlfn(x: str):
#           return not x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("My False String", nonlfn)
#       mystr4 = ConstraintString("my Another true string", nonlfn)
#       scpair1 = SingleConstraintPair(str1=mystr1, str2=mystr2)
#       scpair2 = SingleConstraintPair(str1=mystr3, str2=mystr4)
#       mset = frozenset([scpair1, scpair2])
#       ptpl = SinglePairTuple(mset)
#       self.assertEqual(True, ptpl.isValid())

#   def test_uniform_pair_tuple(self):
#       def lfn(x: str):
#           return x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("my another 2 true string", lfn)
#       mystr4 = ConstraintString("my another 3 true string", lfn)
#       scpair1 = SingleConstraintPair(str1=mystr1, str2=mystr2)
#       scpair2 = SingleConstraintPair(str1=mystr3, str2=mystr4)
#       mset = frozenset([scpair1, scpair2])
#       tpl = UniformPairTuple(mset)
#       self.assertEqual(True, tpl.isValid())

#   def test_mixed_pair(self):
#       def lfn(x: str):
#           return x.islower()

#       mset1 = set(["m1", "m2", "m3"])
#       mset1 = frozenset(mset1)
#       tpl1 = StringTuple(mset1)
#       mystr1 = ConstraintString("my true string", lfn)
#       mpair = MixedPair(mystr1, tpl1)
#       self.assertEqual(True, mpair.isValid())

#   def test_single_constraint_mixed_pair(self):
#       def lfn(x: str):
#           return x.islower()

#       def nonlfn(x: str):
#           return not x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("my False string", nonlfn)
#       mystr4 = ConstraintString("my false string", nonlfn)
#       mset2 = set([mystr1, mystr2])
#       mset2 = frozenset(mset2)
#       tpl2 = SingleConstraintTuple(mset2)
#       spair1 = SingleConstraintMixedPair(mystr3, tpl2)
#       spair2 = SingleConstraintMixedPair(mystr4, tpl2)
#       self.assertEqual(True, spair1.isValid())
#       self.assertEqual(False, spair2.isValid())

#   def test_uniform_mixed_pair(self):
#       def lfn(x: str):
#           return x.islower()

#       def nonlfn(x: str):
#           return not x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("my another true string 2", lfn)
#       mystr4 = ConstraintString("my false string", nonlfn)
#       mset2 = set([mystr1, mystr2])
#       mset2 = frozenset(mset2)
#       tpl2 = SingleConstraintTuple(mset2)
#       spair1 = UniformMixedPair(str1=mystr3, strset=tpl2)
#       self.assertEqual(True, spair1.isValid())
#       check = False
#       try:
#           UniformMixedPair(str1=mystr4, strset=tpl2)
#       except AssertionError:
#           check = True
#       self.assertEqual(True, check)

#   def test_non_numeric_mixed_pair(self):
#       def lfn(x: str):
#           return x.islower()

#       mystr1 = ConstraintString("my true string", lfn)
#       mystr2 = ConstraintString("my another true string", lfn)
#       mystr3 = ConstraintString("my another true string 2", lfn)
#       myn1 = NonNumericString("my non numeric")
#       mset2 = set([mystr1, mystr2, mystr3])
#       mset2 = frozenset(mset2)
#       tpl2 = SingleConstraintTuple(mset2)
#       nnpair = NonNumericMixedPair(myn1, tpl2)
#       self.assertEqual(True, nnpair.isValid())


if __name__ == "__main__":
    unittest.main()
