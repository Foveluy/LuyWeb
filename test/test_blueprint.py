import sys
import pytest
sys.path.append("..")
import asyncio

from luya import Luya
from luya.blueprint import Blueprint
from luya.response import text


def test_basic_blueprint():
    '''
        To test basic blueprint.
    '''
    app = Luya('test_basic_blueprint')
    bp = Blueprint('test_basic_blueprint')

    @bp.route('/')
    def handler(request):
        return text('Hello')

    app.register_blueprint(bp)
    rsp = app.test_client.get('/')
    assert app.has_stream == False

    assert rsp.text == 'Hello'
    # print(res)


def test_fix_slash():
    pass


def test_url_prefix():
    app = Luya('test_url_prefix')
    bp = Blueprint('test_url_prefix', prefix_url='/bp')

    @bp.route('/')
    def handler(request):
        return text('Hello')

    app.register_blueprint(bp)
    rsp = app.test_client.get('/bp/')
    assert rsp.text == 'Hello'


def test_url_with_multipe_bp_prefix():
    app = Luya('test_url_prefix')
    bp = Blueprint('test_url_prefix', prefix_url='/bp1')
    bp2 = Blueprint('test_url_prefix', prefix_url='/bp2')

    @bp.route('/')
    def handler(request):
        return text('Hello1')

    @bp2.route('/')
    def handler(request):
        return text('Hello2')

    app.register_blueprint(bp)
    app.register_blueprint(bp2)

    rsp1 = app.test_client.get('/bp1/')
    assert rsp1.text == 'Hello1'

    rsp2 = app.test_client.get('/bp2/')
    assert rsp2.text == 'Hello2'
