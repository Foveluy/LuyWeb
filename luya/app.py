
import functools
from inspect import isawaitable, stack, getmodulename
from traceback import format_exc
import logging

from luya.server import LuyProtocol, serve
from luya.response import html as response_html
from luya.response import HTTPResponse
from luya.router import Router
from luya.exception import LuyAException


class Luya:
    def __init__(self):
        '''init the LuyA instance'''

        self.loop = None
        self.router = Router()
        self.blueprint_name_bundle = {}
        self.blueprint_in_order = []
        self.request_middleware = []
        self.response_middleware = []
        self.exception_handler = {}

    def run(self, host=None, port=None):
        serve(
            self,
            host=host,
            port=port
        )

    def register_blueprint(self, blueprint):
        '''
        register a blueprint
        '''

        if blueprint.name in self.blueprint_name_bundle:
            raise KeyError(
                'the name {} for blueprint has already registered, please choose another name instead')
        else:
            self.blueprint_in_order.append(blueprint)
            blueprint.register(self)

    def register_middleware(self, middleware, before=None):
        if before == 'request':
            self.request_middleware.append(middleware)
        if before == 'response':
            self.response_middleware.append(middleware)

        # decorator
    def middleware(self, middleware_or_string):
        ''' a decorator for registing middleware,which will be invoked
            before request or after request in order.
            example:
            default @app.middleware is for registing 'request'
            middleware_or_string = 'request', it will fire before request
            middleware_or_string = 'response', it will fire before response

            if middleware return a response object, it will response directly
            without calling any other method
        '''

        # if the way is @app.middleware
        if callable(middleware_or_string):
            return self.register_middleware(middleware_or_string, before='request')
        else:
            return functools.partial(
                self.register_middleware,
                before=middleware_or_string)

            # decorator
    def exception(self, exception):

        def decorator(func):
            status_code = exception.status_code
            self.exception_handler[status_code] = func

        return decorator

        # decorator
    def route(self, url, methods=None):
        '''
        if user decorate their function with this method,
        it will fire when a method is being decorated
        '''
        def response(func):
            # todo to using dict directly is not good for reading
            # has to encapsulate into a class
            self.router.set_url(url, func, methods)

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
        #----------------
        # handling request middleware
        #----------------
        try:
            for middleware in self.request_middleware:
                response = middleware(request)

                if isinstance(response, HTTPResponse):
                    if isawaitable(response):
                        response = await response
                    write_callback(response)
                    return
        except Exception as e:
            response = response_html(
                '''<h3>unable to perform the request middleware and router function</h3>
                    <p>{}</p>
                    <p>{}</p>
                '''.format(e, format_exc()), status=500)

        #----------------
        # handling request
        #----------------

        try:
            handler, kw = self.router.get_mapped_handle(request)

            # users may define a non-awaitable function
            response = handler(request, **kw)
            if isawaitable(response):
                response = await response
            else:
                logging.warning('url %s for %s is not isawaitable' %
                                (request.url, handler))
        except LuyAException as e:
            try:
                handler = self.exception_handler.get(e.status_code, None)

                response = handler(request, exception=e)
                if isawaitable(response):
                    response = await response
                
                #setting a status code for return
                if response.status == 200:
                    response.status = e.status_code
                else:
                    logging.warning('url %s for %s is not isawaitable' %
                                    (request.url, handler))
            except Exception as err:
                response = response_html(
                    '<h1>{}</h1>{}'.format(e, format_exc()), status=500)

        except Exception as e:
            response = response_html(
                '''<h3>unable to perform the request middleware and router function</h3>
                    <p>{}</p>
                    <p>{}</p>
                '''.format(e, format_exc()), status=500)

        finally:
            #----------------
            # handling response middleware
            #----------------
            try:
                response = await self.run_response_middleware(request,response)
            except Exception as e:
                response = response_html(
                    '''<h3>unable to perform the request middleware and router function</h3>
                        <p>{}</p>
                        <p>{}</p>
                    '''.format(e, format_exc()), status=500)

        # todo stream call_back
        try:
            write_callback(response)
        except Exception as e:
            print('write_callback fail', e)

    async def run_response_middleware(self, request, response):
        for middleware in self.response_middleware:
            _response = middleware(request, response)

            if isinstance(_response, HTTPResponse):
                if isawaitable(_response):
                    _response = await _response
                if _response:
                    response = _response
                break

        return response
