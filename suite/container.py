"""
This module contains containers of the suite
"""
# author: Kaan Eraslan
# license: see, LICENSE

from suite.primitive import ConstraintString, NonNumericString


class BasePair:
    "Abstract class for all pairs in spec container"

    def __init__(self, arg1, arg2, arg1type, arg2type):
        mess = "arg1 needs to be of type " + str(arg1type)
        assert isinstance(arg1, arg1type), mess
        mess = "arg2 needs to be of type " + str(arg2type)
        assert isinstance(arg2, arg2type), mess
        self.arg1 = arg1
        self.arg2 = arg2

    def __iter__(self):
        "Make a pair iterable"
        return iter((self.arg1, self.arg2))

    def isValid(self):
        cond1 = self.arg1.isValid()
        cond2 = self.arg2.isValid()
        return cond1 and cond2

    def __str__(self):
        return "Pair: ({0}, {1})".format(str(self.arg1), str(self.arg2))

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is not NotImplemented:
            return not res
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))

    def __eq_proc__(self, other):
        cond1 = other.arg1 == self.arg1
        cond2 = other.arg2 == self.arg2
        return cond1 and cond2


class Pair(BasePair):
    "Models spec container Pair"

    def __init__(self, str1: str, str2: str):
        super().__init__(str1, str2, str, str)

    def isValid(self):
        return True

    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class SingleConstraintPair(BasePair):
    "Models spec container Single Constraint Pair"

    def __init__(self, str1: ConstraintString,
                 str2: ConstraintString):
        super().__init__(str1, str2, ConstraintString, ConstraintString)
        myfn = str1.fn
        mess = "anonymous functions are not allowed as constraints"
        assert myfn.__name__ != "<lambda>", mess
        mess = "constraint strings are not bound to same constraint"
        assert str1.fn.__name__ == str2.fn.__name__, mess
        self.constfn = myfn

    def __eq__(self, other):
        if isinstance(other, SingleConstraintPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class DoubleConstraintPair(BasePair):
    "Models spec container Double Constraint Pair"

    def __init__(self, str1: ConstraintString,
                 str2: ConstraintString):
        ""
        super().__init__(str1, str2, ConstraintString, ConstraintString)
        myfn1 = str1.fn
        myfn2 = str2.fn
        mess = "anonymous functions are not allowed as constraints"
        assert myfn1.__name__ != "<lambda>", mess + " see str1 argument"
        assert myfn2.__name__ != "<lambda>", mess + " see str2 argument"
        mess = "Arguments need to have different constraints"
        assert myfn1.__name__ != myfn2.__name__, mess

    def __eq__(self, other):
        if isinstance(other, DoubleConstraintPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class NestedPair(BasePair):
    "Models spec container Nested Pair"

    def __init__(self, str1: str, npair: Pair):
        super().__init__(str1, npair, str, Pair)

    def isValid(self):
        cond1 = self.arg2.isValid()
        return cond1

    def __eq__(self, other):
        if isinstance(other, NestedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class ConstraintNestedPair(BasePair):
    "Models spec container Constraint Nested Pair"

    def __init__(self, str1: ConstraintString,
                 npair: Pair):
        super().__init__(str1, npair,
                         ConstraintString, Pair)

    def __eq__(self, other):
        if isinstance(other, ConstraintNestedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class ConstraintNestedSingleConstraintPair(BasePair):
    "Models spec container Constraint Nested Single Constraint Pair"

    def __init__(self, str1: ConstraintString,
                 npair: SingleConstraintPair):
        super().__init__(str1, npair,
                         ConstraintString,
                         SingleConstraintPair)

    def __eq__(self, other):
        if isinstance(other, ConstraintNestedSingleConstraintPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class BaseTuple:
    "Abstract class for containers in spec"

    def __init__(self, tpl, tpltype, elType):
        assert isinstance(tpl, tpltype)
        assert all([isinstance(e, elType) for e in tpl])

        self.elements = tpl

    def __iter__(self):
        return iter(self.elements)

    def isValid(self):
        return all([el.isValid() for el in self.elements])

    def __str__(self):
        return "Tuple (" + ",".join(self.elements) + ")"

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is not NotImplemented:
            return not res
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))

    def __eq__(self, other):
        if isinstance(other, BaseTuple):
            return other.elements == self.elements
        return NotImplemented


class StringTuple(BaseTuple):
    "Models Tuple container from spec"

    def __init__(self, strset: frozenset):
        super().__init__(strset, frozenset, str)

    def isValid(self):
        return True

    def __eq__(self, other):
        if isinstance(other, StringTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class SingleConstraintTuple(BaseTuple):
    "Models spec container Single Constraint Tuple"

    def __init__(self,
                 strset: frozenset
                 ):
        super().__init__(strset,
                         frozenset,
                         ConstraintString)
        fncs = set([s.fn.__name__ for s in strset])
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    def __eq__(self, other):
        if isinstance(other, SingleConstraintTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class NonNumericTuple(BaseTuple):
    "Derives Single Constraint Tuple"

    def __init__(self, strset: frozenset):
        super().__init__(strset,
                         frozenset,
                         NonNumericString)
        fncs = set([s.fn.__name__ for s in strset])
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    def __eq__(self, other):
        if isinstance(other, NonNumericTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class PairTuple(BaseTuple):
    "Models Pair Tuple container from spec"

    def __init__(self, pairset: frozenset):
        super().__init__(pairset, frozenset, Pair)

    def __eq__(self, other):
        if isinstance(other, PairTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class SinglePairTuple(BaseTuple):
    "Models Single Pair Tuple container from spec"

    def __init__(self, pairset: frozenset):
        super().__init__(pairset, frozenset,
                         SingleConstraintPair)

    def __eq__(self, other):
        if isinstance(other, SinglePairTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class UniformPairTuple(BaseTuple):
    "Models Uniform Pair Tuple container from spec"

    def __init__(self, pairset: frozenset):
        super().__init__(pairset, frozenset,
                         SingleConstraintPair)
        fncs = set([p.arg1.fn.__name__ for p in pairset])
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    def __eq__(self, other):
        if isinstance(other, UniformPairTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class MixedPair(BasePair):
    "Models Mixed Pair container from spec"

    def __init__(self, str1: ConstraintString, tpl: StringTuple):
        super().__init__(str1, tpl,
                         ConstraintString,
                         StringTuple)

    def __eq__(self, other):
        if isinstance(other, MixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class SingleConstraintMixedPair(BasePair):
    "Models spec container Single Constraint Mixed Pair"

    def __init__(self, str1: ConstraintString,
                 strset: SingleConstraintTuple):
        super().__init__(str1, strset,
                         ConstraintString,
                         SingleConstraintTuple)

    def __eq__(self, other):
        if isinstance(other, SingleConstraintMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class UniformMixedPair(BasePair):
    "Models spec container Uniform Mixed Pair"

    def __init__(self, str1: ConstraintString,
                 strset: SingleConstraintTuple):
        super().__init__(str1, strset,
                         ConstraintString,
                         SingleConstraintTuple)
        fncs = set([p.fn.__name__ for p in strset])
        fncs.add(str1.fn.__name__)
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    def __eq__(self, other):
        if isinstance(other, UniformMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class NonNumericMixedPair(BasePair):
    "Derives spec container Single Constraint Mixed Pair"

    def __init__(self, str1: NonNumericString,
                 strset: SingleConstraintTuple):
        super().__init__(str1, strset,
                         NonNumericString,
                         SingleConstraintTuple)

    def __eq__(self, other):
        if isinstance(other, NonNumericMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class UniformNonNumericMixedPair(BasePair):
    "Derives spec container Uniform Mixed Pair"

    def __init__(self, str1: NonNumericString,
                 strset: NonNumericTuple):
        super().__init__(str1, strset,
                         NonNumericString,
                         NonNumericTuple)
        fncs = set([p.fn.__name__ for p in strset])
        fncs.add(str1.fn.__name__)
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    def __eq__(self, other):
        if isinstance(other, UniformNonNumericMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))
