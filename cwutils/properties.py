__author__ = 'samantha'

class reader(property):
    def __init__(self, varname):
        _reader = lambda obj: getattr(obj, varname)
        super(reader, self).__init__(_reader)

class accessor(property):
    def __init__(self, varname):
        _reader = lambda obj: getattr(obj, varname)
        def _writer(obj, value):
            setattr(obj, varname, value)
        super(accessor, self).__init__(_reader, _writer)

def abstract(fun):
    def inner(*args, **rest):
        raise Exception('Subclass must implement %s' % fun.__name__)
    inner.__name__ = fun.__name__
    return inner

