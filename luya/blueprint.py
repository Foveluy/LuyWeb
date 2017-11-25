class Blueprint():
    def __init__(self, name, prefix_url=None):
        self.name = name
        self.prefix_url = prefix_url
        self.associate = {}

    def route(self, url, methods=None):

        def wrapper(func):
            self.associate[self.prefix_url + url] = (func, methods)

        return wrapper

    def register(self, app):

        for k, v in self.associate.items():
            handler = v[0]
            methods = v[1]
            app.router.set_url(k, handler, methods=methods)
