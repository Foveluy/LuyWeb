import random
import sys
import pytest
sys.path.append("..")

from luya import Luya
from luya.response import json

try:
    from ujson import loads
except ImportError:
    from json import loads


def test_storage():
    app = Luya('test_text')

    @app.middleware('request')
    def store(request):
        request['user'] = 'luya'
        request['sidekick'] = 'tails'
        del request['sidekick']

    @app.route('/')
    def handler(request):

        return json({'user': request.get('user'), 'sidekick': request.get('sidekick')})

    response = app.test_client.get('/')

    response_json = loads(response.text)
    assert response_json['user'] == 'luya'
    assert response_json.get('sidekick') is None
