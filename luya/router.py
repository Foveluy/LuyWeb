import logging
import re

from collections.abc import Iterable

REGEX_TYPES = {
    'string': (str, r'[^/]+'),
    'int': (int, r'\d+'),
    'number': (float, r'[0-9\\.]+'),
    'alpha': (str, r'[A-Za-z]+'),
    'path': (str, r'[^/].*?'),
}


PATTERN = re.compile(r'<(.+?)>')


def url_hasKey(url):
    return url.count('/')


class Router():
    def __init__(self):
        self.url = None
        self.mapping_static = {}
        self.mapping_dynamic = {}

    def set_url(self, url, func, methods=None):
        method_ary = []
        method_ary.append(('func', func))

        parameters = []

        def parse_parma(match):
            '''
            parse the parma from url
            '''
            pattern = match.group(1)
            parameters.append(pattern)
            return ''

        real_url = re.sub(PATTERN, parse_parma, url)

        if methods is not None:
            for method in methods:
                method_ary.append((method, True))
        else:
            method_ary.append(('GET', True))

        # check url if static or dynamic
        if len(parameters) > 0:
            method_ary.append(('arg', parameters))
            self.mapping_dynamic[url_hasKey(real_url)] = dict(method_ary)
        else:
            self.mapping_static[url] = dict(method_ary)

    def get_mapped_handle(self, request):
        route = self.mapping_static.get(request.url, None)
        out_put = None
        # if static route is not found

        if route is None:
            route, out_put = self._get(request)

        return route['func'], out_put

    def _get(self, request):

        # todo 没找到的情况
        route = self.mapping_dynamic[url_hasKey(request.url)]
        parameters = route.get('arg')
        
        args = request.url.split('/')
        output = []
        for i in range(0, len(parameters)):

            output.append((parameters[i], args[i + 1]))

        return route, dict(output)
