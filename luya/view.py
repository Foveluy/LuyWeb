class MethodView():

    def dispatch(self, request, *arg, **kwarg):
        handler = getattr(self, request.method.lower(), None)

        if handler:
            return handler(request, *arg, **kwarg)

    @classmethod
    def to_view(cls, *cls_arg, **cls_kwarg):
        '''
        create a instance for the view class and dispatch the url
        correctly.
        '''

        def handler(*arg, **kwarg):
            '''
            handler is this function
            '''
            _ins = cls(*cls_arg, **cls_kwarg)
            return _ins.dispatch(*arg, **kwarg)

        handler.view_class = cls
        handler.__doc__ = cls.__doc__
        handler.__module__ = cls.__module__
        handler.__name__ = cls.__name__

        return handler
