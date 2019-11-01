######################
digital-edition-suite
######################

.. image:: https://travis-ci.com/D-K-E/digital-edition-suite.svg?branch=master
    :target: https://travis-ci.com/D-K-E/digital-edition-suite

Small scripts to publish digital editions using authority files easier.
This is intended as small collection of scripts that are not necessarily scalable, 
but that help to produce machine oriented data during edition projects.

It binds the modification of authority files and related structures to a workflow,
which in turn should significantly cut back schema related errors.

It is not done yet

Use cases
==========

New Project
------------

Let's say you want to start a project from scratch. How should you proceed ?
Here are the steps:

1. You define a relations file, and associate function representation (binary
   or string) with each relation.

2. You start to write your document in html or in some templating language.
   

3. Label your entities. For easy generation of authority documents label unit
   entities first. Then generate a simple authority file from them. This would
   come in handy afterwards.

4. Before going on further, you should create all the authority files
   necessary for creating a predicate document. Once all of those are created,
   you can start creating predicates that are going to be associated with
   entities.

5. For each entity there must be a unique predicate for a given relation. At
   this point you should see whether there are any entities that can not be
   associated with any of predicates.

6. Link predicate inside a predicate document with an entity.

7. Use either the corresponding command line or graphical interface for
   handling all the document types mentioned above.

Already Existing Project
--------------------------


Exporting Project Data
----------------------

The suite gives you two choice for serializing your data: :code:`json` and
:code:`xml`. Once you have one of these data you can virtually recreate a
project in another environment.

