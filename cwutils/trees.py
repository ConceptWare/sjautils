__author__ = 'samantha'
from .class_utils import immediate_superclasses
from .category import identity_function
from .properties import reader, accessor

node_value = lambda x: x.value
node_itself = identity_function

class Node(object):
    """general node for a tree has only value and set of child nodes"""
    def __init__(self, value, *children):
        self._value = value
        self._children = list(children)

    value = accessor('_value')
    children = reader('_children')

    def pre_order(self, function = identity_function, node_function = node_value):
        def do_node(node):
            if node:
                yield function(node_function(node))
                for child in node._children:
                    for res in do_node(child):
                        yield res
        return do_node(self)

    def post_order(self, function = identity_function, node_function = node_value):
        def do_node(node):
            if node:
                for child in node._children:
                    for res in do_node(child):
                        yield res
                yield function(node_function(node))
        return do_node(self)

    def _add(self, node):
        #TODO check for silly things like circular references
        self._children.append(node)

    def add_child_node(self, node):
        self._add(node)

    def add_child_value(self, value):
        """adds a new Node with the given value and no children of its own"""
        self._add(self.__class__(value))

class BinaryNode(Node):
    """Tree restricted to max two children per node otherwise known as 'left' and 'right'"""
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

    def in_order(self, function = identity_function, node_function=node_value):
        """Usually this is done with binary trees but in the general case we can define it as
        do half my children, then me, then the other half at each node. The trouble is that it
        is not well-defined when there is only one child in the unordered n-ary tree case."""

        def do_node(node):
            if node:
                for res in do_node(node.left):
                    yield res
                yield function(node_function(node))
                for res in do_node(node.right):
                    yield res
        return do_node(self)

class Tree(object):
    def __init__(self, root, ordered=False, unique=False, make_parent = None):
        self._root = root
        self._ordered = ordered
        self._unique = unique
        self._node_map = {}
        self._make_parent = make_parent or (lambda value : None)

    root = reader('_root')

    def make_parent(self, parent_value):
        return None

    def _get_parent(self, parent_value):
        parent = self._node_map.get(parent_value)
        if not parent:
            parent = self.make_parent(parent_value)
        return parent

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

    def pre_order(self, fun = identity_function, node_function=node_value):
        return self._root.pre_order(fun)

    def post_order(self, fun=identity_function, node_function=node_value):
        return self._root.post_order(fun)

class BinaryTree(Tree):
    def __init__(self, root, ordered = True):
        super(BinaryTree, self).__init__(root)

    def in_order(self, fun = identity_function, node_function=node_value):
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
        super(ClassHierarchy, self).__init__(root)
        order = root.pre_order(identity_function, node_function=node_itself)
        for node in order:
            self._node_map[node.value] = node

    def make_parent(self, parent_class):
        for superclass in immediate_superclasses(parent_class):
            parent = self._get_parent(superclass)
            self.add_parent_child(superclass, parent_class)

