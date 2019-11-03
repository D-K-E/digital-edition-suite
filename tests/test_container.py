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
        self.consMaker = PrimitiveMaker("constant string")
        self.constrMaker = PrimitiveMaker("constraint string")

    def test_pair(self):
        pmaker = ContainerMaker("pair")
        mystr1 = self.consMaker.make(mystr="mystr1")
        mystr2 = self.consMaker.make(mystr="mystr2")
        pair = pmaker.make(arg1=mystr1, arg2=mystr2)
        cmpiter = set([mystr1, mystr2])
        piter = set([p for p in pair])
        self.assertEqual(True, pair.isValid())
        self.assertEqual(piter, cmpiter)
        check = False
        try:
            pmaker.make(arg1=1, arg2="mystr2")
        except TypeError:
            check = True
        self.assertEqual(True, check)

    def test_single_constraint_pair(self):
        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        pmaker = PrimitiveMaker(choice="constraint string")
        pcmaker = PrimitiveMaker(choice="constant string")
        cstr1 = self.consMaker.make(mystr="my true string")
        cstr2 = self.consMaker.make(mystr="my another true string")
        mystr1 = self.constrMaker.make(mystr=cstr1, fnc=lfn)
        mystr2 = self.constrMaker.make(mystr=cstr2, fnc=lfn)
        cmaker = ContainerMaker("single constraint pair")
        check = True
        try:
            scpair1 = cmaker.make(arg1=mystr1, arg2=mystr2)
        except ValueError:
            check = False
        self.assertEqual(True, check)

    def test_double_constraint_pair(self):
        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        mystr1 = self.constrMaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = self.constrMaker.from_string(mystr="my another true string", fnc=lfn)
        mystr3 = self.constrMaker.from_string(mystr="My False String", fnc=nonlfn)
        mystr4 = self.constrMaker.from_string(mystr="my another true string", fnc=lfn)
        scpair1 = DoubleConstraintPair(arg1=mystr1, arg2=mystr3)
        self.assertEqual(True, scpair1.isValid())

    def test_nested_pair(self):
        pmaker = ContainerMaker("nested pair")
        cstr1 = self.consMaker.make(mystr="mystr1")
        cstr2 = self.consMaker.make(mystr="mystr2")
        pair = Pair(cstr1, cstr2)
        cstr3 = self.consMaker.make(mystr="my simple string")
        check = True
        try:
            npair = pmaker.make(arg1=cstr3, arg2=pair)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_constraint_nested_pair(self):
        ""
        pmaker = ContainerMaker("constraint nested pair")

        def lfn(x: ConstantString):
            return x.constr.islower()

        mystr1 = self.constrMaker.from_string(mystr="my true string", fnc=lfn)
        m1 = self.consMaker.from_string(mystr="mystr1")
        m2 = self.consMaker.from_string(mystr="mystr2")
        pair = Pair(m1, m2)
        check = True
        try:
            npair = pmaker.make(arg1=mystr1, arg2=pair)
        except ValueError:
            check = False
        self.assertEqual(True, check)

    def test_constraint_nested_single_constraint_pair(self):
        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        pmaker = ContainerMaker("single constraint pair")
        pmaker2 = ContainerMaker("constraint nested single constraint pair")
        mystr1 = self.constrMaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = self.constrMaker.from_string(mystr="my another true string", fnc=lfn)
        mystr4 = self.constrMaker.from_string(mystr="my True string", fnc=nonlfn)
        scpair1 = pmaker.make(arg1=mystr1, arg2=mystr2)
        check = True
        try:
            cnscp1 = pmaker2.make(arg1=mystr4, arg2=scpair1)
        except ValueError:
            check = False
        self.assertEqual(True, check)

    def test_string_tuple(self):
        cmaker = ContainerMaker("tuple")
        pmaker = PrimitiveMaker(choice="constant string")
        mset1 = set(
            [
                pmaker.from_string(mystr="m1"),
                pmaker.from_string(mystr="m2"),
                pmaker.from_string(mystr="m3"),
            ]
        )
        mset1 = frozenset(mset1)
        check = True
        try:
            tpl1 = cmaker.make(els=mset1)
        except ValueError:
            check = False
        self.assertEqual(True, check)

    def test_single_constraint_tuple(self):
        cmaker = ContainerMaker("single constraint tuple")
        pmaker = PrimitiveMaker(choice="constraint string")

        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        mystr1 = pmaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = pmaker.from_string(mystr="my another true string", fnc=lfn)
        mset1 = set([mystr1, mystr2])
        mset1 = frozenset(mset1)
        check = True
        try:
            tpl = cmaker.make(els=mset1)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)
        mset1 = set(mset1)
        check = True
        try:
            tpl = cmaker.make(els=mset1)
        except TypeError or ValueError:
            check = False
        self.assertEqual(False, check)

    def test_non_numeric_tuple(self):
        pmaker = PrimitiveMaker(choice="non numeric string")
        cmaker = ContainerMaker("non numeric tuple")
        mystr1 = pmaker.from_string(mystr="my true string")
        mystr2 = pmaker.from_string(mystr="my another true string")
        mystr3 = pmaker.from_string(mystr="my false string")
        mset1 = set([mystr1, mystr2, mystr3])
        mset1 = frozenset(mset1)
        check = True
        try:
            tpl2 = cmaker.make(els=mset1)
        except ValueError or TypeError:
            check = False
        self.assertEqual(True, check)

    def test_pair_tuple(self):
        pmaker = PrimitiveMaker(choice="constant string")
        cmaker = ContainerMaker("pair")
        cmaker2 = ContainerMaker("pair tuple")

        pair1 = cmaker.make(
            arg1=pmaker.make(mystr="mystr1"), arg2=pmaker.make(mystr="mystr2")
        )
        pair2 = cmaker.make(
            arg1=pmaker.make(mystr="mystr3"), arg2=pmaker.make(mystr="mystr4")
        )
        pair3 = cmaker.make(
            arg1=pmaker.make(mystr="mystr5"), arg2=pmaker.make(mystr="mystr6")
        )
        mset = frozenset([pair1, pair2, pair3])
        check = True
        try:
            ptpl = cmaker2.make(els=mset)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_single_pair_tuple(self):
        pmaker = PrimitiveMaker(choice="constraint string")
        cmaker = ContainerMaker("single constraint pair")
        cmaker2 = ContainerMaker("single pair tuple")

        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        mystr1 = pmaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = pmaker.from_string(mystr="my another true string", fnc=lfn)
        mystr3 = pmaker.from_string(mystr="My False String", fnc=nonlfn)
        mystr4 = pmaker.from_string(mystr="my Another true string", fnc=nonlfn)
        scpair1 = cmaker.make(arg1=mystr1, arg2=mystr2)
        scpair2 = cmaker.make(arg1=mystr3, arg2=mystr4)
        mset = frozenset([scpair1, scpair2])
        check = True
        try:
            ptpl = cmaker2.make(els=mset)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_uniform_pair_tuple(self):
        pmaker = PrimitiveMaker(choice="constraint string")
        cmaker = ContainerMaker("single constraint pair")
        cmaker2 = ContainerMaker("uniform pair tuple")

        def lfn(x: ConstantString):
            return x.constr.islower()

        mystr1 = pmaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = pmaker.from_string("my another true string", fnc=lfn)
        mystr3 = pmaker.from_string("my another 2 true string", fnc=lfn)
        mystr4 = pmaker.from_string("my another 3 true string", fnc=lfn)
        scpair1 = cmaker.make(arg1=mystr1, arg2=mystr2)
        scpair2 = cmaker.make(arg1=mystr3, arg2=mystr4)
        mset = frozenset([scpair1, scpair2])
        check = True
        try:
            tpl = cmaker2.make(els=mset)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_mixed_pair(self):
        pmaker = PrimitiveMaker("constant string")
        pmaker2 = PrimitiveMaker("constraint string")
        cmaker = ContainerMaker("tuple")
        cmaker2 = ContainerMaker("mixed pair")

        def lfn(x: ConstantString):
            return x.constr.islower()

        mset1 = set(
            [pmaker.make(mystr="m1"), pmaker.make(mystr="m2"), pmaker.make(mystr="m3")]
        )
        mset1 = frozenset(mset1)
        tpl1 = cmaker.make(els=mset1)
        mystr1 = pmaker.make(mystr="my true string")
        check = True
        try:
            mpair = cmaker2.make(arg1=mystr1, arg2=tpl1)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_single_constraint_mixed_pair(self):
        pmaker = PrimitiveMaker(choice="constraint string")
        cmaker = ContainerMaker("single constraint tuple")
        cmaker2 = ContainerMaker("single constraint mixed pair")

        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        mystr1 = pmaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = pmaker.from_string(mystr="my another true string", fnc=lfn)
        mystr3 = pmaker.from_string(mystr="my False string", fnc=nonlfn)
        mset2 = set([mystr1, mystr2])
        mset2 = frozenset(mset2)
        tpl2 = cmaker.make(els=mset2)
        check = True
        try:
            spair1 = cmaker2.make(arg1=mystr3, arg2=tpl2)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_uniform_mixed_pair(self):
        pmaker = PrimitiveMaker(choice="constraint string")
        cmaker = ContainerMaker("single constraint tuple")

        def lfn(x: ConstantString):
            return x.constr.islower()

        def nonlfn(x: ConstantString):
            return not x.constr.islower()

        mystr1 = pmaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = pmaker.from_string(mystr="my another true string", fnc=lfn)
        mystr3 = pmaker.from_string(mystr="my another true string 2", fnc=lfn)
        mset2 = set([mystr1, mystr2])
        mset2 = frozenset(mset2)
        tpl2 = cmaker.make(els=mset2)
        cmaker2 = ContainerMaker("uniform mixed pair")
        check = True
        try:
            spair1 = cmaker2.make(arg1=mystr3, arg2=tpl2)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)

    def test_non_numeric_mixed_pair(self):
        pmaker = PrimitiveMaker(choice="constraint string")
        pmaker2 = PrimitiveMaker(choice="non numeric string")
        cmaker = ContainerMaker("single constraint tuple")
        cmaker2 = ContainerMaker("non numeric mixed pair")

        def lfn(x: ConstantString):
            return x.constr.islower()

        mystr1 = pmaker.from_string(mystr="my true string", fnc=lfn)
        mystr2 = pmaker.from_string(mystr="my another true string", fnc=lfn)
        mystr3 = pmaker.from_string(mystr="my another true string 2", fnc=lfn)
        myn1 = pmaker2.from_string(mystr="my non numeric")
        mset2 = set([mystr1, mystr2, mystr3])
        mset2 = frozenset(mset2)
        tpl2 = cmaker.make(els=mset2)
        check = True
        try:
            nnpair = cmaker2.make(arg1=myn1, arg2=tpl2)
        except TypeError or ValueError:
            check = False
        self.assertEqual(True, check)


if __name__ == "__main__":
    unittest.main()
