from requests import Session

class Kanbanize(Session):
    """ Specialized version of restkit.Resource to deal with kanbanize.com APIs

        :param apikey: Your kanbanize.com API key
        :type apikey: str

    """

    def __init__(self, apikey, **kwargs):
        self.apikey = apikey
        super(Kanbanize, self).__init__(**kwargs)

    def request(self, method, url=None, data=None, headers=None, **kwargs):
        URI = 'http://kanbanize.com/index.php/api/kanbanize'
        url = '%s%s' % (URI, url)
        headers = { 'apikey': self.apikey, }
        format =  kwargs['format']
        del kwargs['format']
        if format == 'raw':
            f = ''
        elif format in ['xml', 'json', 'csv']:
            f = format
        elif format == 'dict':
            f = 'json'
        else:
            raise TypeError
        url = "%s/format/%s" % (url, f)
        return super(Kanbanize, self).request(
            method,
            url=url,
            data=data,
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

        Example::

            >>> from kanbanize.wrapper import Kanbanize
            >>> from credentials import *

            >>> k = Kanbanize(apikey)
            >>> k.get_all_tasks(5)
            [{u'columnname': u'backlog', u'blockedreason': None, u'lanename': u'Default Swimlane', u'subtaskdetails': [], u'subtasks': None, u'title': u'Task title', u'color': u'#F0F0F0', u'tags': u'', u'priority': u'Average', u'assignee': u'None', u'deadline': None, u'taskid': u'38', u'subtaskscomplete': None, u'extlink': u'', u'blocked': None, u'type': u'0', u'leadtime': 1, u'size': u'2'}, {u'columnname': u'Backlog', u'blockedreason': None, u'lanename': u'Default Swimlane', u'subtaskdetails': [], u'subtasks': u'0', u'title': u'Kanbanize test task 01', u'color': u'#99b399', u'tags': None, u'priority': u'Average', u'assignee': u'None', u'deadline': None, u'taskid': u'27', u'subtaskscomplete': u'0', u'extlink': None, u'blocked': u'0', u'type': u'0', u'leadtime': 15, u'size': u'2'}, {u'columnname': u'Backlog', u'blockedreason': None, u'lanename': u'Default Swimlane', u'subtaskdetails': [], u'subtasks': u'0', u'title': u'Kanbanize test task 02', u'color': u'#99b399', u'tags': None, u'priority': u'Average', u'assignee': u'None', u'deadline': None, u'taskid': u'28', u'subtaskscomplete': u'0', u'extlink': None, u'blocked': u'0', u'type': u'0', u'leadtime': 15, u'size': u'2'}]

        """
        r = self.post('/get_all_tasks/boardid/%s' % boardid, format=format)
        if format == 'dict':
            return r.json
        else:
            return r.content

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
            return r.json
        else:
            return r.content

    def create_new_task(self, boardid, details={}):
        """
        Creates a new task in 'boardid' board with optional 'details'

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param details: Task details
        :type details: dict (http://kanbanize.com/ctrl_integration for details)
        :rtype: int

        """

        p = []
        for k, v in details.iteritems():
            p.append(k)
            p.append(v)

        params = '/'.join(p)
        r = self.post('/create_new_task/boardid/%s/%s' % (boardid, params), format = 'raw')
        return r.content

if __name__ == "__main__":
    import doctest
    doctest.testmod()