import sys
import pytest
sys.path.append("..")
import asyncio

from luya import Luya
from luya.blueprint import Blueprint
from luya.response import text
from luya.view import MethodView
from luya.exception import LuyAException

from luya.constant import HTTP_METHODS


@pytest.mark.parametrize('method', ('GET', 'POST'))
def test_methods(method):
    app = Luya('test_methods')

    class DummyView(MethodView):

        async def get(self, request):
            print('进来了')
            assert request.stream is None

            return text('', headers={'method': 'GET'})

        def post(self, request):
            return text('', headers={'method': 'POST'})

        async def put(self, request):
            return text('', headers={'method': 'PUT'})

        def head(self, request):
            return text('', headers={'method': 'HEAD'})

        def options(self, request):
            return text('', headers={'method': 'OPTIONS'})

        async def patch(self, request):
            return text('', headers={'method': 'PATCH'})

        def delete(self, request):
            return text('', headers={'method': 'DELETE'})

    app.add_route(DummyView.to_view(), '/')
    assert app.has_stream is False

    response = getattr(app.test_client, method.lower())('/')
    assert response.headers['method'] == method


def test_unexisting_methods():
    app = Luya('test_unexisting_methods')

    class DummyView(MethodView):

        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.to_view(), '/')
    response = app.test_client.get('/')
    assert response.text == 'I am get method'
    response = app.test_client.post('/')
    assert response.text == '<h3>/ is not allow POST<h3>'


def test_argument_methods():
    app = Luya('test_argument_methods')

    class DummyView(MethodView):

        def get(self, request, my_param_here):
            return text('I am get method with %s' % my_param_here)

    app.add_route(DummyView.to_view(), '/<my_param_here>')

    response = app.test_client.get('/test123')

    assert response.text == 'I am get method with test123'


def test_with_bp():
    app = Luya('test_with_bp')
    bp = Blueprint('test_text')

    class DummyView(MethodView):

        def get(self, request):
            assert request.stream is None
            return text('I am get method')

    bp.add_route(DummyView.to_view(), '/')

    app.register_blueprint(bp)
    response = app.test_client.get('/')

    assert app.has_stream is False
    assert response.text == 'I am get method'


def test_with_bp_with_url_prefix():
    app = Luya('test_with_bp_with_url_prefix')
    bp = Blueprint('test_text', prefix_url='/test1')

    class DummyView(MethodView):

        def get(self, request):
            return text('I am get method')

    bp.add_route(DummyView.to_view(), '/')

    app.register_blueprint(bp)
    response = app.test_client.get('/test1/')

    assert response.text == 'I am get method'


# def test_with_middleware():
#     app = Luya('test_with_middleware')

#     class DummyView(MethodView):

#         def get(self, request):
#             return text('I am get method')

#     app.add_route(DummyView.to_view(), '/')

#     results = []

#     @app.middleware
#     async def handler(request):
#         results.append(request)

#     request, response = app.test_client.get('/')

#     assert response.text == 'I am get method'
#     assert type(results[0]) is Request

def test_with_custom_class_methods():
    app = Luya('test_with_custom_class_methods')

    class DummyView(MethodView):
        global_var = 0

        def _iternal_method(self):
            self.global_var += 10

        def get(self, request):
            self._iternal_method()
            return text('I am get method and global var is {}'.format(self.global_var))

    app.add_route(DummyView.to_view(), '/')
    response = app.test_client.get('/')
    assert response.text == 'I am get method and global var is 10'


# def test_with_decorator():
#     app = Luya('test_with_decorator')

#     results = []

#     def stupid_decorator(view):
#         def decorator(*args, **kwargs):
#             results.append(1)
#             return view(*args, **kwargs)
#         return decorator

#     class DummyView(MethodView):
#         decorators = [stupid_decorator]

#         def get(self, request):
#             return text('I am get method')

#     app.add_route(DummyView.to_view(), '/')
#     response = app.test_client.get('/')
#     assert response.text == 'I am get method'
