import ujson as json
import httptools
from httptools import parse_url
import re
from urllib.parse import parse_qs, urlunparse
from luya.exception import LuyAException
import logging


class request(dict):

    def __init__(self, url_bytes=None, header=None, version=None, method=None):
        self.url = url_bytes
        self.header = header
        self.version = version
        self.method = method
        self.stream = None
        self.body = []
        self.parsed_args = None
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

    @property
    def args(self):
        if self.parsed_args is None:
            if self.HttpURL_class.query:
                self.parsed_args = parse_qs(self.HttpURL_class.query.decode())
        print(self.parsed_args)
        return self.parsed_args

    @property
    def ip(self):
        return self.header['host'].split(':')[0]

    @property
    def fragment(self):
        return self.HttpURL_class.fragment

    @property
    def userinfo(self):
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
        if body == '':
            return None

        try:
            return json.loads(body)
        except Exception as e:
            logging.error('json parse err ,{}'.format(e))
            raise LuyAException('Bad Request', status_code=400)
