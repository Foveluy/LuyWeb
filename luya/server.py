import asyncio
from httptools import HttpRequestParser, HttpParserError
import functools
import uvloop

from luya.request import request as request_class
from luya.response import HTTPResponse


class LuyProtocol(asyncio.Protocol):
    def __init__(self, app, loop=None, keep_alive=True):
        self.parser = None
        self.url = None
        self._request_handler_task = None
        self.loop = loop

        self.header = {}
        self.app = app
        self.keep_alive = keep_alive

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
        if value is not None:
            if name == b'Content-Length' and int(value) > 1500:
                self.write_error()

            self.header[name.decode().casefold()] = value.decode()

    def on_headers_complete(self):
        self.request = request_class(
            url=self.url.decode(),
            header=self.header,
            version=self.parser.get_http_version(),
            method=self.parser.get_method().decode()
        )

    def on_body(self, body):
        self.request.body.append(body)

    def on_message_complete(self):
        # print('on_message_complete')
        self._request_handler_task = self.loop.create_task(
            self.app.request_handler(
                self.request,
                self.write_response,
                None))

    #---------------------------
    #      error handling
    #---------------------------
    def write_error(self):
        self.transport.write(b'''HTTP/1.1 200 OK

'{'fuck':'shit'}'

''')
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

    def refresh(self):
        '''
        refresh the server state
        prepare for next incoming request
        '''
        self.url = None
        self.header = {}


def serve(app, host=None, port=None):
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
        loop=loop
    )

    host, port = host or "127.0.0.1", port or 8000
    server_setting = (host, port)

    try:
        coroutine = loop.create_server(LuyaServer, *server_setting)
    except Exception as e:
        print('unable to run the server', e)
        return

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
    print('Luya listening at', *server_setting)

    # run the the server
    luya_httpServer = loop.run_until_complete(coroutine)
    loop.run_forever()

    # wait for all connection drain and then close
    luya_httpServer.close()
    loop.run_until_complete(luya_httpServer.wait_closed())

    loop.close()
