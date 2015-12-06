from collections import defaultdict
from itertools import chain

from .tools import unique

def identity_function(x):
    return x

def partition(data, key_extractor, data_changer=identity_function):
    """partition as sequence of data clumps into a dictionary whose
    keys are the values given by applying key_extractor to each item in
    data and whose value is given by applying the data_changer to each
    item.  The data_changer defaults to the identity function"""

    partitions = defaultdict(list)
    for item in data:
        slot = key_extractor(item)
        info = data_changer(item)
        partitions[slot].append(info)

    return partitions


def binary_partition(data, item_test):
    p = partition(data, item_test)
    return p[True], p[False]


def combine_and(thunks):
    result = set()
    for thunk in thunks:
        values = set(thunk())
        if values:
            result = result.intersection(values) if result else values
            if not result:
                return []
    return result

def combine_or(thunks, make_unique=True):
    c = chain((thunk() for thunk in thunks))
    return unique(c) if make_unique else c


def always_true(x):
    return True

def tree_eval(thunk, recurse_test, arg, yield_test=None):
    seen = set()
    yield_test = identity_function if not yield_test else yield_test
    def do_node(val):
        for item in thunk(val):
            yield_it = yield_test(item)
            if yield_test(item):
                if item not in seen:
                    seen.add(item)
                    yield item
                else:
                    continue
            if recurse_test(item):
                for x in do_node(item):
                    yield x
    return do_node(arg)

def complement(fun):
    def inner(*args, **kwargs):
        return not fun(*args, **kwargs)
    inner.func_name = fun.func_name + '_complement'
    return inner

