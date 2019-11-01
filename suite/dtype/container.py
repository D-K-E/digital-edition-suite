"""
This module contains containers of the suite
"""
# author: Kaan Eraslan
# license: see, LICENSE

from suite.dtype.primitive import ConstraintString, NonNumericString
from suite.dtype.primitive import ConstantString
from typing import NamedTuple
from types import FunctionType


class BasePair:
    "Abstract class for all pairs in spec container"

    def __iter__(self):
        "Make a pair iterable"
        return iter(set(self.arg1, self.arg2))

    def isValid(self):
        cond1 = self.arg1.isValid()
        cond2 = self.arg2.isValid()
        return cond1 and cond2

    def __repr__(self):
        return "Pair: ({0}, {1})".format(repr(self.arg1), repr(self.arg2))

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


class PairBase(NamedTuple):
    "Models spec container Pair"
    arg1: ConstantString
    arg2: ConstantString


class Pair(BasePair, PairBase):
    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def single_constraint_pair_check_pair(arg1, arg2, arg1type, arg2type):
    pair_init_check_proc(arg1, arg2, arg1type, arg2type)


class SingleConstraintPairBase(NamedTuple):
    arg1: ConstraintString
    arg2: ConstraintString


class SingleConstraintPair(BasePair, SingleConstraintPairBase):
    "Models spec container Single Constraint Pair"

    def __eq__(self, other):
        if isinstance(other, SingleConstraintPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def double_constraint_pair_init_check_proc(arg1, arg2, arg1type, arg2type):
    pair_init_check_proc(arg1, arg2, arg1type, arg2type)


class DoubleConstraintPairBase(NamedTuple):
    arg1: ConstraintString
    arg2: ConstraintString


class DoubleConstraintPair(BasePair, DoubleConstraintPairBase):
    "Models spec container Double Constraint Pair"

    def __eq__(self, other):
        if isinstance(other, DoubleConstraintPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def nested_pair_check_proc(arg1, arg2, arg1type, arg2type):
    pair_init_check_proc(arg1, arg2, arg1type, arg2type)


class NestedPairBase(NamedTuple):
    arg1: ConstantString
    arg2: Pair


class NestedPair(BasePair, NestedPairBase):
    "Models spec container Nested Pair"

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


def constraint_nested_pair_check_proc(arg1, arg2, arg1type, arg2type):
    pair_init_check_proc(arg1, arg2, arg1type, arg2type)


class ConstraintNestedPairBase(NamedTuple):
    "Models spec container Constraint Nested Pair"
    arg1: ConstraintString
    arg2: Pair


class ConstraintNestedPair(BasePair, ConstraintNestedPairBase):
    def __eq__(self, other):
        if isinstance(other, ConstraintNestedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def constraint_nested_single_pair_check_proc(arg1, arg2, arg1type, arg2type):
    pair_init_check_proc(arg1, arg2, arg1type, arg2type)


class ConstraintNestedSingleConstraintPairBase(NamedTuple):
    arg1: ConstraintString
    arg2: SingleConstraintPair


class ConstraintNestedSingleConstraintPair(
    BasePair, ConstraintNestedSingleConstraintPairBase
):
    "Models spec container Constraint Nested Single Constraint Pair"

    def __eq__(self, other):
        if isinstance(other, ConstraintNestedSingleConstraintPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def base_tuple_init_check_proc(tpl, tplType, elType):
    assert isinstance(tpl, tpltype)
    assert all([isinstance(e, elType) for e in tpl])


class BaseTuple:
    "Abstract class for containers in spec"

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


class StringTupleBase(NamedTuple):
    elements: frozenset


class StringTuple(BaseTuple, StringTupleBase):
    "Models Tuple container from spec"

    def __eq__(self, other):
        if isinstance(other, StringTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class SingleConstraintTupleBase(NamedTuple):
    elements: frozenset


class SingleConstraintTuple(BaseTuple, SingleConstraintTupleBase):
    "Models spec container Single Constraint Tuple"

    def __eq__(self, other):
        if isinstance(other, SingleConstraintTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class NonNumericTupleBase(NamedTuple):
    elements: frozenset


class NonNumericTuple(BaseTuple, NonNumericTupleBase):
    "Derives Single Constraint Tuple"

    def __eq__(self, other):
        if isinstance(other, NonNumericTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class PairTupleBase(NamedTuple):
    elements: frozenset


class PairTuple(BaseTuple, PairTupleBase):
    "Models Pair Tuple container from spec"

    def __eq__(self, other):
        if isinstance(other, PairTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def single_pair_tuple_init_check_proc(tpl):
    assert isinstance(tpl, frozenset)
    assert all([isinstance(e, SingleConstraintPair) for e in tpl])


class SinglePairTupleBase(NamedTuple):
    elements: frozenset


class SinglePairTuple(BaseTuple, SinglePairTupleBase):
    "Models Single Pair Tuple container from spec"

    def __eq__(self, other):
        if isinstance(other, SinglePairTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class UniformPairTupleBase(NamedTuple):
    elements: frozenset


class UniformPairTuple(BaseTuple, UniformPairTupleBase):
    "Models Uniform Pair Tuple container from spec"

    def __eq__(self, other):
        if isinstance(other, UniformPairTuple):
            return other.elements == self.elements
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def mixed_pair_init_check_proc(arg1, arg2):
    pair_init_check_proc(arg1, arg2, ConstraintString, StringTuple)


class MixedPairBase(NamedTuple):
    arg1: ConstraintString
    arg2: StringTuple


class MixedPair(BasePair, MixedPairBase):
    "Models Mixed Pair container from spec"

    def __eq__(self, other):
        if isinstance(other, MixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def single_constraint_mixed_pair_init_check_proc(arg1, arg2):
    pair_init_check_proc(arg1, arg2, ConstraintString, SingleConstraintTuple)


class SingleConstraintMixedPairBase(NamedTuple):
    arg1: ConstraintString
    arg2: SingleConstraintTuple


class SingleConstraintMixedPair(BasePair, SingleConstraintMixedPairBase):
    "Models spec container Single Constraint Mixed Pair"

    def __eq__(self, other):
        if isinstance(other, SingleConstraintMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def uniform_mixed_pair_init_check_proc(arg1, arg2):
    pair_init_check_proc(arg1, arg2, ConstraintString, SingleConstraintTuple)
    fncs = set([p.fn.__name__ for p in arg2])
    fncs.add(str1.fn.__name__)
    assert len(fncs) == 1
    fncs = list(fncs)
    fnc = fncs[0]
    assert fnc != "<lambda>"


class UniformMixedPairBase(NamedTuple):
    arg1: ConstraintString
    arg2: SingleConstraintTuple


class UniformMixedPair(BasePair, UniformMixedPairBase):
    "Models spec container Uniform Mixed Pair"

    def __eq__(self, other):
        if isinstance(other, UniformMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def non_numeric_mixed_pair_init_check_proc(arg1, arg2):
    pair_init_check_proc(arg1, arg2, NonNumericString, SingleConstraintTuple)


class NonNumericMixedPairBase(NamedTuple):
    arg1: NonNumericString
    arg2: SingleConstraintTuple


class NonNumericMixedPair(BasePair, NonNumericMixedPairBase):
    "Derives spec container Single Constraint Mixed Pair"

    def __eq__(self, other):
        if isinstance(other, NonNumericMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def uniform_non_numeric_mixed_pair_init_check_proc(arg1, arg2):
    pair_init_check_proc(arg1, arg2, NonNumericString, SingleConstraintTuple)
    fncs = set([p.fn.__name__ for p in arg2])
    fncs.add(arg1.fn.__name__)
    assert len(fncs) == 1
    fncs = list(fncs)
    fnc = fncs[0]
    assert fnc != "<lambda>"


class UniformNonNumericMixedPairBase(NamedTuple):
    arg1: NonNumericString
    arg2: NonNumericTuple


class UniformNonNumericMixedPair(BasePair, UniformNonNumericMixedPairBase):
    "Derives spec container Uniform Mixed Pair"

    def __eq__(self, other):
        if isinstance(other, UniformNonNumericMixedPair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class ContainerMaker:
    "Container maker"

    def __init__(self):
        pass

    @staticmethod
    def pair_init_check_proc(arg1, arg2, arg1type, arg2type):
        mess = "arg1 needs to be of type " + str(arg1type)
        assert isinstance(arg1, arg1type), mess
        mess = "arg2 needs to be of type " + str(arg2type)
        assert isinstance(arg2, arg2type), mess
        assert arg1.isValid()
        assert arg2.isValid()

    @staticmethod
    def single_constraint_pair_init_check_proc(arg1, arg2):
        ContainerMaker.pair_init_check_proc(
            arg1, arg2, ConstraintString, ConstraintString
        )
        myfn = arg1.fn
        mess = "anonymous functions are not allowed as constraints"
        assert arg1.__name__ != "<lambda>", mess
        mess = "constraint strings are not bound to same constraint"
        assert arg1.fn.__name__ == arg2.fn.__name__, mess

    @staticmethod
    def double_constraint_pair_init_check_proc(arg1, arg2):
        ContainerMaker.pair_init_check_proc(
            arg1, arg2, ConstraintString, ConstraintString
        )
        myfn1 = arg1.fn
        myfn2 = arg2.fn
        mess = "anonymous functions are not allowed as constraints"
        assert myfn1.__name__ != "<lambda>", mess + " see arg1 argument"
        assert myfn2.__name__ != "<lambda>", mess + " see arg2 argument"
        mess = "Arguments need to have different constraints"
        assert myfn1.__name__ != myfn2.__name__, mess

    @staticmethod
    def nested_pair_init_check_proc(arg1, arg2):
        ContainerMaker.pair_init_check_proc(arg1, arg2, ConstantString, Pair)

    @staticmethod
    def constraint_nested_pair_check_proc(arg1, arg2):
        ContainerMaker.pair_init_check_proc(arg1, arg2, ConstraintString, Pair)

    @staticmethod
    def constraint_nested_single_pair_check_proc(arg1, arg2):
        ContainerMaker.pair_init_check_proc(
            arg1, arg2, ConstraintString, SingleConstraintPair
        )

    @staticmethod
    def tuple_init_check_proc(els, elsType, elType):
        assert isinstance(els, elsType)
        assert all([isinstance(e, elType) for e in els])

    @staticmethod
    def string_tuple_init_check_proc(els):
        ContainerMaker.tuple_init_check_proc(els, frozenset, ConstantString)

    @staticmethod
    def single_constraint_tuple_init_check_proc(els):
        ContainerMaker.tuple_init_check_proc(els, frozenset, ConstraintString)
        fncs = set([s.fn.__name__ for s in els])
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    @staticmethod
    def non_numeric_tuple_init_check_proc(els):
        ContainerMaker.tuple_init_check_proc(els, frozenset, NonNumericString)
        fncs = set([s.fn.__name__ for s in els])
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    @staticmethod
    def pair_tuple_init_check_proc(els):
        ContainerMaker.tuple_init_check_proc(els, frozenset, Pair)

    @staticmethod
    def single_pair_tuple_init_check_proc(els):
        ContainerMaker.tuple_init_check_proc(els, frozenset, SingleConstraintPair)

    @staticmethod
    def uniform_pair_tuple_init_check_proc(els):
        ContainerMaker.tuple_init_check_proc(els, frozenset, SingleConstraintPair)
        fncs = set([p.arg1.fn.__name__ for p in els])
        assert len(fncs) == 1
        fncs = list(fncs)
        fnc = fncs[0]
        assert fnc != "<lambda>"

    @staticmethod
    def mixed_pair_init_check_proc(arg1, arg2):
        ContainerMaker.pair_init_check_proc(arg1, arg2, ConstraintString, StringTuple)

    @staticmethod
    def make_pair(arg1, arg2):
        ContainerMaker.pair_init_check_proc(arg1, arg2, ConstantString, ConstantString)
        return Pair(arg1, arg2)

    @staticmethod
    def make_single_constraint_pair(arg1, arg2):
        ContainerMaker.single_constraint_pair_init_check_proc(arg1, arg2)
        return SingleConstraintPair(arg1, arg2)

    @staticmethod
    def make_double_constraint_pair(arg1, arg2):
        ContainerMaker.double_constraint_pair_init_check_proc(arg1, arg2)
        return DoubleConstraintPair(arg1, arg2)

    @staticmethod
    def make_nested_pair(arg1, arg2):
        ContainerMaker.nested_pair_init_check_proc(arg1, arg2)
        return NestedPair(arg1, arg2)

    @staticmethod
    def make_constraint_nested_pair(arg1, arg2):
        ContainerMaker.constraint_nested_pair_check_proc(arg1, arg2)
        return ConstraintNestedPair(arg1, arg2)

    @staticmethod
    def make_constraint_nested_single_constraint_pair(arg1, arg2):
        ContainerMaker.constraint_nested_single_pair_check_proc(arg1, arg2)
        return ConstraintNestedSingleConstraintPair(arg1, arg2)

    @staticmethod
    def make_string_tuple(els):
        ContainerMaker.string_tuple_init_check_proc(els)
        return StringTuple(elements=els)

    @staticmethod
    def make_single_constraint_tuple(els):
        ContainerMaker.single_constraint_tuple_init_check_proc(els)
        return SingleConstraintTuple(elements=els)
