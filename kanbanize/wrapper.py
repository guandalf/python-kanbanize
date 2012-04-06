__author__ = 'Stefano Guandalini <guandalf@gmail.com'
__version__ = '0.1.2'
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
:abstract: Python interface to Request Tracker REST API
:version: %s
:author: %s
:contact: http://stefanoguandalini.it/
:date: 2012-04-06
:copyright: %s
""" % (__version__, __author__, __license__)

from json import loads
from restkit import Resource
from pprint import pprint as pp

class Kanbanize(Resource):

    def __init__(self, **kwargs):
        URI = 'http://kanbanize.com/index.php/api/kanbanize'
        super(Kanbanize, self).__init__(URI, **kwargs)

    def request(self, method, path=None, payload=None, headers=None, **kwargs):
        headers = headers or { 'apikey': 'XTJGwx9zKi1IJ3RZPXD2WfL0Vx4bJcaAZDL3qEtD', }
        format =  kwargs['format']
        if format == 'raw':
            f = ''
        elif format in ['xml', 'json', 'csv']:
            f = format
        elif format == 'dict':
            f = 'json'
        else:
            raise TypeError
        path = "%s/format/%s" % (path, f)
        return super(Kanbanize, self).request(
            method,
            path=path,
            payload=payload,
            headers=headers,
            **kwargs
        )

    def get_all_tasks(self, boardid, format='dict'):
        """
        Retireves a list of all tasks on 'boardid' board

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param format: Return format
        :type format: None, 'xml', 'json, 'csv'
        :rtype: dict or str (for explicit format request)
        :raises: TypeError if given format is != from the ones above

        """
        r = self.post('/get_all_tasks/boardid/%s' % boardid, format=format)
        if format == 'dict':
            return loads(r.body_string())
        else:
            return r.body_string()

    def get_task_details(self, boardid, taskid, format='dict'):
        """
        Retireves 'taskid' task details from 'boardid' board

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param taskid: Id of the task to retrieve details from
        :type taskid: int
        :param format: Return format
        :type format: None, 'xml', 'json, 'csv'
        :rtype: dict or str (for explicit format request)
        :raises: TypeError if given format is != from the ones above

        """
        r = self.post('/get_task_details/boardid/%s/taskid/%s' % (boardid, taskid), format=format)
        if format == 'dict':
            return loads(r.body_string())
        else:
            return r.body_string()


if __name__ == "__main__":
    k = Kanbanize()
    pp( k.get_all_tasks(5) )
    print '--------------------'
    pp( k.get_task_details(5, 27))


