from luya.strtime import gmtime
try:
    from ujson import dumps as json_dumps
except:
    from json import dumps as json_dumps


COMMON_STATUS_CODES = {
    200: b'OK',
    400: b'Bad Request',
    404: b'Not Found',
    500: b'Internal Server Error',
}
ALL_STATUS_CODES = {
    100: b'Continue',
    101: b'Switching Protocols',
    102: b'Processing',
    200: b'OK',
    201: b'Created',
    202: b'Accepted',
    203: b'Non-Authoritative Information',
    204: b'No Content',
    205: b'Reset Content',
    206: b'Partial Content',
    207: b'Multi-Status',
    208: b'Already Reported',
    226: b'IM Used',
    300: b'Multiple Choices',
    301: b'Moved Permanently',
    302: b'Found',
    303: b'See Other',
    304: b'Not Modified',
    305: b'Use Proxy',
    307: b'Temporary Redirect',
    308: b'Permanent Redirect',
    400: b'Bad Request',
    401: b'Unauthorized',
    402: b'Payment Required',
    403: b'Forbidden',
    404: b'Not Found',
    405: b'Method Not Allowed',
    406: b'Not Acceptable',
    407: b'Proxy Authentication Required',
    408: b'Request Timeout',
    409: b'Conflict',
    410: b'Gone',
    411: b'Length Required',
    412: b'Precondition Failed',
    413: b'Request Entity Too Large',
    414: b'Request-URI Too Long',
    415: b'Unsupported Media Type',
    416: b'Requested Range Not Satisfiable',
    417: b'Expectation Failed',
    422: b'Unprocessable Entity',
    423: b'Locked',
    424: b'Failed Dependency',
    426: b'Upgrade Required',
    428: b'Precondition Required',
    429: b'Too Many Requests',
    431: b'Request Header Fields Too Large',
    500: b'Internal Server Error',
    501: b'Not Implemented',
    502: b'Bad Gateway',
    503: b'Service Unavailable',
    504: b'Gateway Timeout',
    505: b'HTTP Version Not Supported',
    506: b'Variant Also Negotiates',
    507: b'Insufficient Storage',
    508: b'Loop Detected',
    510: b'Not Extended',
    511: b'Network Authentication Required'
}


class BaseResponse():
    def parse_header(self):
           # header should be a dict
        parsed_header = b''
        for key, value in self.header.items():
            try:
                parsed_header += (b'%b:%b\r\n'
                                  % (key.encode(), value.encode()))
            # sometimes,key & value may not to be a string
            except AttributeError as e:
                parsed_header += (b'%b:%b\r\n'
                                  % (str(key).encode(), str(value).encode()))
        return parsed_header


class HTTPResponse(BaseResponse):
    __slots__ = ('body', 'status', 'content_type', 'header', '_cookies')

    def __init__(self, status=200, body=None,
                 content_type='text/plain', header=None):
        '''
        :parma content_type:https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
        '''
        self.status = status
        self.body = body
        self.content_type = content_type
        self.header = header or {}

    def drain(self, version=b'1.1', keep_alive=False, keep_alive_timeout=None):
        '''
        flush a response to whatever you wanted
        '''

        timeout_header = b''
        if keep_alive and keep_alive_timeout is not None:
            timeout_header = b'Keep-Alive: %d\r\n' % keep_alive_timeout
        self.header['Content-Length'] = len(self.body.encode())
        self.header['Content-Type'] = self.content_type
        # it looks very tricky that it will slow down the server
        # self.header['Date'] = gmtime()

        header = self.parse_header()
        statusText = COMMON_STATUS_CODES.get(self.status, None)
        if statusText is None:
            statusText = ALL_STATUS_CODES.get(self.status, b'UNKNOWN RESPONSE')

        return (b'HTTP/%b %d %b\r\n'
                b'Connection: %b\r\n'
                b'%b'
                b'%b\r\n'
                b'%b') % (
                    version, self.status, statusText,
                    b'keep-alive'if keep_alive else b'close',
                    timeout_header,
                    header,
                    self.body.encode())


class HTTPStreamingResponse(BaseResponse):
    def __init__(self, streaming_fn, status=200, header=None,
                 content_type='text/plain'):
        self.content_type = content_type
        self.streaming_fn = streaming_fn
        self.status = status
        self.header = header or {}
        self._cookies = None

    def compute_header(self, version=b'1.1', keep_alive=False, keep_alive_timeout=None):

        timeout_header = b''
        if keep_alive and keep_alive_timeout is not None:
            timeout_header = b'Keep-Alive: %d\r\n' % keep_alive_timeout

        self.header['Transfer-Encoding'] = 'chunked'
        self.header.pop('Content-Length', None)
        self.header['Content-Type'] = self.header.get(
            'Content-Type', self.content_type)

        headers = self.parse_header()
        statusText = COMMON_STATUS_CODES[self.status]
        if statusText is None:
            statusText = ALL_STATUS_CODES.get(self.status, b'UNKNOWN RESPONSE')

        return (b'HTTP/%b %d %b\r\n'
                b'%b'
                b'%b\r\n') % (version, self.status, statusText,
                              timeout_header,
                              headers)

    def write(self, chunked):
        '''
            it will call transport.write() function.
            This method does not block; it buffers the data and arranges for it to be sent out asynchronously.

            transport.write() : https://docs.python.org/3/library/asyncio-protocol.html
        '''

        if type(chunked) != bytes:
            chunked = chunked.encode()

        # dynamicly adding a transport from server
        self.transport.write(
            b"%x\r\n%b\r\n" % (len(chunked), chunked))

    async def stream_output(self, version=b"1.1", keep_alive=False, keep_alive_timeout=None):
        '''
            a coroutine function,awating stream_fn until it gets a None
        '''
        headers = self.compute_header(
            version, keep_alive=keep_alive,
            keep_alive_timeout=keep_alive_timeout)

        # dynamicly adding a transport from server
        self.transport.write(headers)
        await self.streaming_fn(self)


def stream(
        streaming_fn, status=200, header=None,
        content_type="text/plain; charset=utf-8"):
    '''
    this method will return a HTTPStreamingResponse class 
    for stream response

    return stream(sample_streaming_fn, content_type='text/csv')

    :parma streaming_fn: coroutine function
    '''

    return HTTPStreamingResponse(
        streaming_fn,
        header=header,
        content_type=content_type,
        status=status
    )


def json(body, status=200, header=None, content_type="application/json", **kwargs):
    '''
    ujson is way more faster than json module, 
    highly recommended the user to install it

    :parma body: a dict to be convert 

    :parma status: http code

    :parma header: header is none if user do not specify

    :parma **kwargs: user can use a key-value form : json(key=value,key2=value2)
    '''

    return HTTPResponse(body=json_dumps(body, **kwargs),
                        content_type=content_type,
                        status=status,
                        header=header)


def text(body, status=200, header=None, content_type="text/plain:charset=utf-8"):
    return HTTPResponse(body=body,
                        content_type=content_type,
                        status=status,
                        header=header)


def html(body, status=200, header=None):
    return HTTPResponse(body=body,
                        content_type="text/html; charset=utf-8",
                        status=status,
                        header=header)
