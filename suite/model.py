"""
This module contains models
that are used for documents used by the project
"""
# author: Kaan Eraslan
# license: see, LICENSE


class ConstraintString:
    "Models spec primitive Constraint String"

    def __init__(self, my_string: str, constraint: lambda x: x):
        ""
        self.cstr = my_string
        self.fn = constraint

    def isValid(self):
        "Is string valid for given constraint"
        return self.fn(self.cstr)


class NonNumericString(ConstraintString):
    "Models spec primitive Non Numeric String"

    def __init__(self, my_string: str):
        def constfn(x: str): return x.isnumeric()
        super().__init__(my_string, constfn)


class Pair:
    "Models spec container Pair"

    def __init__(self, str1: str, str2: str):
        self.str1 = str1
        self.str2 = str2


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


class SingleConstraintTuple:
    "Models spec container Single Constraint Tuple"

    def __init__(self, strset: frozenset, constfn: lambda x: x):
        self.strset = strset
        self.constfn = constfn

    def isValid(self):
        return all([self.constfn(el) for el in self.strset])


class SingleConstraintMixedPair:
    "Models spec container Single Constraint Mixed Pair"

    def __init__(self, str1: ConstraintString, strset: SingleConstraintTuple):
        self.str1 = str1
        self.strset = strset

    def isValid(self):
        return self.str1.isValid() and self.strset.isValid()


class SimpleStructure:
    "Simple structure"

    def __init__(self, idstr: NonNumericString, value: str, definition: str):
        self.idstr = idstr
        self.value = value
        self.definition = definition

    def isValid(self):
        return (isinstance(self.value, str) and
                isinstance(self.definition, str) and
                self.idstr.isValid())

