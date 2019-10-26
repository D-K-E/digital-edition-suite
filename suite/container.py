"""
This module contains containers of the suite
"""
# author: Kaan Eraslan
# license: see, LICENSE

from suite.primitive import ConstraintString, NonNumericString


class Pair:
    "Models spec container Pair"

    def __init__(self, str1: str, str2: str):
        self.str1 = str1
        self.str2 = str2

    def __iter__(self):
        "Make a pair iterable"
        return iter((self.str1, self.str2))

    def isValid(self):
        return (isinstance(self.str1, str) and
                isinstance(self.str2, str))


class SingleConstraintPair(Pair):
    "Models spec container Single Constraint Pair"

    def __init__(self, str1: str, str2: str, constfn: lambda x: x):
        super().__init__(str1, str2)
        self.constfn = constfn

    def isValid(self):
        "Is valid constraint"
        return self.constfn(self.str1) and self.constfn(self.str2)


class DoubleConstraintPair(Pair):
    "Models spec container Double Constraint Pair"

    def __init__(self, str1: str, str2: str, constfn1: lambda x: x,
                 constfn2: lambda x: x):
        ""
        super().__init__(str1, str2)
        self.constfn1 = constfn1
        self.constfn2 = constfn2

    def isValid(self):
        "is valid pair"
        return self.constfn1(self.str1) and self.constfn2(self.str2)


class NestedPair(Pair):
    "Models spec container Nested Pair"

    def __init__(self, str1: str, npair: Pair):
        self.str1 = str1
        self.pair = npair

    def isValid(self):
        return isinstance(self.str1, str) and self.pair.isValid()


class ConstraintNestedPair(NestedPair):
    "Models spec container Constraint Nested Pair"

    def __init__(self, str1: ConstraintString,
                 npair: Pair):
        self.str1 = str1
        self.pair = npair

    def isValid(self):
        return self.str1.isValid() and self.pair.isValid()


class ConstraintNestedSingleConstraintPair(NestedPair):
    "Models spec container Constraint Nested Single Constraint Pair"

    def __init__(self, str1: ConstraintString,
                 npair: SingleConstraintPair):
        self.str1 = str1
        self.npair = npair

    def isValid(self):
        return self.str1.isValid() and self.npair.isValid()


class StringTuple:
    "Models Tuple container from spec"

    def __init__(self, strset: frozenset):
        self.strset = strset

    def isValid(self):
        "is valid string tuple"
        return all([isinstance(v, str) for v in self.strset])

    def __iter__(self):
        return iter(self.strset)


class SingleConstraintTuple(StringTuple):
    "Models spec container Single Constraint Tuple"

    def __init__(self, strset: frozenset, constfn: lambda x: x):
        super().__init__(strset)
        self.strset = strset
        self.constfn = constfn

    def isValid(self):
        return all([self.constfn(el) for el in self.strset])


class PairTuple:
    "Models Pair Tuple container from spec"

    def __init__(self, pairset: frozenset):
        self.pairset = pairset

    def isValid(self):
        return all([isinstance(v, Pair) for v in self.pairset])

    def __iter__(self):
        return iter(self.pairset)


class SinglePairTuple(PairTuple):
    "Models Single Pair Tuple container from spec"

    def __init__(self, pairset: frozenset):
        super().__init__(pairset)

    def isValid(self):
        return all([isinstance(p, SingleConstraintPair) for p in self.pairset])


class MixedPair:
    "Models Mixed Pair container from spec"

    def __init__(self, str1: ConstraintString, tpl: StringTuple):
        self.str1 = str1
        self.tpl = tpl

    def isValid(self):
        return self.str1.isValid() and self.tpl.isValid()

    def __iter__(self):
        return iter((self.str1, self.tpl))


class SingleConstraintMixedPair(MixedPair):
    "Models spec container Single Constraint Mixed Pair"

    def __init__(self, str1: ConstraintString,
                 strset: SingleConstraintTuple):
        super().__init__(str1, strset)
        assert isinstance(str1, ConstraintString)
        assert isinstance(strset, SingleConstraintTuple)


class NonNumericMixedPair(SingleConstraintMixedPair):
    "Derives spec container Single Constraint Mixed Pair"

    def __init__(self, str1: NonNumericString,
                 strset: SingleConstraintTuple):
        super().__init__(str1, strset)
        assert isinstance(str1, ConstraintString)
        assert isinstance(strset, SingleConstraintTuple)
        assert all([s.isValid() for s in strset])
