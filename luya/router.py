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
            if ':' in pattern:
                splited = pattern.split(':')
                pattern = splited[0]
                Type = splited[1]
                parameters.append((pattern, Type))
            else:
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
            self.map_static(url, dict(method_ary))

    def map_static(self, url, method_ary):
        if url in self.mapping_static:
            raise ValueError('request <{}> is exisit'.format(url))

        self.mapping_static[url] = method_ary

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
            if isinstance(parameters[i], tuple):
                parma = parameters[i][0]
                Type = parameters[i][1]
                regex = REGEX_TYPES.get(Type, None)

                # regular type
                if regex is not None:
                    matching = re.compile(regex[1]).match(args[i + 1])
                    if args[i + 1] == matching.group():
                        output.append((parma, regex[0](args[i + 1])))
                    else:
                        #not found 404
                        pass
                else:
                    # todo not regular one
                    pass
            else:
                # if no type define ,goes here
                output.append((parameters[i], args[i + 1]))

        return route, dict(output)