from luya.constant import HTTP_METHODS


class Blueprint():
    def __init__(self, name, prefix_url=None):
        self.name = name
        self.prefix_url = prefix_url or ''
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

    def add_route(self, handler_or_class, url, methods=['GET']):
        is_class = hasattr(handler_or_class, 'view_class')
        http_methods = methods
        if is_class:
            for http_method in HTTP_METHODS:
                handler = getattr(handler_or_class.view_class,
                                  http_method.lower(), None)
                if handler:
                    http_methods.append(http_method)

        self.route(url, methods=http_methods)(handler_or_class)
