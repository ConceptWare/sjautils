from math import prod, sqrt
from functools import reduce
from itertools import chain, combinations
from sjautils.iterext import while_satisfying, while_not_satisfying, all_satisfy
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

    def add_prime(cls, p, succ=False):
        if succ:
            cls.known_primes.append(p)
        cls.prime_set.add(p)

    def possible_factors(self, num):
        return self.le(num)

    def moduli(self, num):
        return (num%p for p in self.possible_factors)

  
    def is_prime(self, n):
        if n in self.prime_set:
            return True
        mod6 = n % 6
        if mod6 == 1 or mod6 == 5:
            return all_satisfy(lambda x: x != 0, self.moduli(n))   
        else:
            return False

    def iterator(self):
        for p in self.known_primes:
            yield p
        for candidate in possible_primes(self.known_primes[-1]):
            if self.is_prime(candidate):
                self.add_prime(candidate, succ=True)
                yield candidate

    def le(self, val):
        for p in self.iterator():
            if p <= val:
                yield p
            else:
                break

primes = Primes()

def factor(num):
    return primes.factor(num)

def moduli(num):
    return primes.moduli(num)

def is_prime_pair_upper(num, sep=2):
    return primes.is_prime(num) and all_satisfy(lambda x: x != sep, moduli(num))


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
    factors = factor(n)
    the_prod = number_from_factors(factors)
    assert the_prod == n, f'{factor_string(factors)} should equal {the_prod}'


def expand_factors(factors):
    parts = [v * [k] for k,v in factors.items()]
    return reduce(lambda a,b: a + b, parts, [])

def all_divisors(num):
    factors = expand_factors(factor(num))
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

