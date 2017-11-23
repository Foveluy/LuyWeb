import logging
import re

from luya.exception import LuyAException
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
        self.mapping_partial = {}
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

            # get the position of parmaeters
            splited = url.split('/')
            idx = 0
            for index, value in enumerate(splited):
                if value == match.group():
                    idx = index

            if ':' in pattern:
                splited = pattern.split(':')
                pattern = splited[0]
                Type = splited[1]
                parameters.append((pattern, Type, idx))
            else:
                parameters.append({'pattern': pattern, 'index': idx})

            return ''

        real_url = re.sub(PATTERN, parse_parma, url)

        static_part_splited = real_url.split('/')

        for value in static_part_splited:
            if value != '':
                self.mapping_partial[value] = True

        if methods is not None:
            for method in methods:
                method_ary.append((method, True))
        else:
            method_ary.append(('GET', True))

        # check url if static or dynamic
        if len(parameters) > 0:
            method_ary.append(('arg', parameters))
            self.map_dynamic(url_hasKey(real_url), dict(method_ary))
        else:
            self.map_static(url, dict(method_ary))

    def map_dynamic(self, key, method_ary):
        if key not in self.mapping_dynamic:
            self.mapping_dynamic[key] = []

        self.mapping_dynamic[key].append(method_ary)

    def map_static(self, url, method_ary):
        if url in self.mapping_static:
            raise ValueError('request <{}> is exisit'.format(url))
        self.mapping_static[url] = method_ary

    def get_mapped_handle(self, request):
        '''
            get a handler from url
            :parma request: the request of one connection
        '''
        route = self.mapping_static.get(request.url, None)
        
        kwarg = {}
        # if static route is not found
        if route is None:
            route, kwarg = self._get(request)

        return route['func'], kwarg

    def _get(self, request):
        '''
            this function is for parsing a dynamic url.
            notice that using dynamic url is very slow.
            we are not highly recommand to use a lot of dynamic urls in your project.

            :parma request: the request of one connection
        '''

        # todo 没找到的情况
        route = self.mapping_dynamic.get(url_hasKey(request.url), None)
        if route is None:
            raise LuyAException('Page Not Fount 404', 404)

        args = request.url.split('/')

        for _route in route:
            parameters = _route.get('arg')
            output = []

            # check how many args
            for i in range(0, len(parameters)):

                if isinstance(parameters[i], tuple):
                    parma = parameters[i][0]
                    Type = parameters[i][1]
                    idx = parameters[i][2]
                    regex = REGEX_TYPES.get(Type, None)

                    # regular type
                    if regex is not None:
                        matching, index = self.check_matching(
                            re.compile(regex[1]), args, idx)
                        if matching is None:
                            continue

                        if args[index] == matching.group():
                            output.append((parma, regex[0](args[index])))
                        else:
                            # not found 404
                            raise LuyAException('Page Not Fount 404', 404)
                    else:
                        # todo not regular one
                        raise LuyAException('Internal Error', 500)
                else:
                    # if no type define, goes here
                    pattern = parameters[i].get('pattern')
                    index = parameters[i].get('index')
                    output.append((pattern, args[index]))

            # check if found
            if len(output) > 0:
                return _route, dict(output)

        raise LuyAException('Page Not Fount 404', 404)

    def check_matching(self, regex, args, idx):
        '''
        for checking the every single part of the url

        example /bp/<key:type> checking the static 'bp'

        :parma regex: it is a regex object 
        :parma args: array, splited from url
        :parma idx: index of this dynamic argument,
                    example  /bp/<key:type> ,its index is 1. couting from 0.

        '''
        for index, value in enumerate(args):
            if value in self.mapping_partial:
                continue

            if idx == index:
                match = regex.match(value)
                if match is not None:
                    return match, index
        raise LuyAException('Page Not Fount 404', 404)
