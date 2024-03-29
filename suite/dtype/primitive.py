"""
This module contains primitives of the suite
"""
# author: Kaan Eraslan
# license: see, LICENSE

from fractions import Fraction

from typing import NamedTuple
from types import FunctionType


class BasePrimitive:
    "Base class for all primitives"

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is not NotImplemented:
            return not res
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class ConstantStringBase(NamedTuple):
    "Models spec primitive Constant String"
    constr: str


class ConstantString(BasePrimitive, ConstantStringBase):
    def isValid(self):
        "Check if constant string is valid"
        check = True
        try:
            mybyte = self.constr.encode("utf-8")
            mystr = mybyte.decode("utf-8")
            check = mystr == self.constr
        except UnicodeDecodeError or UnicodeEncodeError:
            check = False
        return check

    def __repr__(self):
        return "string: " + str(self) + " of type: " + self.__class__.__name__

    def __str__(self):
        return self.constr

    def __eq__(self, other):
        if isinstance(other, ConstantString):
            cond1 = other.constr == self.constr
            return cond1
        return NotImplemented

    def __copy__(self):
        return ConstantString(constr=self.constr)

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class ConstraintStringBase(NamedTuple):
    cstr: ConstantString
    fn: FunctionType

    def isValid(self):
        "Is string valid for given constraint"
        return self.fn(self.cstr)

    def __str__(self):
        return str(self.cstr)

    def __repr__(self):
        mess = "string: " + str(self) + " of type: " + self.__class__.__name__
        mess += " with constraint: " + self.fn.__name__
        return mess

    def __eq__(self, other):
        if isinstance(other, ConstraintString):
            cond1 = other.cstr == self.cstr
            cond2 = other.fn.__name__ == self.fn.__name__
            return cond1 and cond2
        return NotImplemented


class ConstraintString(BasePrimitive, ConstraintStringBase):
    def __copy__(self):
        return ConstraintString(cstr=self.cstr, fn=self.fn)

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


def nonNumeric(myx: ConstantString) -> bool:
    x = myx.constr
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


class NonNumericStringBase(NamedTuple):
    cstr: ConstantString

    @property
    def fn(self):
        return nonNumeric

    def isValid(self):
        "Is string valid for given constraint"
        return self.fn(self.cstr)

    def __str__(self):
        return str(self.cstr)

    def __repr__(self):
        mess = "string: " + str(self) + " of type: " + self.__class__.__name__
        mess += " with constraint: " + self.fn.__name__
        return mess


class NonNumericString(NonNumericStringBase, BasePrimitive):
    "Models spec primitive Non Numeric String"

    def __eq__(self, other):
        if isinstance(other, NonNumericString):
            cond1 = other.cstr == self.cstr
            cond2 = other.fn.__name__ == self.fn.__name__
            return cond1 and cond2
        return NotImplemented

    def __copy__(self):
        return NonNumericString(cstr=self.cstr, fn=self.fn)

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class PrimitiveMaker:
    ""

    def __init__(self, choice: str):
        self.choice = choice

    @classmethod
    def make_constant_string(cls, mystr: str):
        mess = "Incompatible type: " + type(mystr).__name__
        mess += ". Only str type is allowed"
        if not isinstance(mystr, str):
            raise TypeError(mess)
        constr = ConstantString(constr=mystr)
        if not constr.isValid():
            raise ValueError("Not valid ConstantString: " + str(constr))
        return constr

    @classmethod
    def make_constraint_string(cls, mystr: ConstantString, fnc: FunctionType):
        mess = "Incompatible type: " + type(mystr).__name__
        mess += ". Only ConstantString type is allowed"
        if not isinstance(mystr, ConstantString):
            raise TypeError(mess)
        mess = "Incompatible type: " + type(fnc).__name__
        mess += ". Only FunctionType type is allowed"
        if not isinstance(fnc, FunctionType):
            raise TypeError(mess)
        fname = fnc.__name__
        mess = "Anonymous functions are not allowed."
        if not fname != "<lambda>":
            raise ValueError(mess)
        cstr = ConstraintString(cstr=mystr, fn=fnc)
        if not cstr.isValid():
            raise ValueError("Invalid ConstraintString: " + str(cstr))
        return cstr

    @classmethod
    def make_non_numeric_string(cls, mystr: ConstantString):
        mess = "Incompatible type: " + type(mystr).__name__
        mess += ". Only ConstantString type is allowed"
        if not isinstance(mystr, ConstantString):
            raise TypeError(mess)
        nnstr = NonNumericString(cstr=mystr)
        if not nnstr.isValid():
            raise ValueError("Not valid NonNumericString: " + str(nnstr))
        return nnstr

    def make(self, **kwargs):
        choice = self.choice.lower()
        if choice == "constant string":
            return self.make_constant_string(**kwargs)
        elif choice == "constraint string":
            return self.make_constraint_string(**kwargs)
        elif choice == "non numeric string":
            return self.make_non_numeric_string(**kwargs)
        else:
            raise ValueError("Unknown primitive choice: " + choice)

    def from_string(self, mystr: str, **kwargs):
        "make object from choice using string"
        choice = self.choice.lower()
        mess = "Incompatible type: " + type(mystr).__name__
        mess += ". Only str type is allowed"
        if not isinstance(mystr, str):
            raise TypeError(mess)
        if choice == "constant string":
            return self.make_constant_string(mystr)
        elif choice == "constraint string":
            cstr = self.make_constant_string(mystr)
            return self.make_constraint_string(mystr=cstr, **kwargs)
        elif choice == "non numeric string":
            cstr = self.make_constant_string(mystr)
            return self.make_non_numeric_string(mystr=cstr)
        else:
            raise ValueError("Unknown primitive choice: " + choice)

    @classmethod
    def from_type(cls, primitiveType, **kwargs):
        "make primitive from giving its type"
        pname = primitiveType.__name__
        if pname == "ConstantString":
            return cls.make_constant_string(**kwargs)
        elif pname == "ConstraintString":
            return cls.make_constraint_string(**kwargs)
        elif pname == "NonNumericString":
            return cls.make_non_numeric_string(**kwargs)
        else:
            raise ValueError("Unknown Primitive Type: " + pname)
