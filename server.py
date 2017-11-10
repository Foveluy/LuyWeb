import asyncio
from httptools import HttpRequestParser, HttpParserError
import functools
import uvloop
import asyncio

class request():

    def __init__(self, url=None, header=None, version=None, method=None):
        self.url = url
        self.header = header
        self.version = version
        self.method = method

        self.body = []


class LuyProtocol(asyncio.Protocol):
    def __init__(self, loop=None):
        self.parser = None
        self.header = {}
        self.url = None
        #print('init:', placeholder)

    def connection_made(self, transport):
        self.transport = transport
        if self.parser is None:
            self.parser = HttpRequestParser(self)

    def connection_lost(self, exc):
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
        print(self.header)
        self.request = request(
            url=self.url,
            header=self.header,
            version=self.parser.get_http_version(),
            method=self.parser.get_method()
        )
        #print('\n', self.parser.get_method())

    def on_body(self, body):
        self.request.body.append(body)

    def on_message_complete(self):
        # print('on_message_complete')
        print(self.request.body)
        self.transport.write(b'''HTTP/1.1 200 OK

'{'fuck':'shit'}'

''')
        self.transport.close()

    #------------------------------------------------------------------------
    #                       error handling
    #------------------------------------------------------------------------
    def write_error(self):
        self.transport.write(b'''HTTP/1.1 200 OK

'{'fuck':'shit'}'

''')


def serve(host=None, port=None):
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(False)


    LuyaServer = functools.partial(
        LuyProtocol,
        loop=loop
    )

    host, port = host or "127.0.0.1", port or 8000
    server_setting = (host , port)

    try:
        coroutine = loop.create_server(LuyaServer, *server_setting)
    except Exception as e:
        print('unable to run the server',e)
        return

    print('Server listening at', *server_setting)

    #run the 
    luya_httpServer = loop.run_until_complete(coroutine)
    loop.run_forever()

    #wait for all connection drain and then close
    luya_httpServer.close()
    loop.run_until_complete(luya_httpServer.wait_closed())

    loop.close()
