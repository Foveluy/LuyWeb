import asyncio
from httptools import HttpRequestParser, HttpParserError


class LuyProtocol(asyncio.Protocol):
    def __init__(self, placeholder, loop=None):
        self.parser = None
        self.header = {}
        self.url = None
        print('init:', placeholder)

    def connection_made(self, transport):
        self.transport = transport
        if self.parser is None:
            self.parser = HttpRequestParser(self)

    def connection_lost(self, exc):
        self.transport = None

    def data_received(self, data):
        # print('recv:收到data',data)
        try:
            self.parser.feed_data(data)
        except HttpParserError as e:
            print('出错', e)
        finally:
            print('进入回调')

    #------------------------------------------------------------------------

    #                       httptools callback

    #------------------------------------------------------------------------
    def on_message_begin(self):
        print('on_message_begin')

    def on_url(self, url):
        if not self.url:
            self.url = url
        else:
            self.url += url
        print(url)

    def on_header(self, name, value):
        self.header[name] = value

    def on_headers_complete(self):
        print('on_headers_complete:\n')
        print(self.header)
        print('\n', self.parser.get_method())

    def on_body(self, body):
        print('parsebody中....')
        print(body)
        print('parse 完毕')

    def on_message_complete(self):
        print('on_message_complete')
        self.transport.write(b'{"b":"fuck"}')
