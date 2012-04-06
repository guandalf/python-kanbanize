================================
Kanbanize.com Python API Wrapper
================================

To install just::
  easy_istall python-kanbanize

Getting started::
  from kanbanize.wrapper import Kanbanize

  k = Kanbanize(<your api key here>)
  k.get_all_tasks(<boardid>)

The wrapper will reproduce all the methods available at:

http://kanbanize.com/ctrl_integration