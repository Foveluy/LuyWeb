import logging
import re

from collections.abc import Iterable

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
            print(pattern)
            parameters.append(pattern)
            return ''

        real_url = re.sub(PATTERN, parse_parma, url)

        method_ary.append(('arg', parameters))

        if methods is not None:
            for method in methods:
                method_ary.append((method, True))
        else:
            method_ary.append(('GET', True))

        self.mapping_static[url_hasKey(real_url)] = dict(method_ary)

    def get_mapped_handle(self, request):
        static = self.mapping_static[url_hasKey(request.url)]

        out_put = dict(self._get(request))
        return static['func'], out_put

    def _get(self, request):

        static = self.mapping_static[url_hasKey(request.url)]
        parameters = static.get('arg')
        arg = ''
        args = []
        last = len(request.url[1:]) - 1
        for idx, char in enumerate(request.url[1:]):
            if char != '/':
                arg += char
            else:
                args.append(arg)
                arg = ''

            if idx == last:
                args.append(arg)
                arg = ''

        output = []
        for i in range(0, len(parameters)):
            
            output.append((parameters[i], args[i]))

        return output
