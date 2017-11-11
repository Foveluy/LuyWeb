

class request():

    def __init__(self, url=None, header=None, version=None, method=None):
        self.url = url
        self.header = header
        self.version = version
        self.method = method

        self.body = []
