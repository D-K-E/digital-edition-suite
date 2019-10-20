###############
Specifications
###############

This document contains specifications for the authority files that is used and
produced in this project.

There are 4 main types of document that this suite uses:

- Authority document

- Predicate document

- Entity document

- Entity Predicate Relations document


Authority document has two sub types, namely: simple, combined.

All documents are in :code:`json` format.

Simple Authority Document has the following structure:

.. code:: json

    {"simple-no-1": {"some-value": "value definition"},
     "simple-no-n": {"some-value": "value definition"}}

Keys are of type string. Their value is a :code:`json` object, which has a
single key value pair. Both of them are of string.

Combined Authority Document has the following structure:

.. code:: json

    {
        "combined-id-n": {"value": "value definition",
                          "contains": ["simple-no-0"]}
    }

Keys are of type string. Their value is a :code:`json` object, which has a
double key value pair. First one is a string key with a string associated
value. Second one is a hard coded relation type :code:`contains`. It can be
changed to have another relation documented in another Simple Authority
Document. In any case the reading from left to right should make a sense of
what is being defined to humans. :code:`combined-id-n` :code:`contains` the
following id numbers, in its :code:`value`.

The relations are an important part of our specification because they have
direct impact on the functions that are being employed to modify or render the
authority and related documents.

Predicate Document has the following structure:

.. code:: json

    {
        "predicate-no-0": {"simple-id-0": [
            "combined-id-0",
            "combined-id-1",
            "simple-id-0",
        ]}
    }

Basically it is very much like Combined Authority Document, with the
difference that keys of its associated object are entirely made up of pointers
to authority document parts. Combined Authority Document can still have a
value associated to it, whereas a Predicate Document has only pointers.

Entity Document

.. code:: json

    {"entity-1": {"another-simple-id-no-0": ["simple-id-no-1"]},
    "entity-2": {"another-simple-id-no-0": ["simple-id-no-2"]} ,
    "entity-3": {"another-simple-id-no-0": ["simple-id-no-3"]} ,
    "entity-0": {"another-simple-id-no-1": ["entity-1", "entity-2", "entity-3"]}
    }

Very much like a Predicate Document, with the difference that it can point to
other entities. Predicate Document parts can point to each other and an
authority document. Entity Document parts can point to other entity document
parts and Authority Document parts.

Finally the Entity Predicate Relations Document

.. code:: json

    {"entity-1": {"simple-id-0": ["predicate-1", "predicate-2"]}, 
    "entity-2": {"simple-id-1": ["predicate-2"]}
    }

So far the only relations between a Predicate Document part and an Entity
Document part is that of definition, meaning that we act as if the set of
predicates define the entity. However the schema is extensible to other
relations that can be conceived between a set of predicates and an entity.
