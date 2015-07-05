import random

def synchronized(func):
    def _guarded(*args, **kwargs):
        lock = args[0]._instance_lock
        with lock:
            return func(*args, **kwargs)
    return _guarded




class Foo:
    whatever = read_write_var()


