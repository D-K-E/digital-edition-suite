"""
This module contains primitives of the suite
"""
# author: Kaan Eraslan
# license: see, LICENSE

from fractions import Fraction


class ConstraintString:
    "Models spec primitive Constraint String"

    def __init__(self, my_string: str, constraint: lambda x: x):
        ""
        assert isinstance(my_string, str)
        mess = "anonymous functions are not allowed as constraints"
        assert constraint.__name__ != "<lambda>", mess
        self.cstr = my_string
        self.fn = constraint

    def isValid(self):
        "Is string valid for given constraint"
        return self.fn(self.cstr)

    def __str__(self):
        return "constraint string: " + self.cstr

    def __eq__(self, other):
        if isinstance(other, ConstraintString):
            cond1 = other.cstr == self.cstr
            cond2 = other.fn.__name__ == self.fn.__name__
            return cond1 and cond2
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


def nonNumeric(x: str):
    try:
        mystr = int(x)
    except ValueError:
        try:
            mystr = float(x)
        except ValueError:
            try:
                mystr = Fraction(x)
            except ValueError:
                try:
                    mystr = complex(x)
                except ValueError:
                    mystr = x
    return not isinstance(mystr, (float, int, complex, Fraction))


class NonNumericString(ConstraintString):
    "Models spec primitive Non Numeric String"

    def __init__(self, my_string: str):
        super().__init__(my_string, nonNumeric)

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))

    def __eq__(self, other):
        if isinstance(other, ConstraintString):
            cond1 = other.cstr == self.cstr
            cond2 = other.fn.__name__ == self.fn.__name__
            return cond1 and cond2
        return NotImplemented

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is not NotImplemented:
            return not res
        return NotImplemented
