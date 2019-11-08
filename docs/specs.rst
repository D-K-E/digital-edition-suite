###############
Specifications
###############

Wording in this document conforms to `RFC 2119
<https://tools.ietf.org/html/rfc2119>`_.

Primitives
===========

All primitives are immutable.

- :code:`Character`: A character is defined to be that which has a unicode
  code point value.
  
- :code:`FloatingPoint`: A floating number. Its representation consist of :code:`[-]NumericExpression.NumericExpression`.
  For example, :code:`64.4253` or :code:`-68.123328`.

- :code:`String`: A string is defined to be a ordered list of characters. 

- :code:`Constant String`: a :code:`String` whose size, number of characters,
  and elements, characters, can not change once initiated. 

- :code:`Constraint String`: a :code:`Constant String` who satisfies a name
  bound constraint that evaluates to a boolean condition.

- :code:`Non Numeric String`: a :code:`Constraint String` whose elements do
  not only consist of characters that can be evaluated as numeric expressions.


Containers
=========== 


All containers are immutable.

- :code:`Array`: a set with n members whose elements are of the 
  same type.

- :code:`Pair`: a set with 2 members whose elements are of different
  type.
  
  
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

- :code:`id`: a subclass of :code:`Non Numeric String`
- :code:`value`: a subclass of :code:`Constant String`
- :code:`definition`: a subclass of :code:`Constant String`

:code:`definition` is associated to :code:`value`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair` of size 2.

The array :code:`value-definition` is associated to :code:`id`.  
The cardinality of the association is 1-1. 
Together their type is :code:`Pair`.

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

- :code:`id1`: a subclass of :code:`Non Numeric String`
- :code:`value`: a subclass of :code:`Constant String`
- :code:`definition`: a subclass of :code:`Constant String`
- :code:`id2`: a subclass of :code:`Non Numeric String`
- :code:`values`: a subclass of :code:`Array`, whose elements are of
  :code:`Non Numeric String`

:code:`definition` is associated to :code:`value`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`.


:code:`id2` is associated to :code:`values`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`. The constraint
that applies to both of the components is :code:`Non Numeric String`


:code:`id2-values` is associated to :code:`value-definition`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`

:code:`id1` is associated to :code:`id2-values-value-definition`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`



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

- :code:`id2-ids`: a :code:`Array` whose members are :code:`Pair` composed of:

    - :code:`id2`: a :code:`Non Numeric String`
    - :code:`ids` a :code:`Array` whose members are of :code:`Non Numeric String`

:code:`id1` is associated to :code:`id2-ids`.
The cardinality of the association is 1-1.
Together their type is :code:`Pair`


Recommendations
++++++++++++++++


Form
+++++

Link structure may have the following form

.. code:: json
    
    {"id1": {"id2": ["id3", "id4", "id5"], "id6": ["id7", "id8"]}}
 

Content
========

There are 5 content types used by this suite:

- Singular: has Simple structure

- Unit: has Combined structure

- Relation: has Combined structure

- Predicate: has Link structure

- Entity: has Link structure

Underlaying Mathematical Object
--------------------------------

The underlying mathematical object for our model is
a directed hyper graph where nodes are singular. 
Unit is a hyperedge, just like a relation. Predicate or
Entity is a grouping of units with different relations.

Relation models a differentiable function, so suite has to ensure
that they stay continous and differentiable.

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
