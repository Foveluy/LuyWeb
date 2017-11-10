
import functools
from server import LuyProtocol, serve

class Luya:
    def __init__(self):
        '''init the LuyA instance'''
        self.loop = None
        self.router = {}

    def run(self, host=None, port=None):
        serve(host, port)

    # decorator, if user decorate their function with this method,
    # it will fire when this class is INITed
    def route(self, url):
        print('register url', url)

        def response(func):
            return func(1)

        return response
