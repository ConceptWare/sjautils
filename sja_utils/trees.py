__author__ = 'samantha'

from .class_utils import immediate_superclasses
from .category import identity_function
from .properties import reader, accessor

node_value = lambda x: x.value
node_itself = identity_function


def pruning_tree_collect(root, children_function, test_function, result_function=None):
    """
    returns the nodes closest to the root nodes of the tree that satisfy the test_function.
    The value returned for a satisfying node is determined by the result_function which
    defaults to the node itself.
    """
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


def tree_order(hierarchy, sequence,
               h_extractor=identity_function, s_extractor=identity_function):
    """
    A generator returning items of sequence in the order they appear traversing the
    hierarchy (depth-first pre-order).
    """
    data = dict([(s_extractor(x), x) for x in sequence])
    for value in hierarchy.pre_order(h_extractor):
        if value in data:
            yield data[value]


class Node(object):
    """general node for a tree has only value and set of child nodes"""

    def __init__(self, value, *children):
        self._value = value
        self._children = list(children)
        self._parent = None

    value = accessor('_value')
    children = reader('_children')
    parent = reader('_parent')

    def pre_order(self, result_modifier=identity_function, node_function=node_value):
        def do_node(node):
            if node:
                yield result_modifier(node_function(node))
                for child in node._children:
                    for res in do_node(child):
                        yield res

        return do_node(self)

    def post_order(self, result_modifier=identity_function, node_function=node_value):
        def do_node(node):
            if node:
                for child in node._children:
                    for res in do_node(child):
                        yield res
                yield result_modifier(node_function(node))
            return do_node(self)

    def _add(self, node):
        # TODO check for silly things like circular references
        self._children.append(node)
        node._parent = self

    def add_child_node(self, node):
        self._add(node)

    def add_child_value(self, value):
        """adds a new Node with the given value and no children of its own"""
        self._add(self.__class__(value))


class BinaryNode(Node):
    """Tree restricxsted to max two children per node otherwise known as 'left' and 'right'
    """

    def __init__(self, value, *children):
        children = list(children)
        if len(children) > 2:
            raise Exception("can't have more than two children in a binary tree node!")
        if not children:
            children = [None, None]
        elif len(children) == 1:
            children.append(None)
        super(BinaryNode, self).__init__(value, children)

    @property
    def left(self):
        return self._children[0]

    @property
    def right(self):
        return self._children[1]

    def in_order(self, function=identity_function, node_function=node_value):
        """
        Usually this is done with binary trees but in the general case we can define it as
        do half my children, then me, then the other half at each node. The trouble is
        that it is not well-defined when there is only one child in the unordered n-ary
        tree case.
        """

        def do_node(node):
            if node:
                for res in do_node(node.left):
                    yield res
                yield function(node_function(node))
                for res in do_node(node.right):
                    yield res

        return do_node(self)


class Tree(object):
    def __init__(self, ordered=False, unique=False, key_extractor=identity_function,
                 value_extractor=identity_function, parent_extractor=None):
        """
        Create tree from given root
        :param root:
        :param ordered:
        :param unique:
        :param make_parent:
        """
        self._roots = []
        self._root_keys = set()
        self._key_fn = key_extractor
        self._value_fn = value_extractor
        self._parent_fn = parent_extractor
        self._ordered = ordered
        self._unique = unique
        self._node_map = {}


    @property
    def root(self):
        return self._roots[0] if len(self._roots) == 1 else None

    roots = reader('_roots')

    def add_root(self, node: Node):
        key = self._key_fn(node.value)
        if key not in self._root_keys:
            self._roots.append(node)

    def node_from_data(self, data):
        key = self._key_fn(data)
        node = self.get_node(key)
        if not node:
            node = Node(self._value_fn(data))
            self._node_map[key] = node
        return node

    def get_node(self, node_id):
        return self._node_map.get(node_id)

    def add_with_data(self, data, parent_key=None):
        node = self.get_node(self._key_fn(data))
        if not node:
            node = self.node_from_data(data)
            pnode = self.get_node(parent_key)
            if not pnode:
                parent = self._parent_fn(data) if self._parent_fn else None
                if parent:
                    pnode = self.add_with_data(parent)
            if pnode:
                pnode.add_child_node(node)
            else:
                self._root = node
        return node

    def get_parent(self, parent_data):
        return self.node_from_data(parent_data)

    def __contains__(self, val):
        return val in self._node_map

    def add_parent_child(self, parent_value, child_value, dup_if_missing=False):
        parent = self._get_parent(parent_value)
        if parent:
            child = self._node_map.get(child_value)
            if child and self._unique:
                raise Exception('A node with value %s is already in the unique tree' % child_value)
            else:
                new_child = parent.__class__(child_value)
                parent.add_child_node(new_child)
                if not child:
                    self._node_map[child_value] = new_child

    def pre_order(self, fun=identity_function, node_function=node_value):
        return self._root.pre_order(fun)

    def post_order(self, fun=identity_function, node_function=node_value):
        return self._root.post_order(fun)



class BinaryTree(Tree):
    def __init__(self, root, ordered=True):
        super(BinaryTree, self).__init__(root)

    def in_order(self, fun=identity_function, node_function=node_value):
        return self._root.in_order(fun)

    def insert(self, value):
        pass

    def remove(self, value):
        pass

    def __contains__(self, value):
        pass


class MultiParentTree(Tree):
    def __init__(self, root, ordered=False):
        super(MultiParentTree, self).__init__(root, ordered=ordered)
        self._node_map = {}

    def add_with_data(self, data, parent_keys=None):
        node = self.get_node(self._key_fn(data))
        if not node:
            node = self.node_from_data(data)
            parents = self._parent_fn(data)
            for parent in parents:
                p_node = self.get_node(self._key_fn(parent))
                if not p_node:
                    p_node = self.add_with_data(parent)
                p_node.add_child_node(node)
        return node

    def add_parent_child(self, parent_value, child_value):
        parent = self._get_parent(parent_value)
        if parent:
            child = self._node_map.get(child_value)
            if not child:
                child = parent.__class__(child_value)
                self._node_map[child_value] = child
            parent.add_child_node(child)


class ClassHierarchy(MultiParentTree):
    def __init__(self, the_root):
        root = the_root if isinstance(the_root, Node) else Node(the_root)
        super().__init__(root)
        order = root.pre_order(identity_function, node_function=node_itself)
        for node in order:
            self._node_map[node.value] = node

    def make_parent(self, parent_class):
        for superclass in immediate_superclasses(parent_class):
            parent = self._get_parent(superclass)
            self.add_parent_child(superclass, parent_class)


if __name__ == '__main__':
    # test pruning_tree__collect
    class Node:
        def __init__(self, value):
            self.val = value
            self._children = []

        def add_child(self, c):
            self._children.append(c)

        def gen_test(value):
            return lambda x: x.val == value

        children = lambda x: x._children
        root = Node(6)
        a = Node(5)
        b = Node(4)
        c = Node(6)
        d = Node(4)
        e = Node(4)
        root.add_child(b)
        root.add_child(c)
        c.add_child(d)
        b.add_child(e)
        res = pruning_tree_collect(root, children, gen_test(4))
        # print res
        assert (len(res) == 2)
        assert (b in res)
        assert (d in res)
