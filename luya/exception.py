
def add_status_code(code):
    def add(cls):
        cls.status_code = code
        return cls

    return add



class LuyAException(Exception):

    def __init__(self, message, status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code



@add_status_code(404)
class NOT_FOUND(LuyAException):
    pass
