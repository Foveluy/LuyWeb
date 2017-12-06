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


def test_dynamic_route_int():
    app = Luya('test_dynamic_route_int')

    results = []

    @app.route('/folder/<folder_id:int>')
    async def handler(request, folder_id):
        results.append(folder_id)
        return text('OK')

    response = app.test_client.get('/folder/12345')
    assert response.text == 'OK'
    assert type(results[0]) is int

    response = app.test_client.get('/folder/asdf')
    assert response.status == 404


def test_dynamic_route_number():
    app = Luya('test_dynamic_route_number')

    results = []

    @app.route('/weight/<weight:number>')
    async def handler(request, weight):
        results.append(weight)
        return text('OK')

    response = app.test_client.get('/weight/12345')
    assert response.text == 'OK'
    assert type(results[0]) is float

    response = app.test_client.get('/weight/1234.56')
    assert response.status == 200

    response = app.test_client.get('/weight/1234-56')
    assert response.status == 404


def test_route_duplicate():
    app = Luya('test_route_duplicate')

    with pytest.raises(ValueError):
        @app.route('/test')
        async def handler1(request):
            pass

        @app.route('/test')
        async def handler2(request):
            pass

    with pytest.raises(ValueError):
        @app.route('/test/<dynamic>/')
        async def handler1(request, dynamic):
            pass

        @app.route('/test/<dynamic>/')
        async def handler2(request, dynamic):
            pass


def test_method_not_allowed():
    app = Luya('test_method_not_allowed')

    @app.route('/test', methods=['GET'])
    async def handler(request):
        return text('OK')

    response = app.test_client.get('/test')
    assert response.status == 200

    response = app.test_client.post('/test')
    assert response.status == 405


def test_static_add_route():
    app = Luya('test_static_add_route')

    async def handler1(request):
        return text('OK1')

    async def handler2(request):
        return text('OK2')

    app.add_route(handler1, '/test')
    app.add_route(handler2, '/test2')

    response = app.test_client.get('/test')
    assert response.text == 'OK1'

    response = app.test_client.get('/test2')
    assert response.text == 'OK2'


def test_dynamic_add_route():
    app = Luya('test_dynamic_add_route')

    results = []

    async def handler(request, name):
        results.append(name)
        return text('OK')

    app.add_route(handler, '/folder/<name>')
    response = app.test_client.get('/folder/test123')

    assert response.text == 'OK'
    assert results[0] == 'test123'


def test_dynamic_add_route_string():
    app = Luya('test_dynamic_add_route_string')

    results = []

    async def handler(request, name):
        results.append(name)
        return text('OK')

    app.add_route(handler, '/folder/<name:string>')
    response = app.test_client.get('/folder/test123')

    assert response.text == 'OK'
    assert results[0] == 'test123'

    response = app.test_client.get('/folder/favicon.ico')

    assert response.text == 'OK'
    assert results[1] == 'favicon.ico'


def test_dynamic_add_route_int():
    app = Luya('test_dynamic_add_route_int')

    results = []

    async def handler(request, folder_id):
        results.append(folder_id)
        return text('OK')

    app.add_route(handler, '/folder/<folder_id:int>')

    response = app.test_client.get('/folder/12345')
    assert response.text == 'OK'
    assert type(results[0]) is int

    response = app.test_client.get('/folder/asdf')
    assert response.status == 404


def test_dynamic_add_route_number():
    app = Luya('test_dynamic_add_route_number')

    results = []

    async def handler(request, weight):
        results.append(weight)
        return text('OK')

    app.add_route(handler, '/weight/<weight:number>')

    response = app.test_client.get('/weight/12345')
    assert response.text == 'OK'
    assert type(results[0]) is float

    response = app.test_client.get('/weight/1234.56')
    assert response.status == 200

    response = app.test_client.get('/weight/1234-56')
    assert response.status == 404


def test_add_route_duplicate():
    app = Luya('test_add_route_duplicate')

    with pytest.raises(ValueError):
        async def handler1(request):
            pass

        async def handler2(request):
            pass

        app.add_route(handler1, '/test')
        app.add_route(handler2, '/test')

    with pytest.raises(ValueError):
        async def handler1(request, dynamic):
            pass

        async def handler2(request, dynamic):
            pass

        app.add_route(handler1, '/test/<dynamic>/')
        app.add_route(handler2, '/test/<dynamic>/')


def test_add_route_method_not_allowed():
    app = Luya('test_add_route_method_not_allowed')

    async def handler(request):
        return text('OK')

    app.add_route(handler, '/test', methods=['GET'])

    response = app.test_client.get('/test')
    assert response.status == 200

    response = app.test_client.post('/test')
    assert response.status == 405


# def test_remove_static_route():
#     app = Luya('test_remove_static_route')

#     async def handler1(request):
#         return text('OK1')

#     async def handler2(request):
#         return text('OK2')

#     app.add_route(handler1, '/test')
#     app.add_route(handler2, '/test2')

#     response = app.test_client.get('/test')
#     assert response.status == 200

#     response = app.test_client.get('/test2')
#     assert response.status == 200

#     app.remove_route('/test')
#     app.remove_route('/test2')

#     response = app.test_client.get('/test')
#     assert response.status == 404

#     response = app.test_client.get('/test2')
#     assert response.status == 404

# def test_overload_routes():
#     app = Luya('test_dynamic_route')

#     @app.route('/overload', methods=['GET'])
#     async def handler1(request):
#         return text('OK1')

#     @app.route('/overload', methods=['POST', 'PUT'])
#     async def handler2(request):
#         return text('OK2')

#     response = app.test_client.get('/overload')
#     assert response.text == 'OK1'

#     response = app.test_client.post('/overload')
#     assert response.text == 'OK2'

#     response = app.test_client.put('/overload')
#     assert response.text == 'OK2'

#     response = app.test_client.delete('/overload')
#     assert response.status == 405

#     with pytest.raises(ValueError):
#         @app.route('/overload', methods=['PUT', 'DELETE'])
#         async def handler3(request):
#             return text('Duplicated')
