###############
Specifications
###############

Wording in this document conforms to `RFC 2119
<https://tools.ietf.org/html/rfc2119>`_.

Primitives
===========

All primitives are immutable.

- :code:`Character`: A character is defined to be that which has a unicode code point value.

- :code:`String`: A string is defined to be a ordered list of characters. 

- :code:`Constant String`: a :code:`String` whose size, number of characters,
  and elements, characters, can not change once initiated. 

- :code:`Constraint String`: a :code:`Constant String` who satisfies a
  constraint expressed as boolean condition.

- :code:`Non Numeric String`: a :code:`Constraint String` whose elements do
  not only consist of characters that can be evaluated as numeric expressions.


Containers
=========== 


All containers are immutable.

- :code:`Pair`: a set with 2 members:

    - a :code:`Constant String`
    - a :code:`Constant String`
    
- :code:`Single Constraint Pair`: a :code:`Pair` whose elements are of
  :code:`Constraint String` who satisfy the same constraint

- :code:`Double Constraint Pair`: a :code:`Pair` whose elements are of
  :code:`Constraint String` who satisfy different constraints.

- :code:`Tuple`: a set with n members whose elements are of :code:`Constant
  String`

- :code:`Single Constraint Tuple`: a :code:`Tuple` whose elements are of
  :code:`Constraint String` that satisfy the same constraint

- :code:`Single Pair Tuple`: a set with n members whose elements are of
  :code:`Single Constraint Pair`

- :code:`Double Pair Tuple`: a set with n members whose elements are of
  :code:`Double Constraint Pair`

- :code:`Mixed Pair`: a set with 2 members who are:

    - a :code:`Constraint String`
    - a :code:`Tuple`

- :code:`Single Constraint Mixed Pair`: a :code:`Pair` whose members are:

    - a :code:`Constraint String`

    - a :code:`Single Constraint Tuple`

- :code:`Nested Single Constraint Mixed Pair`: a :code:`Pair` whose members
  are:

    - a :code:`Constraint String`

    - a :code:`Single Constraint Mixed Pair`


Format
======

This document contains specifications for the files that is used and
produced in this project.

There are 3 structures used by this suite:

- Simple

- Combined

- Link

Simple
-------

Components
+++++++++++

Simple must have three components: :code: `id, value, definition`.

- :code:`id`: a :code:`Non Numeric String`
- :code:`value`: a :code:`Constant String`
- :code:`definition`: a :code:`Constant String`

:code:`definition` is associated to :code:`value`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`.

The tuple :code:`value-definition` is associated to :code:`id`.  
The cardinality of the association is 1-1. 
Together their type is :code:`Mixed Pair`.

Recommendations
++++++++++++++++

It is recommended to use string as the data type for all the
components. 
It is also recommended to use alpha numeric caracters in 
:code:`id` field, with :code:`,` (:code:`U+002C`, virgule) as
separator if necessary.

Form
+++++

Simple Structure may have the following form:

.. code:: json
    
    {"id": {"value": "definition"}}
    
    
Combined
---------

Components
++++++++++++

Combined must have five components: 
:code:`id1, value, definition, id2, values`:

- :code:`id1`: a :code:`Non Numeric String`
- :code:`value`: a :code:`Constant String`
- :code:`definition`: a :code:`Constant String`
- :code:`id2`: a :code:`Non Numeric String`
- :code:`values`: a :code:`Single Constraint Tuple`, whose elements are of
  :code:`Non Numeric String`

:code:`definition` is associated to :code:`value`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`.


:code:`id2` is associated to :code:`values`.
The cardinality of the association is 1-1.
Together their type is :code:`Single Constraint Mixed Pair`. The constraint
that applies to both of the components is :code:`Non Numeric String`


:code:`id1` is associated to :code:`id2-values`, and to
:code:`value-definition`. Both associations are 1-1.



Recommendations
++++++++++++++++


Form
+++++

Combined structure may have the following form

.. code:: json
    
    {"id1": {"value": "definition", "id2": ["id3", "id4", "id5"]}}


Link
-----

Components
++++++++++++

Link must have three components :code:`id1, id2, ids`:

- :code:`id1`: a :code:`Non Numeric String`

- :code:`id2`: a :code:`Non Numeric String`

- :code:`ids`: a :code:`Single Constraint Tuple` whose constraint is
  :code:`Non Numeric String`


:code:`id2` is associated to :code:`ids`.
The cardinality of the association is 1-1.
Together their type is :code:`Single Constraint Mixed Pair`. The constraint
that applies to both of the components is :code:`Non Numeric String`


:code:`id1` is associated to :code:`id2-ids`.
The cardinality of the association is 1-n.


Recommendations
++++++++++++++++


Form
+++++

Link structure may have the following form

.. code:: json
    
    {"id1": {"id2": ["id3", "id4", "id5"]}}
 

Content
========

There are 5 content types used by this suite:

- Authority: has Simple or Combined structure

- Relation: has Simple structure

- Predicate: has Link structure

- Entity: has Link structure

- Entity Predicate Link: has Link structure

For all documents that have a link structure, their :code:`id2` component must
be chosen from the :code:`id` component of a Relation document.


If Authority document has a Combined structure, its :code:`id2` component must
be chosen from the :code:`id` component of a Relation document.

Predicate document may contain an :code:`id1` component of another field from
a Predicate document among its :code:`ids` component, that is predicates can
refer to other predicates.:code:`ids` component may also contain :code:`id` or
:code:`id1` component of an Authority document. Predicate document must not
contain other component content besides the specified options.


Entity document may contain an :code:`id1` component of another field from
a Entity document among its :code:`ids` component, that is entities can
refer to other entities. :code:`ids` component may also contain :code:`id` or
:code:`id1` component of an Authority document. Entity document must not
contain other component content besides the specified options.


Entity Predicate Link document must contain :code:`id1` component of a field
in Entity Document. :code:`ids` must consist of :code:`id1` component of
fields of a Predicate Document.


Recommendations
===============

One should standardise the set of relations between a set of predicates and an
entity. Thus at least one simple authority document should be reserved for
relations between a set of predicates and an entity. These relations can be
used outside of their context, but not the inverse, that is a set of
predicates and an entity can not use other relations besides these. This
standardisation procedure is recommended for other documents that use
relations as well. It is necessary to decide this early on since it governs
the mathematical model underlaying the project.


One should also distinguish another representation of a phenomenon from its
definition, a definition can be applied to multiple representations of a
phenomenon, and a representation is that which one can apply the definition of
a phenomenon. A suggestion might be to use "defined as" relation for terms of
definitions and "equals" for representations.

Qualifiers for representations of phenomena can be implemented using relations
as well. It is recommended to use combined authority documents for modeling
these qualifiers.

Another suggestion is to use active verbs when defining relations since they
should lend themselves easily to a usage of functions. They are treated in
effect as a function where the domain is the parent item containing it and
co-domain is the array of items that it maps to, so active verbs help with
their modeling.

Relations must be differentiable, that is for each parent item, the relation
must map to only a unique set of items. When given a parent item, and
a relation, there must be only one output that results from an evaluation of
relation on parent item.
