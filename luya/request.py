import ujson as json


class request():

    def __init__(self, url=None, header=None, version=None, method=None):
        self.url = url
        self.header = header
        self.version = version
        self.method = method

        self.body = []

    @property
    def json(self):
        '''
            convert the request body to a json dict
        '''
        body = ''
        for chunk in self.body:
            body += chunk.decode()
        return json.loads(body)
