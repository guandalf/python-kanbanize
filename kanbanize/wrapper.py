from requests import Session
import json
import logging

class Kanbanize(Session):
    """ Specialized version of requests.Session to deal with kanbanize.com APIs

        :param subdomain: Your sudomain - https://<subdomain>.kanbanize.com 
        :type subdomain: str

        :param apikey: Your kanbanize.com API key
        :type apikey: str

    """

    def __init__(self, subdomain, apikey, **kwargs):
        self.subdomain = subdomain
        self.apikey = apikey
        super(Kanbanize, self).__init__(**kwargs)

    def request(self, method, url=None, data=None, headers=None, **kwargs):
        URI = 'https://' + self.subdomain + '.kanbanize.com/index.php/api/kanbanize'
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

            >>> from python_kanbanize import Kanbanize

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
            return ret.json()
        else:
            return ret.content

    def move_task(self, boardid, taskid, format='dict', **kwargs):
        """
        Move task on the board

        extra kwargs common used are 'column', 'lane',
        (see http://kanbanize.com/ctrl_integration for details)

        :param boardid: Board number to retrieve tasks from
        :type boardid: int
        :param taskid: TaskID of the task to be moved
        :type taskid: int
        :param format: Return format default to 'dict'
        :type format: None, 'dict', 'xml', 'json, 'csv'
        :rtype: The status of the operation (1 or error) 

        """
        details = {}
        details['boardid'] = boardid
        details['taskid'] = taskid
        details.update(kwargs)
        params = json.dumps(details)
        logging.debug('move_task:%s' % params)
        ret = self.post('/move_task/', data=params, format=format)
        if format == 'dict':
            return ret.json()
        else:
            return ret.content


    def archive_task(self, cardid, format='dict', **kwargs):
        """
        Move a card to archive
        :param cardid: CardID of the card to be moved
        :type cardid: int
        :param format: Return format default to 'dict'
        :type format: None, 'dict', 'xml', 'json, 'csv'
        :rtype: The status of the operation (1 or error) 

        """
        details = {}
        details['cardid'] = cardid
        params = json.dumps(details)
        logging.debug('archive_task:%s' % params)
        ret = self.post('/archive_task/', data=params, format=format)
        if format == 'dict':
            return ret.json()
        else:
            return ret.content

    def get_attachment(self, taskid, uniqueName, format='raw'):
        """
        Get attachment from a task
        :param taskid: TaskID of the task
        :type taskid: int
	:param uniqueName: uniqueName of the attachment
	:this parameter can be extracted with method get_task_details
	:type uniqueName: string
        :param format: Return format default to 'raw'
        :rtype: Content of the attachment 

        """
        details = {}
        details['taskid'] = taskid
        details['uniquename'] = uniqueName
        params = json.dumps(details)
        logging.debug('get_attachment:%s' % params)
        ret = self.post('/get_attachment/', data=params, format=format)
        if format == 'dict':
            return ret.json()
        else:
            return ret.content



if __name__ == "__main__":
    import doctest
    doctest.testmod()
