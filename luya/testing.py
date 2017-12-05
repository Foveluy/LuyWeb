
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

    def _run_test_server(self, url='/', headers=None):
        self.app.run(port=PORT)

    async def get(self, url='/', method='get', headers=None):
        async with aiohttp.ClientSession() as session:
            async with getattr(
                    session, method.lower())('127.0.0.1' + url, headers=headers) as response:
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
                self.app.stop()
                return response
