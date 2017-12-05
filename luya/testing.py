
import functools
from inspect import isawaitable, stack, getmodulename
from traceback import format_exc
import logging

from luya.server import LuyProtocol, serve, multiple_serve, _print_logo
from luya.response import html as response_html
from luya.response import HTTPResponse, HTTPStreamingResponse
from luya.router import Router
from luya.exception import LuyAException
import aiohttp
from json import JSONDecodeError

PORT = 23333


class LuyA_Test():
    def __init__(self, app):
        self.app = app

    async def _request(self, url='/', method='get', headers=None):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            async with getattr(
                    session, method.lower())('http://127.0.0.1:{}'.format(PORT) + url, headers=headers) as response:
                try:
                    response.text = await response.text()
                except UnicodeDecodeError as e:
                    response.text = None

                try:
                    response.json = await response.json()
                except (JSONDecodeError,
                        UnicodeDecodeError,
                        aiohttp.ClientResponseError):
                    response.json = None

                response.body = await response.read()
                return response

    def _run_test_server(self, url='/', method='get', headers=None):

        rsp = [None]

        async def request():
            rsp[0] = await self._request(url=url, method=method, headers=headers)

            self.app.stop()
        self.app.listener('after_start')(request)

        self.app.run(port=PORT)
        return rsp[0]

    def get(self, url='/', headers=None):
        return self._run_test_server(url=url, method='get', headers=headers)
