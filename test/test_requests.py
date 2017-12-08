import sys
import pytest
sys.path.append("..")
import asyncio
from ujson import loads as json_loads
from ujson import dumps as json_dumps

from luya import Luya
from luya.blueprint import Blueprint
from luya.response import text, json
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


def test_json():
    app = Luya('test_json')

    @app.route('/')
    async def handler(request):
        return json({"test": True})

    response = app.test_client.get('/')

    results = json_loads(response.text)

    assert results.get('test') == True


def test_empty_json():
    app = Luya('test_json')

    @app.route('/')
    async def handler(request):
        assert request.json == None
        return json(request.json)

    response = app.test_client.get('/')
    assert response.status == 200
    assert response.text == 'null'


def test_invalid_json():
    app = Luya('test_json')

    @app.route('/', methods=['POST'])
    async def handler(request):
        return json(request.json)

    data = "I am not json"
    response = app.test_client.post('/', data=data)

    assert response.status == 400


def test_query_string():
    app = Luya('test_query_string')
    args = [None]

    @app.route('/')
    async def handler(request):
        args[0] = request.args
        return text('OK')

    response = app.test_client.get('/?test1=1&test2=2&test3=false')
    arg = args[0]
    assert arg['test1'][0] == '1'
    assert arg['test2'][0] == '2'
    assert arg['test3'][0] == 'false'


def test_match_info():
    app = Luya('test_match_info')
    arg = [None]

    @app.route('/api/v1/user/<user_id>/')
    async def handler(request, user_id):
        arg[0] = user_id
        return text('OK')

    response = app.test_client.get('/api/v1/user/sanic_user/')
    assert arg[0] == 'sanic_user'


def test_post_json():
    app = Luya('test_post_json')
    arg = [None]

    @app.route('/', methods=['POST'])
    async def handler(request):
        arg[0] = request
        return text('OK')

    payload = {'test': 'OK'}
    headers = {'content-type': 'application/json'}

    response = app.test_client.post(
        '/', data=json_dumps(payload), headers=headers)

    assert arg[0].json.get('test') == 'OK'
    assert response.text == 'OK'


# def test_post_form_urlencoded():
#     app = Luya('test_post_form_urlencoded')
#     arg = [None]

#     @app.route('/', methods=['POST'])
#     async def handler(request):
#         arg[0] = request
#         return text('OK')

#     payload = 'test=OK'
#     headers = {'content-type': 'application/x-www-form-urlencoded'}

#     response = app.test_client.post(
#         '/', data=payload, headers=headers)

#     assert arg[0].form.get('test') == 'OK'
