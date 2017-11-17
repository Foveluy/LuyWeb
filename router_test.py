from luya.router import Router
from luya.request import request as request_class
import unittest


class TestRouter(unittest.TestCase):

    def test_oneArg(self):

        request = request_class(url='/1234')
        router_instance = Router()
        router_instance.set_url('/<tag>', self.noop)

        handler, kw = router_instance.get_mapped_handle(request)
        self.assertEqual(kw, {'tag': '1234'})
        self.assertEqual(handler, self.noop)

    def test_multArg(self):

        request = request_class(url='/1234/12323')
        router_instance = Router()
        router_instance.set_url('/<tag>/<tag2>', self.noop)

        handler, kw = router_instance.get_mapped_handle(request)
        self.assertEqual(kw, {'tag': '1234', 'tag2': '12323'})
        self.assertEqual(handler, self.noop)

        request2 = request_class(url='/1234/12323/123')
        router_instance.set_url('/<tag>/<tag2>/<b4>', self.noop)
        handler, kw = router_instance.get_mapped_handle(request2)
        self.assertEqual(kw, {'tag': '1234', 'tag2': '12323', 'b4': '123'})
        self.assertEqual(handler, self.noop)

    def test_static_url(self):

        request = request_class(url='/1234')
        router_instance = Router()
        router_instance.set_url('/1234', self.noop)

        handler, kw = router_instance.get_mapped_handle(request)
        self.assertEqual(kw, None)
        self.assertEqual(handler, self.noop)

    def test_static_duplicate_url(self):

        request = request_class(url='/1234')
        request2 = request_class(url='/1234')
        router_instance = Router()
        router_instance.set_url('/1234', self.noop)

        with self.assertRaises(ValueError):
            router_instance.set_url('/1234', self.noop)

    def test_int_url(self):

        request = request_class(url='/123')
        
        router_instance = Router()
        router_instance.set_url('/<tag:int>', self.noop)

        handler, kw = router_instance.get_mapped_handle(request)
        self.assertEqual(kw, {'tag': 123})
        self.assertEqual(handler, self.noop)

        request2 = request_class(url='/12hh3-22')
        handler, kw = router_instance.get_mapped_handle(request2)
        self.assertEqual(kw, {})
        self.assertEqual(handler, self.noop)

    def noop(self):
        pass


if __name__ == '__main__':
    unittest.main()
