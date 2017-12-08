import sys
import pytest
sys.path.append("..")
import asyncio

from luya import Luya
from luya.blueprint import Blueprint
from luya.response import text, HTTPResponse
from luya.request import request
from luya.exception import NOT_FOUND

def test_middleware_request():
    app = Luya('test_middleware_request')

    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    @app.route('/')
    async def handler(request):
        return text('OK')

    response = app.test_client.get('/')

    assert response.text == 'OK'
    assert type(results[0]) is request


def test_middleware_response():
    app = Luya('test_middleware_response')

    results = []

    @app.middleware('request')
    async def process_response(request):
        results.append(request)

    @app.middleware('response')
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    @app.route('/')
    async def handler(request):
        return text('OK')

    response = app.test_client.get('/')

    assert response.text == 'OK'
    assert type(results[0]) is request
    assert type(results[1]) is request
    assert isinstance(results[2], HTTPResponse)

def test_middleware_response_exception():
    app = Luya('test_middleware_response_exception')
    result = {'status_code': None}

    @app.middleware('response')
    async def process_response(request, response):
        result['status_code'] = response.status
        return response

    @app.exception(NOT_FOUND)
    async def error_handler(request, exception):
        return text('OK', exception.status_code)

    @app.route('/')
    async def handler(request):
        return text('FAIL')

    response = app.test_client.get('/page_not_found')
    assert response.text == 'OK'
    assert result['status_code'] == 404

def test_middleware_override_request():
    app = Luya('test_middleware_override_request')

    @app.middleware
    async def halt_request(request):
        return text('OK')

    @app.route('/')
    async def handler(request):
        return text('FAIL')

    response = app.test_client.get('/')

    assert response.status == 200
    assert response.text == 'OK'

def test_middleware_override_response():
    app = Luya('test_middleware_override_response')

    @app.middleware('response')
    async def process_response(request, response):
        return text('OK')

    @app.route('/')
    async def handler(request):
        return text('FAIL')

    response = app.test_client.get('/')

    assert response.status == 200
    assert response.text == 'OK'