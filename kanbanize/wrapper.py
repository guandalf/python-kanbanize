from requests import Session
import json
import logging

class Kanbanize(Session):
    """ Specialized version of requests.Session to deal with kanbanize.com APIs

        :param apikey: Your kanbanize.com API key
        :type apikey: str

    """

    def __init__(self, apikey, **kwargs):
        self.apikey = apikey
        super(Kanbanize, self).__init__(**kwargs)

    def request(self, method, url=None, data=None, headers=None, **kwargs):
        URI = 'http://kanbanize.com/index.php/api/kanbanize'
        url = '%s%s' % (URI, url)
        headers = { 'apikey': self.apikey, 'content-type': 'application/json' }
        format =  kwargs['format']
        del kwargs['format']
        if format in ['xml', 'json', 'csv']:
            f = format
            url = "%s/format/%s" % (url, f)
        elif format == 'dict':
            f = 'json'
            url = "%s/format/%s" % (url, f)
        elif format == 'raw':
            pass
        else:
            raise TypeError
        logging.debug('Kanbanize.request:%s - %s - %s' % (url, data, format))

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

            >>> from python_kanbanize.wrapper import Kanbanize

            >>> k = Kanbanize(apikey)
            >>> t = k.get_all_tasks(5)
            >>> len(t)
            12
            >>> type(t)
            <type 'list'>
            >>> type(t[0])
            <type 'dict'>

        """
        r = self.post('/get_all_tasks/boardid/%s' % boardid, format=format)
        if format == 'dict':
            return r.json()
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
            return r.json()
        else:
            return r.content

    def create_new_task(self, boardid, details):
        """
        Creates a new task in 'boardid' board with optional 'details'

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param details: Task details
        :type details: dict (http://kanbanize.com/ctrl_integration for details)
        :rtype: xml

        """
        details['boardid'] = boardid
        params = json.dumps(details)
        logging.debug('create_new_task:%s' % params)
        r = self.post('/create_new_task/', data=params, format = 'raw')
        return r.content

    def edit_task(self, boardid, details):
        """
        Edit a task in 'boardid' board with provided 'details'

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param details: Task details
        :type details: dict (http://kanbanize.com/ctrl_integration for details)
        :rtype: xml

        """
        details['boardid'] = boardid
        params = json.dumps(details)
        logging.debug('edit_task:%s' % params)
        r = self.post('/edit_task/', data=params, format = 'raw')
        return r.content

    def get_board_activities(self, boardid, fromdate, todate, format='dict',
                             **kwargs):
        """
        Retrieves 'boardid' board activities

        extra kwargs common used are 'page', 'resultsperpage', 'textformat' [plain, html]
        (see http://kanbanize.com/ctrl_integration for details)

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param fromdate: From Date parameter
        :type fromdate: str (http://kanbanize.com/ctrl_integration for details)
        :param todate: To Date parameter
        :type todate: str (http://kanbanize.com/ctrl_integration for details)
        :param format: Return format default to 'dict' only tested this!
        :type format: None, 'dict', 'xml', 'json, 'csv'
        :rtype: dict or str (for explicit format request)

        """
        details = {}
        details['boardid'] = boardid
        details['fromdate'] = fromdate
        details['todate'] = todate
        details.update(kwargs)
        params = json.dumps(details)
        logging.debug('get_board_activities:%s' % params)
        ret = self.post('/get_board_activities/', data=params, format=format)
        if format == 'dict':
            return ret.json
        else:
            return ret.content


if __name__ == "__main__":
    import doctest
    doctest.testmod()
