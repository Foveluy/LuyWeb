from luya.router import Router
from luya.request import request as request_class
from luya import response
from luya.view import MethodView
from luya import Luya
import unittest


class TestRouter(unittest.TestCase):

    def test_one_Blueprint(self):
        
        app = Luya()
        class Mv(MethodView):
            def __init__(self):
                pass

            def get(self, request):
                return response.html('<h1>class view test</h1>')

            def post(self, request):
                return response.html('<h1>post</h1>')

        app.add_route(Mv.to_view(), '/MethodView')

        request = request_class(url='/MethodView',method='GET')
        handler, kw = app.router.get_mapped_handle(request)
        self.assertEqual(kw, {})
        self.assertEqual(handler(request).status, 200)

        request = request_class(url='/MethodView',method='POST')


    def noop(self):
        pass


if __name__ == '__main__':
    unittest.main()
