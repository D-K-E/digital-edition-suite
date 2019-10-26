"""
This module contains models
that are used for documents used by the project
"""
# author: Kaan Eraslan
# license: see, LICENSE

from suite.primitive import ConstraintString, NonNumericString
from suite.container import Pair
from suite.container import SingleConstraintPair
from suite.container import DoubleConstraintPair
from suite.container import NestedPair
from suite.container import ConstraintNestedPair
from suite.container import ConstraintNestedSingleConstraintPair
from suite.container import StringTuple
from suite.container import SingleConstraintTuple
from suite.container import PairTuple
from suite.container import SinglePairTuple
from suite.container import MixedPair
from suite.container import SingleConstraintMixedPair
from suite.container import NonNumericMixedPair


class Structure:
    "Abstract class for all structure"

    def __init__(self):
        pass

    def isValidComponent(self):
        ""
        raise NotImplementedError

    def isValid(self):
        ""
        raise NotImplementedError

    def make(self):
        ""
        raise NotImplementedError


class SimpleStructure(Structure):
    "Simple structure"

    def __init__(self, idstr: NonNumericString, value: str, definition: str):
        assert isinstance(idstr, NonNumericString)
        assert isinstance(value, str)
        assert isinstance(definition, str)
        self.idstr = idstr
        self.value = value
        self.definition = definition

    def isValidComponent(self):
        return self.idstr.isValid()

    def isValid(self):
        nested = self.make()
        return self.isValidComponent() and nested.isValid()

    def make(self):
        "make structure"
        pair = Pair(str1=self.value, str2=self.definition)
        nested = ConstraintNestedPair(self.idstr, pair)
        return nested


class CombinedStructure(Structure):
    "Models spec structure Combined"

    def __init__(self, id1: NonNumericString,
                 value: str, definition: str,
                 id2: NonNumericString,
                 values: NonNumericMixedPair):
        assert isinstance(id1, NonNumericString)
        self.id1 = id1
        assert isinstance(value, str)
        self.value = value
        assert isinstance(definition, str)
        self.definition = definition
        assert isinstance(id2, NonNumericString)
        self.id2 = id2
        assert isinstance(values, SingleConstraintTuple)
        assert all([isinstance(val, NonNumericString) for val in values])
        self.values = values

    def isValidComponent(self):
        cond1 = self.id1.isValid()
        cond2 = self.id2.isValid()
        cond3 = all([val.isValid() for val in self.values])
        cond4 = self.values.isValid()
        return cond1 and cond2 and cond3 and cond4

    def make(self):
        ""
        pair = Pair(str1=self.value, str2=self.definition)
        npair = NonNumericMixedPair(str1=self.id2, strset=self.values)
        return (self.id1, pair, npair)

    def isValid(self):
        ""
        cond1 = self.isValidComponent()
        tpl = self.make()
        cond2 = all([t.isValid() for t in tpl])
        return cond1 and cond2


class LinkStructure(Structure):
    "Models spec structure Link"

    def __init__(self, id1: NonNumericString,
                 id2_ids: SingleConstraintMixedPair):
        assert isinstance(id1, NonNumericString)
        assert isinstance(id2_ids, NonNumericMixedPair)
        self.id1 = id1
        self.id2_ids = id2_ids

    def isValidComponent(self):
        return self.id1.isValid() and self.id2_ids.isValid()

    def make(self):
        "make an object"
        return (self.id1, self.id2_ids)

    def isValid(self):
        cond1 = self.isValidComponent()
        tpl = self.make()
        cond2 = all([t.isValid() for t in tpl])
        return cond1 and cond2

