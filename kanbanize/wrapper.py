from json import loads
from restkit import Resource

class Kanbanize(Resource):
    """ Specialized version of restkit.Resource to deal with kanbanize.com APIs

        :param apikey: Your kanbanize.com API key
        :type apikey: str

    """

    def __init__(self, apikey, **kwargs):
        URI = 'http://kanbanize.com/index.php/api/kanbanize'
        self.apikey = apikey
        super(Kanbanize, self).__init__(URI, **kwargs)

    def request(self, method, path=None, payload=None, headers=None, **kwargs):
        headers = headers or { 'apikey': self.apikey, }
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

        Example::

            from kanbanize.wrapper import Kanbanize

            k = Kanbanize(apikey = <your api key here>)
            k.get_all_tasks(<boardid>)

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
