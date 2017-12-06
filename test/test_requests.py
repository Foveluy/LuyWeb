import sys
import pytest
sys.path.append("..")
import asyncio

from luya import Luya
from luya.blueprint import Blueprint
from luya.response import text
from luya.exception import ServerError


def test_sync():
    app = Luya('test_text')

    @app.route('/')
    def handler(request):
        return text('Hello')

    response = app.test_client.get('/')

    assert response.text == 'Hello'


def test_remote_address():
    app = Luya('test_text')

    @app.route('/')
    def handler(request):
        # print(request.ip)
        return text("{}".format(request.ip))

    response = app.test_client.get('/')

    assert response.text == '127.0.0.1'


def test_text():
    app = Luya('test_text')

    @app.route('/')
    async def handler(request):
        return text('Hello')

    response = app.test_client.get('/')

    assert response.text == 'Hello'


def test_headers():
    app = Luya('test_text')

    @app.route('/')
    async def handler(request):
        headers = {"spam": "great"}
        return text('Hello', headers=headers)

    response = app.test_client.get('/')

    assert response.headers.get('spam') == 'great'


def test_non_str_headers():
    app = Luya('test_text')

    @app.route('/')
    async def handler(request):
        headers = {"answer": 42}
        return text('Hello', headers=headers)

    response = app.test_client.get('/')

    assert response.headers.get('answer') == '42'


def test_invalid_response():
    app = Luya('test_invalid_response')

    @app.exception(ServerError)
    def handler_exception(request, exception):
        return text('Internal Server Error.', 500)

    @app.route('/')
    async def handler(request):
        return 'This should fail'

    response = app.test_client.get('/')
    assert response.status == 500
    assert response.text == "Internal Server Error."
