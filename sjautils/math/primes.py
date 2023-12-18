from math import sqrt
from sjautils.iterext import while_satisfying, while_not_satisfying
from sjautils import iterext as itx
from collections import defaultdict
from math import prod

class Primes:
    known_primes = [2, 3, 5, 7, 11, 13]
    prime_set = set(known_primes)

    @classmethod
    def add_prime(cls, p, succ=False):
        if succ:
            cls.known_primes.append(p)
        cls.prime_set.add(p)

    @classmethod
    def satisfying(cls, test):
        return while_satisfying(test, cls())

    @classmethod
    def filtered(cls, filter_fn):
        return itx.not_satisfying(filter_fn, cls())

    @classmethod
    def pair_tops(cls, sep=2):
        big_enough = lambda p: (p - sep) >= 3
        return cls.satisfying(lambda p: big_enough(p) and cls.filter_moduli(p, lambda x: x == sep))

    @classmethod
    def while_lt(cls, val):
        return cls.satisfying(lambda n: n < val)

    @classmethod
    def filter_moduli(cls, n, filter_fn):
        for r in cls.moduli(n):
            if filter_fn(r):
                return False
        return True

    @classmethod
    def is_prime(cls, n, filtered=0):
        if n in cls.prime_set:
            return True
        mod6 = n % 6
        if mod6 == 1 or mod6 == 5:
                
            return cls.filter_moduli(n, lambda x: x == filtered)
        else:
            return False

    
    @classmethod
    def while_le(cls, val):
        return cls.satisfying(lambda n: n <= val)

    @classmethod
    def moduli(cls, n):
        return (n%p for p in cls.while_le(sqrt(n)))

    @classmethod
    def factor(cls, n):
        # TODO fix me to return defaultdict(int) and use better
        # algorithm
        

        factors = defaultdict(int)
        working = [n]

        low_factors = list(cls.while_le(sqrt(n)))
    
        #print(n, factors, low_factors)

        def compute_exp(p):
            while not working[0] % p:
                factors[p] += 1
                working[0] //= p
            #print('factors added', p, factors[p])
            
            
        for p in low_factors:
            #print('checking', p, n, working)
            if working[0] == 1:
                break
            if not working[0] % p:
                compute_exp(p)

        if working[0] != 1:
            factors[working[0]] = 1

        return factors
            
                

                
                

    
        
        


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
                self.add_prime(self._last, succ=True)
                yield self._last
            self._test += 2

def factor_string(factors):
    def prime_term(base, exponent):
        if exponent == 1:
            return f'{base}'
        else:
            return f'{base}^{exponent}'
        
    terms = [prime_term(k,v) for k,v in factors.items()]
    return ' * '.join(terms)
    
def test_factors(n):
    factors = Primes.factor(n)
    vals = [k**v for k,v in factors.items()]
    the_prod = prod(vals)
    assert the_prod == n, f'{factor_string(factors)} should equal {the_sum}'

    
