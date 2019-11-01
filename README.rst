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

2. You start writing your entities document, this should almost never be
   directly created. It should be mostly a product of machine through a markup
   language either html or a templating language.

3. Upon launching the programme you should only write down entities. 


Already Existing Project
--------------------------


Exporting Project Data
----------------------

The suite gives you two choice for serializing your data: :code:`json` and
:code:`xml`. Once you have one of these data you can virtually recreate a
project in another environment.

