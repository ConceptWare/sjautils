from collections import defaultdict
import random, re
import validators
import subprocess as sub
from functools import reduce

def as_list(fn, *args, **kwargs):
  'because python3 made way two many things generators effectively'
  return list(fn(*args, **kwargs))

def lmap(fn, *iterables):
  return as_list(map, fn, *iterables)

def dict_keys(a_dict):
  '''
  Since 3.x was stupid enough to make dict.keys() return something not indexable
  :param a_dict: the dict to get keys for
  :return: return keys as a list
  '''
  return list(a_dict.keys())

def dict_values(a_dict):
  '''
  Since 3.x was stupid enough to make dict.values() return something not indexable
  :param a_dict: the dict to get keys for
  :return: return keys as a list
  '''
  return list(a_dict.values())

def is_url(string):
  if not './/' in string:
    string = 'https://' + string
    trial = validators.url(string)
    if not isinstance(trial,validators.ValidationFailure):
      return string
    return False

def set_and(fn, values):
  res = set()
  for v in values:
    res_v = fn(v)
    if not res:
      res.update(res_v)
    else:
      res = res & res_v
    if not res:
      break
  return res

def set_or(fn, values):
  return reduce(lambda a, b: a | b, map(fn, values))


def match_fields(pat, aString, *fields):
  match = re.search(pat, aString)
  data = match.groupdict() if match else None
  return [data.get(f, None) for f in fields] if data else [None for _ in fields]

def sub_pipes(*pipes):
    return {p: sub.PIPE for p in pipes}
standard_pipes = sub_pipes('stdin', 'stdout', 'stderr')

def command_output(command):
    get_output = lambda stuff: [l.strip() for l in stuff.split('\n')]
    p = sub.Popen(command, shell=True, **standard_pipes)
    out, err = p.communicate()
    return get_output(out) or get_output(err)

def writable_files_in(path):
    data = command_output('ls -lR %s' % path)
    switch_path = False
    res = []
    for d in data:
        ds = d.split()
        if not d:
            switch_path = True
            continue
        if switch_path:
            path = ds[0]
            switch_path=False
            continue
        if d.startswith('total'):
            continue
        base = ds[-1]
        #print 'base:', base
        res.append(os.path.join(path, ds[-1]))
    return res


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


def tree_order(hierarchy, sequence, h_extractor=identity_function, s_extractor=identity_function):
  """
  A generator returning items of sequence in the order they appear traversing the
  hierarchy (depth-first pre-order).
  """
  data = dict([(s_extractor(x), x) for x in sequence])
  for value in hierarchy.pre_order(h_extractor):
    if value in data:
      yield data[value]


def not_empty(seq):
  """returns None if sequence is empty else a generator on the sequence. Good for checking generator
  contains anything at all. Of course you would hang waiting on a generator that waits.."""

  def list_gen(first, rest):
    yield first
    for x in rest:
      yield x


def pruning_tree_collect(root, children_function, test_function, result_function=None):
  """returns the nodes closest to the root nodes of the tree that satisfy the test_function.
      The value returned for a satisfying node is determined by the result_function which
          defaults to the node itself."""
  if result_function is None: result_function = identity_function
  results = []

  def do_node(node):
    # print 'evaluating node %s' % node
    if test_function(node):
      # print 'node %s satisfied test' % node
      results.append(result_function(node))
    else:
      # print 'node %s did not satisfy test so examining children %s' % (node, children_function(node))
      for child in children_function(node):
        do_node(child)

  do_node(root)
  return results


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


def identity(x): return x




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
  h = [ho[i:i + 2] for i in range(0, len(ho), 2)]
  ints = [int(x, 16) for x in h]
  return ''.join([chr(i) for i in ints])


def str2hexord(s):
  def hex2(n):
    res = hex(n)[2:]
    return res if len(res) == 2 else '0' + res

  return ''.join([hex2(ord(x)) for x in s])


def encrypt(key, val):
  def ith(x, i):
    return ord(x[i]) if i < len(x) else 0

  def mod_len(x, i):
    return ord(x[i % len(x)])

  l = max(len(key), len(val))
  k = [mod_len(key, i) for i in range(l)]
  v = [ith(val, i) for i in range(l)]
  tangled = [chr(k[i] ^ v[i]) for i in range(l)]
  return ''.join(tangled)


def decrypt(key, code):
  l = max(len(key), len(code))

  def mod_len(x, i):
    return ord(x[i % len(x)])

  k = [mod_len(key, i) for i in range(l)]
  c = [ord(x) for x in code]
  ut = [chr(k[i] ^ c[i]) for i in range(l) if k[i] != c[i]]
  return ''.join(ut)


def plain2cipher(key, plain):
  return str2hexord(encrypt(key, plain))


def cipher2plain(key, cipher):
  return decrypt(key, hexord2str(cipher))


class ObjectDict(dict):
  def __init__(self, **contents):
    super(ObjectDict, self).__init__(**contents)

  def __getattr__(self, key):
    return self.get(key)

  def __setattr__(self, key, val):
    self[key] = val

def dict_diff(incoming, existing):
  """
  Compute and return dictionary of changes in incoming
  from what is in existing including new keys.  This only does
  the top level in case of nested dictionary.
  :param incoming: incoming changes
  :param existing: existing dictionary information
  :return: actual changes from incoming over existing
  """
  result = {}
  for k,v in incoming.items():
    if v != existing.get(k, None):
      result[k] = v
  return result

def splitter(lst):
  sz = len(lst)
  if sz == 0:
    return [], []
  if sz == 1:
    return lst, []
  if sz == 2:
    return lst[:-1], lst[-1:]
  return lst[:sz / 2], lst[sz / 2:]


def random_pick(lst):
  return lst[random.randint(0, len(lst) - 1)]
