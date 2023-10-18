from itertools import chain, cycle, count, takewhile, dropwhile, islice
import asyncio
from functools import wraps

take = lambda n, iter: (iter.next() for _ in range(n))


class take_only_while(object):
  def __init__(self,pred, iterator):
    self._pred = pred
    self._iter = iterator
    self._rest = iter([])

  def __iter__(self):
    return self

  def next(self):
    item = self._iter.next()
    if self._pred(item):
      return item
    else:
      self._rest = chain([item], self._iter)
      raise StopIteration

  def __next__(self):
      return self.next()
  
  @property
  def the_rest(self):
    return self._rest


def drop_while(predicate, iterable):
    return dropwhile(predicate, iterable)

def take_n(n, iterable):
    return islice(iterable, n)

def replace_first(curr, iterable):
  """
  Returns an iterator that first yields curr then items from iter
  :param curr: item to return first
  :param iterable: other items
  :return: iterator with curr first
  """

  yield curr
  for item in iterable:
    yield item

def take_while(pred, iterable):
    return takewhile(pred, iterable)

def while_satisfying(pred, iterable):
    return takewhile(pred, iterable)

def satisfying(pred, iterable):
    return (p for p in iterable if pred(p))

def not_pred(pred):
    return lambda x: not pred(x)

def not_satisfying(pred, iterable):
    return satisfying(not_pred(pred), iterable)


def while_not_satisfying(pred, iterable):
    return while_satisfying(not_pred(pred), iterable)

def test_take_while():
    data = [1] + list(range(2, 12, 2))
    test_odd = lambda x: x % 2
    test_even = lambda x: not (x % 2)
    res_even = list(take_while(test_even, (x for x in data)))
    print(res_even)
    assert res_even == data
    res_odd = list(take_while(test_odd, (x for x in data)))
    assert not res_odd

