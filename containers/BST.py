'''
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the functions in the
BinaryTree file.
'''

from containers.BinaryTree import BinaryTree, Node


class BST(BinaryTree):
    '''
    The BST is a superclass of BinaryTree.
    That means that the BST class "inherits" all of the methods from
    BinaryTree,
    and we don't have to reimplement them.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        super().__init__()
        if xs:
            for vals in xs:
                self.insert(vals)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be
        used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's __repr__ will return "BST([1,2,3])"

        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST will have a
        correct implementation of __repr__, and that they won't have to
        reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def __iter__(self):
        return self._traverse(self.root)

    def _traverse(self, node):
        if node:
            for i in self._traverse(node.left):
                yield i
            yield node.value
            for i in self._traverse(node.right):
                yield i

    def __eq__(self, t2):
        '''
        This method checks to see if the contents of self and t2 are equal.
        The expression `a == b` desugars to `a.__eq__(b)`.
        NOTE:
        We only care about "semantic" equality,
        and not "syntactic" equality.
        That is, we do not care about the tree structure itself,
        and only care about the contents of what the tree contains.
        HINT:
        Convert the contents of both trees into a sorted list,
        then compare those sorted lists for equality.
        '''
        l1 = self.to_list('inorder')
        l2 = t2.to_list('inorder')
        if l1 != l2:
            return False
        return True

    def is_bst_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete
        functions
        are actually working.
        '''
        if self.root:
            return BST._is_bst_satisfied(self.root)
        return True

    @staticmethod
    def _is_bst_satisfied(node):
        '''
        FIXME:
        The current implementation has a bug:
        it only checks if the children of the current node are less
        than/greater than,
        rather than ensuring that all nodes to the left/right are less
        than/greater than.

        HINT:
        Use the _find_smallest and _find_largest functions to fix the bug.
        You should use the _ prefixed methods because those are static methods
        just like this one.'''
        ret = True
        if node.left:
            if node.value < BST._find_largest(node.left):
                ret = False
            else:
                ret &= BST._is_bst_satisfied(node.left)
        if node.right:
            if node.value > BST._find_smallest(node.right):
                ret = False
            else:
                ret &= BST._is_bst_satisfied(node.right)
        return ret

    def insert(self, value):
        '''
        Inserts value into the BST.

        FIXME:
        Implement this function.

        HINT:
        Create a staticmethod helper function following the pattern of
        _is_bst_satisfied.
        '''

        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self, value, self.root)

    @staticmethod
    def _insert(self, value, node):
        if node is None:
            node = Node(value)
        else:
            if node.value == value:
                return node
            elif node.value < value:
                node.right = self._insert(self, value, node.right)
            else:
                node.left = self._insert(self, value, node.left)
        return node

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.

        HINT:
        Repeatedly call the insert method.
        You cannot get this method to work correctly until you have gotten
        insert to work correctly.
        '''
        for vals in xs:
            self.insert(vals)

    def __contains__(self, value):
        '''
        Recall that `x in tree` desugars to `tree.__contains__(x)`.
        '''
        return self.find(value)

    def find(self, value):
        '''
        Returns whether value is contained in the BST.

        FIXME:
        Implement this function.
        '''
        return BST._find(value, self.root)

    @staticmethod
    def _find(value, node):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None:
            return False
        elif value < node.value:
            return BST._find(value, node.left)
        elif node.value == value:
            return True
        else:
            return BST._find(value, node.right)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        '''
        This is a helper function for find_smallest and not intended to be
        called directly by the user.
        '''
        assert node is not None
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)

    @staticmethod
    def _find_largest(node):
        assert node is not None
        if node.right is None:
            return node.value
        else:
            return BST._find_largest(node.right)

    def find_largest(self):
        '''
        Returns the largest value in the tree.

        FIXME:
        Implement this function.

        HINT:
        Follow the pattern of the _find_smallest function.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_largest(self.root)

    def remove(self, value):
        '''
        Removes value from the BST.
        If value is not in the BST, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        You should have everything else working before you implement this
        function.

        HINT:
        Use a recursive helper function.
        '''
        self.root = self._remove(value, self.root)

    def _remove(self, value, node):
        if node is None:
            return node
        elif value < node.value:
            node.left = self._remove(value, node.left)
        elif value > node.value:
            node.right = self._remove(value, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                least = self._find_smallest(node.right)
                node.value = least
                node.right = self._remove(node.value, node.right)
        return node

    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.

        FIXME:
        Implement this function.

        HINT:
        See the insert_list function.
        '''
        for val in xs:
            if self.__contains__(val):
                self.remove(val)
        return
