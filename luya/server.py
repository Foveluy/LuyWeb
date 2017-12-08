import asyncio
from httptools import HttpRequestParser, HttpParserError
from luya.response import html
import functools
import uvloop
import logging
import sys
import os
from inspect import isawaitable

from traceback import format_exc
from multiprocessing import Process

from luya.request import request as request_class
from luya.response import HTTPResponse


from socket import (
    socket,
    SOL_SOCKET,
    SO_REUSEADDR,
)


class LuyProtocol(asyncio.Protocol):
    def __init__(self, app, loop=None, keep_alive=True, request_max_size=None, has_stream=False, debug=True):
        self.parser = None
        self.url = None
        self._request_handler_task = None
        self._request_stream_task = None
        self.request_max_size = request_max_size
        self._total_request_size = 0
        self.loop = loop
        self.header = {}
        self.app = app
        self.keep_alive = keep_alive
        self.has_stream = has_stream
        self.stream_handler = None

    def connection_made(self, transport):
        self.transport = transport
        if self.parser is None:
            self.parser = HttpRequestParser(self)

    def connection_lost(self, exc):

        self.transport.close()
        self.refresh()
        self.transport = None

    #-------------------------------------
    #               parsing
    #-------------------------------------
    def data_received(self, data):
        '''
        reveiving data from network.
        it is a streaming.
        has to check the data size for pretecting memory limits.
        '''
        if self.request_max_size:
            self._total_request_size += len(data)
            if self._total_request_size > self.request_max_size:
                # todo:payload too large,have to implement a method represent PAYLOAD TOO LARGE
                self.write_error()

        try:
            self.parser.feed_data(data)
        except HttpParserError as e:
            print('出错', e)
        finally:
            pass

    def on_message_begin(self):
        # print('on_message_begin')
        pass

    def on_url(self, url):
        # storing the url from web
        if not self.url:
            self.url = url
        else:
            self.url += url

    def on_header(self, name, value):
        '''
        Content-Length cannot be too long,
        protect the server
        '''
        if value is not None:
            if name == b'Content-Length' and int(value) > 1500:
                self.write_error()
            self.header[name.decode().casefold()] = value.decode()

    def on_headers_complete(self):
        self.request = request_class(
            url_bytes=self.url,
            header=self.header,
            version=self.parser.get_http_version(),
            method=self.parser.get_method().decode()
        )

        # here is where we deal with "Expect: 100-Continue"
        # when user upload some big file or big things
        # their client would send a header with 'Expect: 100-Continue'
        # to if check the server can be accepted.
        if self.has_stream:
            self.stream_handler, kw = self.app.router.get_mapped_handle(
                self.request)
            if self.stream_handler and kw['stream']:
                # here is a coroutine queue
                # when await get()
                self.request.stream = asyncio.Queue()
                self.execute_request_handler()

    def on_body(self, body):
        if self.has_stream and self.stream_handler:
            self.loop.create_task(self.request.stream.put(body))
            return

        self.request.body.append(body)

    def on_message_complete(self):

        # None is the signal for task to stop
        if self.has_stream and self.stream_handler:
            self.loop.create_task(self.request.stream.put(None))
            return

        self.execute_request_handler()

    def execute_request_handler(self):
        self._request_handler_task = self.loop.create_task(
            self.app.request_handler(
                self.request,
                self.write_response,
                self.stream_callback))

    #---------------------------
    #      error handling
    #---------------------------
    def write_error(self):
        response = html('bad connecton', status=400)
        self.write_response(response)
        self.transport.close()

    #-------------------------------------
    #            write response
    #-------------------------------------

    def write_response(self, response):
        '''
        the writing phase is very fast
        so may not have to use coroutine
        '''
        try:
            keep_alive = self.keep_alive
            self.transport.write(response.drain(keep_alive=keep_alive))
            if keep_alive:
                self.refresh()
            else:
                self.transport.close()
        except AttributeError as e:
            print('AttributeError????', e)
            self.transport.close()
        except RuntimeError as e:
            print('RuntimeError????', e)
            self.transport.close()
        except Exception as e:
            print('Exception????', e)
            self.transport.close()

    async def stream_callback(self, response):
        '''

        '''
        try:
            keep_alive = self.keep_alive
            response.transport = self.transport
            await response.stream_output(self.request.version, keep_alive)
            if keep_alive:
                self.refresh()
            else:
                self.transport.close()

        except AttributeError as e:
            print('AttributeError????', e)
            self.transport.close()
        except RuntimeError as e:
            print('RuntimeError????', e)
            self.transport.close()
        except Exception as e:
            print('Exception????', e)
            self.transport.close()

    def refresh(self):
        '''
        refresh the server state
        prepare for next incoming request
        '''
        self.url = None
        self.header = {}
        self._request_handler_task = None
        self.stream_handler = None


def serve(app, host=None, port=None, sock=None, workers=1, has_stream=False, debug=True):
    '''
    start a server with host & port

    :parma app: Luya app,it is for protocol class use
    :parma host: host ip ,example : 0.0.0.0
    :parma port: hosting port (1-65536)
    '''

    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(False)

    LuyaServer = functools.partial(
        LuyProtocol,
        app=app,
        loop=loop,
        has_stream=has_stream,
        debug=debug
    )

    try:
        coroutine = loop.create_server(
            LuyaServer,
            host=host,
            port=port,
            sock=sock,
            reuse_address=True,
            reuse_port=True)

        if debug:
            _print_workers(host, port, '[pid:{}]'.format(os.getpid()))

    except Exception as e:
        logging.error('unable to run the server,{}'.format(format_exc()))
        return

    # run the the server
    luya_httpServer = loop.run_until_complete(coroutine)

    try:
        run_listener(app.after_server_start, app, loop)
    except Exception as e:
        return
        logging.error('unable to run the server,{}'.format(format_exc()))

    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print('server closing, wait for all connection drain and then close')
        # wait for all connection drain and then close
        luya_httpServer.close()
        loop.run_until_complete(luya_httpServer.wait_closed())
    finally:
        loop.close()
        print('server closed', ', [pid:{}]'.format(os.getpid()))


def multiple_serve(app, server_args):
    processes = []
    host = server_args['host']
    port = server_args['port']

    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.set_inheritable(True)
    server_args['sock'] = sock
    server_args['host'] = None
    server_args['port'] = None

    serves = functools.partial(
        serve,
        app,
        **server_args
    )

    try:
        for i in range(0, server_args['workers']):
            process = Process(target=serves, kwargs=server_args)
            process.daemon = True
            process.start()
            processes.append(process)
            _print_workers(host, port, '[pid:{}]'.format(process.pid))

        # wait for every process complete
        for process in processes:
            process.join()
    except KeyboardInterrupt as e:
        for process in processes:
            print('process pid:[{}] is terminated', process.pid)
            process.terminate()
    finally:
        sock.close()


def run_listener(listeners, app, loop):
    '''
        trigger the listener
    '''
    for listener in listeners:
        func = listener(app, loop)
        if isawaitable(func):
            loop.run_until_complete(func)


def stop():
    asyncio.get_event_loop().close()


def _print_logo():
    '''unuseful method dont call it!!!!!!!!!!'''
    print('''
                        ██╗     ██╗   ██╗██╗   ██╗ █████╗ 
                        ██║     ██║   ██║╚██╗ ██╔╝██╔══██╗
                        ██║     ██║   ██║ ╚████╔╝ ███████║
                        ██║     ██║   ██║  ╚██╔╝  ██╔══██║
                        ███████╗╚██████╔╝   ██║   ██║  ██║
                        ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
            ╔═╗┌─┐┬ ┬┌─┐┬─┐┌─┐┌┬┐  ┌┐ ┬ ┬  ╔═╗┬ ┬┌─┐┌┐┌┌─┐╔═╗┌─┐┌┐┌┌─┐
            ╠═╝│ ││││├┤ ├┬┘├┤  ││  ├┴┐└┬┘  ╔═╝├─┤├┤ ││││ ┬╠╣ ├─┤││││ ┬
            ╩  └─┘└┴┘└─┘┴└─└─┘─┴┘  └─┘ ┴   ╚═╝┴ ┴└─┘┘└┘└─┘╚  ┴ ┴┘└┘└─┘
    ''')


def _print_workers(*setting):
    print('Luya process listening at ', *setting)
