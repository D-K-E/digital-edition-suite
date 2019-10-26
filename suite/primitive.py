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
        self.cstr = my_string
        self.fn = constraint

    def isValid(self):
        "Is string valid for given constraint"
        return self.fn(self.cstr)

    def __str__(self):
        return "constraint string: " + self.cstr


class NonNumericString(ConstraintString):
    "Models spec primitive Non Numeric String"

    def __init__(self, my_string: str):
        def constfn(x: str):
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

        super().__init__(my_string, constfn)
