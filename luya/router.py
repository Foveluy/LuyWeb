import logging
from collections.abc import Iterable


class Router():
    def __init__(self):
        self.url = None
        self.mapping_static = {}

    def set_url(self, url, func, methods=None):
        method_ary = []
        method_ary.append(('func', func))

        if methods is not None:
            for method in methods:
                method_ary.append((method, True))
        else:
            method_ary.append(('GET', True))

        self.mapping_static[url] = dict(method_ary)

    def get_mapped_handle(self, request):

        static = self.mapping_static[request.url]
        if request.method in static:
            return static['func']
        else:
            return None
