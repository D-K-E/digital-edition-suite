"""
This module contains containers of the suite
"""
# author: Kaan Eraslan
# license: see, LICENSE

from suite.dtype.primitive import ConstraintString, NonNumericString
from suite.dtype.primitive import ConstantString
from typing import NamedTuple
from collections import namedtuple
from types import FunctionType


class BasePair:
    "Abstract class for all pairs in spec container"

    def __iter__(self):
        "Make a pair iterable"
        return iter(set((self.arg1, self.arg2)))

    def isValid(self):
        cond1 = self.arg1.isValid()
        cond2 = self.arg2.isValid()
        cond3 = type(self.arg2) != type(self.arg1)
        return cond1 and cond2 and cond3

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


class Pair(BasePair, namedtuple("Pair", "arg1 arg2")):
    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.__eq_proc__(other)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class Array:
    "Models array container from spec"

    def __init__(self, iterable):
        ""
        check = True
        try:
            iterator = iter(iterable)
        except TypeError:
            check = False
        #
        if check is False:
            raise TypeError(
                "Provided object should be an iterable. It is of type: "
                + str(type(iterable))
            )
        firstElement = None
        eltypes = set()
        for item in iterable:
            eltypes.add(type(item))

        if len(eltypes) > 1:
            mess = "Iterable contains different types: " + str(eltypes)

            raise ValueError(mess)
        validCheck = all([el.isValid() for el in iterable])
        if validCheck is False:
            raise ValueError(
                "Array contains invalid objects: "
                + " ".join([el for el in iterable if el.isValid() is False])
            )
        self.elements = frozenset(iterable)

    def isValid(self):
        "If the array is initialized that it should have been valid"
        return True

    def __str__(self):
        return "Array: " + " ".join([el for el in self.elements])

    def __eq__(self, other):
        if isinstance(other, Array):
            return self.elements == other.elements
        return NotImplemented

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is not NotImplemented:
            return not res
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class ContainerMaker:
    "Container maker"

    def __init__(self, choice: str):
        self.choice = choice

    def make_pair(self, arg1, arg2):
        "Make pair using arg1 and arg2"
        p = Pair(arg1=arg1, arg2=arg2)
        if p.isValid() is False:
            mess = "\n  - each argument is valid"
            mess += mess + "\n  - arguments are of different type"
            raise ValueError(
                "Pair initialized with invalid parameters. Make sure: " + mess
            )
        return

    def make_array(self, els):
        "make array using iterable"
        arr = Array(iterable=els)
        if arr.isValid() is False:
            mess = "\n  - each argument is valid"
            mess += mess + "\n  - arguments are of same type"
            raise ValueError(
                "Array initialized with invalid parameters. Make sure: " + mess
            )
        return arr

    @classmethod
    def from_type(cls, objType, **kwargs):
        objname = objType.__name__
        if objname == "Pair":
            arg1, arg2 = kwargs["arg1"], kwargs["arg2"]
            return cls.make_pair(arg1=arg1, arg2=arg2)
        elif objname == "Array":
            els = kwargs["elements"]
            return cls.make_array(els)
        else:
            raise ValueError("Unknown object type: " + objname)

    def make(self, **kwargs):
        "make object based on choice"
        choice = self.choice.lower()
        if choice == "pair":
            arg1, arg2 = kwargs["arg1"], kwargs["arg2"]
            return self.make_pair(arg1, arg2)
        elif choice == "array":
            els = kwargs["elements"]
            return self.make_array(els)
        else:
            raise ValueError("Unknown choice: " + choice)
