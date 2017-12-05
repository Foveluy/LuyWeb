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
