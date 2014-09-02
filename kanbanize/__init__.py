__author__ = 'Stefano Guandalini <guandalf@gmail.com>'
__version__ = '0.3.0'
__classifiers__ = [
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
]
__copyright__ = "2011, %s " % __author__
__license__ = """
   Copyright (C) %s

      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or
      (at your option) any later version.

      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
      along with this program.  If not, see <http://www.gnu.org/licenses/>.
""" % __copyright__

__docformat__ = 'restructuredtext en'

__doc__ = """
:abstract: Python interface to kanbanize.com API
:version: %s
:author: %s
:contact: http://about.me/guandalf
:date: 2014-0828
:copyright: %s
""" % (__version__, __author__, __license__)

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .wrapper import *