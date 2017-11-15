from luya.router import Router
from luya.request import request as request_class
import unittest


class TestRouter(unittest.TestCase):

    def test_output(self):

        request = request_class(url='/1234')
        router_instance = Router()
        router_instance.set_url('/<tag>', self.noop)

        handler, kw = router_instance.get_mapped_handle(request)
        self.assertEqual(kw, {'tag': '1234'})
        self.assertEqual(handler, self.noop)

        

    def noop(self):
        pass


if __name__ == '__main__':
    unittest.main()
