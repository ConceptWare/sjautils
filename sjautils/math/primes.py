from math import sqrt
from sjautils.iterext import satisfying, not_satisfying


class Primes:
    known_primes = [2, 3, 5, 7, 11, 13]

    @classmethod
    def until(cls, test):
        for p in cls():
            if not test(p):
                break
            yield p

    @classmethod
    def satisfying(cls, test):
        return satisfying(test, cls())
@
    @classmethod
    def filtered(cls, filter_fn):
        return not satisfying(filter_fn, cls())

    @classmethod
    def pair_tops(cls, sep=2):
        big_enough = lambda p: (p - sep) >= 3
        return cls.satisfying(lambda p: big_enough(p) and cls.filter_moduli(p, lambda x: x == sep))

    @classmethod
    def while_lt(cls, val):
        return cls.until(lambda n: n < val)

    @classmethod
    def filter_moduli(cls, n, filter_fn):
        for r in cls.moduli(n):
            if filter_fn(r):
                return False
        return True

    @classmethod
    def is_prime(cls, n, filtered=0):
        return cls.filter_moduli(n, lambda x: x == filtered)

    @classmethod
    def while_le(cls, val):
        return cls.until(lambda n: n <= val)

    @classmethod
    def moduli(cls, n):
        for p in cls.while_le(sqrt(n)):
            yield n % p

    @classmethod
    def is_pair_max(cls, n, sep=2):
        return cls.filter_moduli(n, lambda r: (r == 0) or (r == sep))

    def __init__(self):
        self._last = None
        self._test = None

    def __iter__(self):
        for p in self.known_primes:
            self._last = p
            yield p
        self._test = self._last + 2
        while True:
            if self.is_prime(self._test):
                self._last = self._test
                self.known_primes.append(self._last)
                yield self._last
            self._test += 2