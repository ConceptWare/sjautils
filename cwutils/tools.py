from collections import defaultdict
import random
def gensym(object):
    """generate and return a symbol (att ribute name typically) unique to the object's attributes and method names"""
    trial = 'hash_%X' % random.getrandbits(16)
    while hasattr(object, trial):
        trial = 'hash_%X' % random.getrandbits(16)
    return trial

def force_unicode(x):
    return x.decode('utf-8') if isinstance(x, str) else x

identity_function = lambda x: x

def n_defaultdict(n, a_type):
    maker = lambda t: lambda: defaultdict(t)
    for _ in range(n):
        a_type = maker(a_type)
    return a_type()




def not_empty(seq):
    """returns None if sequence is empty else a generator on the sequence. Good for checking generator
    contains anything at all. Of course you would hang waiting on a generator that waits.."""
    def list_gen(first, rest):
        yield first
        for x in rest:
            yield x

    try:
        s = seq.__iter__()  #just seq for anything that is already an iterator like a generator
        first = s.next()
        return list_gen(first, s)
    except StopIteration:
        return []





def all_satisfy(func, sequence):
    """
    Returns (True, None) if all elements satisfy func else (False, element) of the first element that
    does not satisfy func
    """
    for s in sequence:
        if not func(s):
            return False, s
    return True, None

def one_satisfies(func, sequence):
    "the any builtin unfortunately does not return the element that satisfied the func"
    for s in sequence:
        if func(s):
            return True, s
    return False, None

def identity(x) : return x

def unique(sequence, hash_converter=None):
    """returns the unique elements in the sequence. Note that the raw form
    would only work if elements in the sequence are all hashable.  Passing a
    hash_converter that can map elements that are the "same" to the
    same hashable gets around this issue for many cases"""

    seen = set()
    convert = hash_converter is not None
    for s in sequence:
        hashable = hash_converter(s) if convert else s
        if not hashable in seen:
            seen.add(hashable)
            yield s
    del seen


def hexord2str(ho):
    h = [ho[i:i+2] for i in range(0, len(ho), 2)]
    ints = [int(x, 16) for x in h]
    return ''.join([chr(i) for i in ints])

def str2hexord(s):
    def hex2(n):
        res = hex(n)[2:]
        return res if len(res) == 2 else '0' + res
    return ''.join([hex2(ord(x)) for x in s])


def encrypt(key, val):
    def ith (x,i):
        return ord(x[i]) if i < len(x) else 0
    def mod_len(x,i):
        return ord(x[i % len(x)])
    l = max(len(key), len(val))
    k = [mod_len(key, i) for i in range(l)]
    v = [ith(val, i) for i in range(l)]
    tangled = [chr(k[i] ^ v[i]) for i in range(l)]
    return ''.join(tangled)

def decrypt(key, code):
    l = max(len(key), len(code))
    def mod_len(x,i):
        return ord(x[i % len(x)])
    k = [mod_len(key, i) for i in range(l)]
    c  = [ord(x) for x in code]
    ut = [chr(k[i] ^ c[i]) for i in range(l) if k[i] != c[i]]
    return ''.join(ut)

def plain2cipher(key, plain):
    return str2hexord(encrypt(key, plain))

def cipher2plain(key, cipher):
    return decrypt(key, hexord2str(cipher))

class DictObject(dict):
    def __init__(self, *args, **kwargs):
        super(DictObject, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        if name in self:
            return super(DictObject, self)[name]
        else:
            raise AttributeError('%s object has no attribute %s'% (self.__class__.__name__, name))

    def __setattr__(self, name, val):
        self[name] = val



