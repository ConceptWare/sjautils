from math import prod, sqrt
from functools import reduce
from itertools import chain, combinations
from sjautils.iterext import while_satisfying, while_not_satisfying
from sjautils import iterext as itx
from collections import defaultdict
from math import prod

def possible_primes(starting_after=0):
    first_exc = [2, 3]
    mult = 1
    for low in first_exc:
        if starting_after < low:
            yield low
    mult = max((starting_after + 1) // 6, 1)
    while True:
        mult6 = mult * 6
        low, high = mult6 - 1, mult6 + 1
        if low > starting_after:
            yield low
        if high > starting_after:
            yield high
        mult += 1

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
            yield p
        for candidate in possible_primes(self.known_primes[-1]):
            if self.is_prime(candidate):
                self.add_prime(candidate, succ=True)
                yield candidate

def factor_string(factors):
    def prime_term(base, exponent):
        if exponent == 1:
            return f'{base}'
        else:
            return f'{base}^{exponent}'
        
    terms = [prime_term(k,v) for k,v in factors.items()]
    return ' * '.join(terms)

def number_from_factors(factors):
    vals = [k**v for k,v in factors.items()]
    return prod(vals)
    
def test_factors(n):
    factors = Primes.factor(n)
    the_prod = number_from_factors(factors)
    assert the_prod == n, f'{factor_string(factors)} should equal {the_sum}'


def expand_factors(factors):
    parts = [v * [k] for k,v in factors.items()]
    return reduce(lambda a,b: a + b, parts, [])

def all_divisors(num):
    factors = expand_factors(Primes.factor(num))
    prods = chain.from_iterable(combinations(factors, r) for r in range(len(factors)+1))
    return {prod(p) for p in prods} - {1}
    

def has_ndigit_product(n, num):
    has_n_digits = lambda d: lambda _n: (10**(d - 1)) <= _n < 10**d
    is_n_digits = has_n_digits(n)
    for div in all_divisors(num):
        if is_n_digits(div) and is_n_digits(num // div):
            return True
    return False


def common_factors(*factors):
    sets = [set(f.keys()) for f in factors]
    return reduce(lambda a,b: a & b, sets[1:], sets[0])

def factor_exponents(factor_keys, *factors):
    return {k: [f[k] for f in factors] for k in factor_keys}


def combine_factors(combine_fn, *factors, only_common=False):
    if only_common:
        keys = common_factors(*factors)
    else:
        keys = reduce(lambda a,b: a | set(b.keys()), factors, set())

    exponents = factor_exponents(keys, *factors)

    return {k: combine_fn(v) for k,v in exponents.items()}

def gcd(n1, n2):
    factors = combine_factors(min, Primes.factor(n1), Primes.factor(n2), only_common=True)
    factors = {k:v for k,v in factors.items() if v > 0}
    if not factors:
        return 1
    return number_from_factors(factors)


def lcm(*nums):
    pfs = [Primes.factor(n) for n in nums]
    factors = combine_factors(max, *pfs)
    return number_from_factors(factors)

