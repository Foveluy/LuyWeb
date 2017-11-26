from luya.router import Router
from luya.request import request as request_class
from luya.blueprint import Blueprint
from luya.exception import LuyAException
import unittest


class TestRouter(unittest.TestCase):

    def test_one_Blueprint(self):

        request = request_class(url='/bp/1234')
        router_instance = Router()
        router_instance.set_url('/<tag>', self.noop)
        router_instance.set_url('/bp/<tag>', self.noop)

        handler, kw = router_instance.get_mapped_handle(request)
        self.assertEqual(kw, {'tag': '1234'})
        self.assertEqual(handler, self.noop)

    def test_one_Blueprint_with_type(self):
        
        request = request_class(url='/bp/1234-')
        router_instance = Router()
        router_instance.set_url('/<tag>', self.noop)
        router_instance.set_url('/bp/<tag:int>', self.noop)
        
        with self.assertRaises(LuyAException):
            router_instance.get_mapped_handle(request)
        
        request = request_class(url='/bp/1234')
        handler, kw = router_instance.get_mapped_handle(request)

        self.assertEqual(kw, {'tag': 1234})
        self.assertEqual(handler, self.noop)
    
    def test_muilt_Blueprint(self):
        
        request = request_class(url='/bp/1234-')
        router_instance = Router()
        router_instance.set_url('/<tag>', self.noop)
        router_instance.set_url('/bp/<tag:int>', self.noop)
        router_instance.set_url('/bp2/<tag:int>', self.noop)
        
        with self.assertRaises(LuyAException):
            router_instance.get_mapped_handle(request)
        
        request = request_class(url='/bp/1234')
        handler, kw = router_instance.get_mapped_handle(request)

        self.assertEqual(kw, {'tag': 1234})
        self.assertEqual(handler, self.noop)

        request = request_class(url='/bp2/1234')
        handler, kw = router_instance.get_mapped_handle(request)

        self.assertEqual(kw, {'tag': 1234})
        self.assertEqual(handler, self.noop)



    def noop(self):
        pass


if __name__ == '__main__':
    unittest.main()
