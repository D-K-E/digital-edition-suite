"""
This module contains models
that are used for documents used by the project
"""
# author: Kaan Eraslan
# license: see, LICENSE

from suite.primitive import NonNumericString
from suite.container import Pair
from suite.container import NonNumericTuple
from suite.container import UniformNonNumericMixedPair

from suite.container import SingleConstraintTuple


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

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is not NotImplemented:
            return not res
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


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
        ntpl = self.make()
        return self.isValidComponent() and isinstance(ntpl, frozenset)

    def make(self):
        "make structure"
        pair = Pair(str1=self.value, str2=self.definition)
        return frozenset((self.idstr, pair))

    def __str__(self):
        return "Simple Structure: " + ",".join([str(e) for e in self.make()])

    def __eq__(self, other):
        if isinstance(other, SimpleStructure):
            cond1 = other.idstr == self.idstr
            cond2 = other.value == self.value
            cond3 = other.definition == self.definition
            return cond1 and cond2 and cond3
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class CombinedStructure(Structure):
    "Models spec structure Combined"

    def __init__(self, id1: NonNumericString,
                 value: str, definition: str,
                 id2: NonNumericString,
                 values: NonNumericTuple):
        assert isinstance(id1, NonNumericString)
        self.id1 = id1
        assert isinstance(value, str)
        self.value = value
        assert isinstance(definition, str)
        self.definition = definition
        assert isinstance(id2, NonNumericString)
        self.id2 = id2
        assert isinstance(values, NonNumericTuple)
        assert all([isinstance(val, NonNumericString) for val in values])
        self.values = values

    def isValidComponent(self):
        cond1 = self.id1.isValid()
        cond2 = self.id2.isValid()
        cond3 = self.values.isValid()
        return cond1 and cond2 and cond3

    def make(self):
        ""
        pair = Pair(str1=self.value, str2=self.definition)
        npair = UniformNonNumericMixedPair(str1=self.id2, strset=self.values)
        return frozenset((self.id1, pair, npair))

    def isValid(self):
        ""
        cond1 = self.isValidComponent()
        tpl = self.make()
        cond2 = all([t.isValid() for t in tpl])
        return cond1 and cond2 and isinstance(tpl, frozenset)

    def __str__(self):
        return "Combined Structure: " + ",".join([str(e) for e in self.make()])

    def __eq__(self, other):
        if isinstance(other, CombinedStructure):
            cond1 = other.id1 == self.id1
            cond2 = other.value == self.value
            cond3 = other.definition == self.definition
            cond4 = other.values == self.values
            cond5 = other.id2 == self.id2
            return bool(cond1 and
                        cond2 and
                        cond3 and
                        cond4 and
                        cond5)
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))


class LinkStructure(Structure):
    "Models spec structure Link"

    def __init__(self, id1: NonNumericString,
                 id2_ids: frozenset):
        assert isinstance(id1, NonNumericString)
        assert isinstance(id2_ids, frozenset)
        assert all(
            [isinstance(p, UniformNonNumericMixedPair) for p in id2_ids]
        )
        self.id1 = id1
        self.id2_ids = id2_ids

    def isValidComponent(self):
        cond1 = all([p.isValid() for p in self.id2_ids])
        return self.id1.isValid() and cond1

    def hasUniqueId2s(self):
        "check if link structure have unique id2"
        id2s = set()
        for pair in self.id2_ids:
            id2 = pair.arg1
            if id2 not in id2s:
                id2s.add(id2)
            else:
                return False
        return True

    def make(self):
        "make an object"
        return frozenset((self.id1, self.id2_ids))

    def isValid(self):
        cond1 = self.isValidComponent()
        tpl = self.make()
        cond2 = isinstance(tpl, frozenset)
        cond3 = self.hasUniqueId2s()
        return cond1 and cond2 and cond3

    def __str__(self):
        return "Link Structure: " + ",".join([str(e) for e in self.make()])

    def __eq__(self, other):
        if isinstance(other, LinkStructure):
            cond1 = other.id1 == self.id1
            cond2 = other.id2_ids == self.id2_ids
            return cond1 and cond2
        return NotImplemented

    def __hash__(self):
        items = list(self.__dict__.items())
        items.sort()
        return hash(tuple(items))
