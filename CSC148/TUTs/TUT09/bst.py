
from typing import Any

class BinarySearchTree:
    """Binary Search Tree class."""

    def __init__(self, root: Any = None) -> None:
        """Initialize a new BST containing only the given root value."""
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty."""
        return self._root is None

    def height(self) -> int:
        """Return the height of this BST."""
        if self.is_empty():
            return 0
        else:
            left_height = self._left.height() if self._left else 0
            right_height = self._right.height() if self._right else 0
            return 1 + max(left_height, right_height)

    def items_in_range(self, start: Any, end: Any) -> list:
        """Return the items in this BST between <start> and <end>, inclusive, in sorted order."""
        if self.is_empty():
            return []
        
        result = []
        if self._left and start <= self._root:
            result.extend(self._left.items_in_range(start, end))
        
        if start <= self._root <= end:
            result.append(self._root)
        
        if self._right and self._root <= end:
            result.extend(self._right.items_in_range(start, end))
        
        return result

    def insert(self, item: Any) -> None:
        """Insert <item> into this BST, maintaining the BST property."""
        if self.is_empty():
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item < self._root:
            self._left.insert(item)
        else:
            self._right.insert(item)

    def rotate_right(self) -> None:
        """Rotate the BST clockwise, i.e. make the left subtree the root."""
        if self._left.is_empty():
            return  # Can't rotate if there's no left subtree to promote
        
        new_root = self._left
        self._left = new_root._right
        new_root._right = BinarySearchTree(self._root)
        new_root._right._left = self._left
        new_root._right._right = self._right

        # Update the current root to new values
        self._root, self._left, self._right = new_root._root, new_root._left, new_root._right

    def rotate_left(self) -> None:
        """Rotate the BST counter-clockwise, i.e. make the right subtree the root."""
        if self._right.is_empty():
            return  # Can't rotate if there's no right subtree to promote
        
        new_root = self._right
        self._right = new_root._left
        new_root._left = BinarySearchTree(self._root)
        new_root._left._left = self._left
        new_root._left._right = self._right

        # Update the current root to new values
        self._root, self._left, self._right = new_root._root, new_root._left, new_root._right

    def __str__(self) -> str:
        """Return a string representation of this BST."""
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST."""
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer
