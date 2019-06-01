from itertools import chain, izip, cycle, count
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


def dropwhile(predicate, iterable):
    # dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
    iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            yield x
            break
    for x in iterable:
        yield x

def replace_first(curr, iter):
  """
  Returns an iterator that first yields curr then items from iter
  :param curr: item to return first
  :param iter: other items
  :return: iterator with curr first
  """

  yield curr
  for item in iter:
    yield item

def take_while(pred, iter):
    for curr in iter:
        if pred(curr):
            yield curr
        else:
            break
        
    if not pred(curr):
        return replace_first(curr, iter)
