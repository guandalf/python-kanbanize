================================
Kanbanize.com Python API Wrapper
================================

Installation
============

To install just::

    $ easy_istall python-kanbanize

Usage
=====
Getting started::

    from kanbanize.wrapper import Kanbanize

    k = Kanbanize(<your api key here>)
    k.get_all_tasks(<boardid>)

Note
====

The wrapper will reproduce all the methods available at:

http://kanbanize.com/ctrl_integration