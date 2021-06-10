import inspect


def flat_keys(arg, key=''):
    acc = {}

    def flatten(something, key):
        key_extend = lambda ek: ('%s[%s]' % (key, ek)) if key else ek
        if isinstance(something, dict):
            for k, v in something.items():
                nk = key_extend(k)
                flatten(v, nk)
        elif isinstance(something, list or isinstance(something, tuple)):
            for index, item in enumerate(something):
                flatten(item, key_extend(index))
        else:
            acc[key] = something

    flatten(arg, key)
    return acc


def dict_diff(new, old):
    flat_new = flat_keys(new)
    flat_old = flat_keys(old)
    modified = {k: v for k, v in flat_new.items() if k in flat_old and flat_old[k] != v}
    added = {k: v for k, v in flat_new.items() if k not in flat_old}
    dropped = {k: v for k, v in flat_old.items() if k not in flat_new}
    return dict(
        modified=modified, added=added, dropped=dropped
    )


def ensure_in_dict(a_dict, key, value):
    if key not in a_dict:
        a_dict[key] = value


def get_dict_path(a_dict, *keys):
    '''
    Gets a subpart of a dictionary based on a dictionary navigation path to it.
    :param a_dict: the dictionary to retrieve from
    :param keys: the ordered keys to navigate the dict to desired subpart
    :return: None if path not present in dictionary else subpart of dictionary at the path.
    '''
    if not (a_dict and isinstance(a_dict, dict)):
        return None
    working = a_dict
    for key in keys:
        working = working.get(key)
        if not working:
            return None
    return working


def with_keys(a_dict, *keys):
    return {k: a_dict[k] for k in keys if k in a_dict}


def without_keys(a_dict, *keys):
    return {k: v for k, v in a_dict.items() if k not in keys}


def dict_values(a_dict, *kp):
    def get(d, key):
        if '.' in key:
            parts = key.split('.')
            sub = a_dict.get(parts[0], {})
            rest = '.'.join(parts[1:])
            return get(sub, rest)
        else:
            return d.get(key)

    return [get(a_dict, k) for k in kp]


def add_missing(a_dict, missing_dict):
    update = {k: v for k, v in missing_dict.items() if k not in a_dict}
    a_dict.update(update)


class DictObject(dict):
    '''
    Provides both dict functionality and json like attribute access to keys.  Works for
    multiple level dictionaries as well.
    '''

    def __init__(self, **data):
        super().__init__(**data)
        self._adjust_dicts()

    def _adjust_dicts(self):
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = DictObject(**v)

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, val):
        if isinstance(val, dict):
            val = DictObject(**val)
        self[name] = val


class ImmutableKeysDict(DictObject):
    '''DictObject that will not accept new keys'''

    def __init__(self, **kvs):
        super().__init__(**kvs)

    def __setattr__(self, key, value):
        if key in self:
            super().__setattr__(key, value)

    def __setitem__(self, key, value):
        if key in self:
            dict.__setitem__(self, key, value)


def param_dict(smash_kwargs=True):
    '''
    To be called within a function. Returns a dictionary of values the function was called with.
    :return: dictionary of parameter values.
    :param smash_kwangs - whether to return kwargs as top level members of the dictionary
    :return the dictionary of {param_name => value}
    '''

    raw = inspect.getargvalues(inspect.currentframe())
    res = raw.locals
    if smash_kwargs:
        kw = res.pop('kwargs', {})
        res.update(kw)
    return res
