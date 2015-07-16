import random
import radix

def make_id(nbits):
    num = random.getrandbits(nbits)
    return radix.str(num, 62)

class Index:

    """This class generates base 64 encoded strings from a random number of bits."""

    by_name = {}

    @classmethod
    def named(cls, name):
        cls.by_name.get(name)

    def __init__(self, name, bits=32):
        self._name = name
        self._bit_count = bits
        self.__class__.by_name[name] = self

    def next(self):
        return make_id(self._bit_count)

