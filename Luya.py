
import functools
from server import LuyProtocol, serve
from inspect import isawaitable, stack, getmodulename


class Luya:
    def __init__(self):
        '''init the LuyA instance'''

        self.loop = None
        self.router = {}

    def run(self, host=None, port=None):
        serve(
            self,
            host=host,
            port=port
        )

    # decorator, if user decorate their function with this method,
    # it will fire when this class is INITed
    def route(self, url):
        print('registing :', url)

        def response(func):
            # todo to using dict directly is not good for reading
            # has to encapsulate into a class
            self.router[url] = func

        return response

    async def request_handler(self, request, write_callback, stream_callback):
        '''
        this method will fire when the request has been parsed,
        the user has to make sure every single function is a coroutine
        function and super fast.

        this is a coroutine function

        :param write_callback: the callback for writing response back
        :param stream_callback: for stream request,normally it is a download request
        '''
        try:
            handler = self.router[request.url]

            # users may define a non-awaitable function
            response = handler(request)
            if isawaitable(response):
                response = await response
            else:
                print('warnning:url %s for %s is not isawaitable' %
                      (request.url, handler))
        except Exception as e:
            print('unable to perform the request middleware and router function', e)
            response = 'unable to perform the request middleware and router function '
        finally:
            pass

        # todo stream call_back
        write_callback(response)
