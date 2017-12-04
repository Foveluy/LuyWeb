import ujson as json
import httptools
from httptools import parse_url
import re
import urlparse

class request():

    def __init__(self, url=None, header=None, version=None, method=None):
        self.url = url
        self.header = header
        self.version = version
        self.method = method
        self.stream = None
        self.body = []
        self.HttpURL_class = None
        self.parse_URL()

    @property
    def path(self):
        return self.HttpURL_class.path.decode()

    @property
    def schema(self):
        return self.HttpURL_class.schema

    @property
    def host(self):
        return self.HttpURL_class.host

    @property
    def port(self):
        return self.HttpURL_class.port

    def args(self, name, code='utf-8'):
        regx = re.compile(r"(^|&)" + name + "=([^&]*)(&|$)")
        res = regx.match(self.HttpURL_class.query.decode(code))
        print(self.HttpURL_class.query)
        print(res)
        return res

    @property
    def fragment(self):
        return self.HttpURL_class.fragment

    @property
    def fragment(self):
        return self.HttpURL_class.userinfo

    def parse_URL(self):
        self.HttpURL_class = parse_url(self.url)

    @property
    def json(self):
        '''
            convert the request body to a json dict
        '''
        body = ''
        for chunk in self.body:
            body += chunk.decode()
        return json.loads(body)
