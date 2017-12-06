import sys
import pytest
sys.path.append("..")
import asyncio

from luya import Luya
from luya.blueprint import Blueprint
from luya.response import text


def test_route_get():
    app = Luya('test_route_get')

    @app.route('/get')
    def handler(request):
        return text('OK')

    response = app.test_client.get('/get')
    assert response.text == 'OK'

    response2 = app.test_client.post('/get')
    assert response2.status == 405


def test_route_invalid_parameter_syntax():
    with pytest.raises(ValueError):
        app = Luya('test_route_invalid_param_syntax')

        @app.route('/get/<:string>')
        def handler(request):
            return text('OK')


def test_route_post():
    app = Luya('test_route_get')

    @app.route('/post', methods=['POST'])
    def handler(request):
        return text('OK')

    response = app.test_client.get('/post')
    assert response.status == 405

    response2 = app.test_client.post('/post')
    assert response2.text == 'OK'


def test_static_routes():
    app = Luya('test_static_routes')

    @app.route('/test')
    async def handler1(request):
        return text('OK1')

    @app.route('/pizazz')
    async def handler2(request):
        return text('OK2')

    response = app.test_client.get('/test')
    assert response.text == 'OK1'

    response = app.test_client.get('/pizazz')
    assert response.text == 'OK2'


def test_dynamic_route():
    app = Luya('test_dynamic_route')

    results = []

    @app.route('/folder/<name>')
    async def handler(request, name):
        results.append(name)
        return text('OK')

    response = app.test_client.get('/folder/test123')

    assert response.text == 'OK'
    assert results[0] == 'test123'


def test_dynamic_route_string():
    app = Luya('test_dynamic_route_string')

    results = []

    @app.route('/folder/<name:string>')
    async def handler(request, name):
        results.append(name)
        return text('OK')

    response = app.test_client.get('/folder/test123')

    assert response.text == 'OK'
    assert results[0] == 'test123'

    response = app.test_client.get('/folder/favicon.ico')
    assert response.text == 'OK'
    assert results[1] == 'favicon.ico'
