"""

                                      SAMPLE HIERARCHY DIAGRAM

                                                food
                                                  |
                       ======================================================
                       |                                                    |
                    fruits                                              vegetables
                       |                                                    |
           ========================                           =================================
           |                      |                           |                  |            |
        apple                   grape                       pepper             carrot      tomato
 ===================        =================            ================                  =========
 |        |        |        |       |       |            |      |       |                  |       |
red    yellow   green     muscat shiraz  merlot         red   green   yellow              red    green
"""

from collections.abc import Iterable
from cattreelib.path import Path
from cattreelib.error import (
    ParentLoopError,
    NotACategoryError,
    SameNameParentError,
    ChildrenNotIterableError,
    DuplicateNameError,
    RootDeleteError,
    RootMoveError,
    CategoryDoesNotExistError,
    InvalidDepthError,
)


class Category:
    """
    Represents a hierarchical structure of categories.

    Root:
        The node without a parent.

    Leaf:
        A node without any children.

    Path:
        A sequence of nodes that lead from one node to another following the parent-child relationship.
        The path of a node is the path from the root node to point of interest.
        The path of a node is unique within certain tree.

    The implementation of the Category class is based on the following rules:
        Path is unique for each category.
        Two categories with the same name can't be siblings or ancestors to each other
        Name can only be string (not numbers or other objects).
        Parent must be either None or a Category instance.
        A category cannot be parent of itself.
        Children must be either empty list or a list of Category objects.
        Children cannot be None.
        Root cannot be deleted.
        Root cannot be moved.
        A category can be a root and a leaf at the same time.
        A parent can't be a child of any of its children.

    """
    def __init__(self, name=None, description=None, image=None, parent=None, children=None):
        self._parent = None
        self._children = []

        self.name = name
        self.description = description
        self.image = image
        self.parent = parent
        self.children = children or []

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category: {self.name}>"

    @property
    def path(self):
        """
        Return the path from the root to the current category including the current one.
        """
        if not self.parent:
            return Path([self.name])
        return Path(self.parent.path) + Path([self.name])

    @property
    def parent(self):
        """
        Return the parent of the category
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Set the parent of the current category.

        Makes sure that:
            Parent is an instance of Category
            Parent is not the current category
            Parent has different name than current category
            If parent is None and the category has a parent, remove the category from current parent's children.

        Parameters:
        parent(Category): the new parent of the current category

        Returns:
        None
        """
        if parent is not None:
            if not isinstance(parent, Category):
                raise NotACategoryError(parent)
            if self is parent:
                raise ParentLoopError(parent)
            if self.name == parent.name:
                raise SameNameParentError(parent)
        else:
            if self.parent:
                self.parent._remove_child(self)
        self._parent = parent

    @property
    def children(self):
        """
        Return a list of the children of the category
        """
        return self._children

    @children.setter
    def children(self, children):
        """
        Set the children of the current category.

        Parameters:
        children (list): iterable of instances of Category

        Returns:
        None
        """
        if not isinstance(children, Iterable):
            raise ChildrenNotIterableError()

        self._children = []
        for child in children:
            if not isinstance(child, Category):
                raise NotACategoryError(child)
            self._add_child(child)

    @property
    def leaves(self):
        """
        Return all the leaf categories
        """
        leaves = []
        if not self.children:
            leaves = [self]
        else:
            for child in self.children:
                leaves.extend(child.leaves)
        return leaves

    def get(self, path):
        """
        Get the category whose path is given as argument.

        Search can be performed anywhere in the tree (cf sample diagram):

        Valid searches:
            tree.get('food') -> food (itself)
            tree.get('fruits') -> fruits
            tree.get('apple') -> apple
            tree.get('fruits/apple') -> apple
            tree.get('food/fruits/apple') -> apple


        Invalid searches (return None):
            tree.get('food/apple')

        Parameters:
        path(str,iterable,Path): path of the category that is searched for

        Returns:
        found(Category,None): the found category or None
        """
        found = None
        path = Path(path)

        start = self._find_start(path)
        if start:
            found = start._find(path)

        return found

    def add(self, category, path=None):
        """
        Add category under the given path.

        Parameters:
        category(Category): category to add under path
        path(str,iterable,Path): path under which the category is to be added

        Returns:
        None
        """
        if not path:
            self._add_child(category)
        else:
            path = Path(path)
            parent = self.get(path)
            if not parent:
                raise CategoryDoesNotExistError(path)
            parent._add_child(category)

    def delete(self, path):
        """
        Remove the instance from parent's children.
        A category can be deleted anywhere in the tree.

        Makes sure that:
            Root category cannot be deleted.

        Parameters:
        path(str,iterable,Path): path of the category to be deleted.

        Returns:
        None

        Raises:
        RootDeleteError
        """
        to_delete = self.get(Path(path))
        if to_delete.is_root():
            raise RootDeleteError()
        to_delete.parent._remove_child(to_delete)

    def move(self, path, new_parent_path):
        """
        Move category from anywhere to anywhere in the tree.
        Category can only be moved 'under' a new parent. So it can't be moved on top of the root category.

        Makes sure that:
            Root category cannot be moved.

        Parameters:
        path(str,iterable,Path): path of the category to be moved.
        new_parent_path(str,iterable,Path): path of the new parent of the category to be moved.

        Returns:
        None

        Raises:
        RootMoveError
        """
        path = Path(path)
        new_parent_path = Path(new_parent_path)

        category = self.get(path)
        if category.is_root():
            raise RootMoveError()

        new_parent = self.get(new_parent_path)
        category.parent._remove_child(category)
        new_parent._add_child(category)

    def update(self, **data):
        """
        Update any of the attributes of the category except for parent and child.

        Makes sure that:
            If the name is updated it doesn't break the rules about siblings or ancestors with the same name.

        Parameters:
        data(dictionary): attributes with their respective values that need to be updated.

        Returns:
        None

        Raises:
        DuplicateNameError
        """
        self.description = data.get('description') or self.description
        self.image = data.get('image') or self.image
        if 'name' in data:
            new_name = data.get('name')

            if new_name in self.path:
                raise DuplicateNameError(new_name, self.path)

            if self.parent:
                for child in self.parent.children:
                    if new_name in child.name:
                        raise DuplicateNameError(new_name, self.path)

            self.name = new_name

    def size(self, path=None):
        """
        Return the number of all the categories under a given path including the root of the given tree.

        Parameters:
        path(str,iterable,Path): path of the category whose size should be returned

        Return:
        size(int): number of all categories under the current one

        Raises:
        CategoryDoesNotExistsError
        """
        size = 1
        if not path:
            category = self
        else:
            category = self.get(Path(path))
            if not category:
                raise CategoryDoesNotExistError(path)

        for child in category.children:
            size = size + child.size()
        return size

    def is_root(self):
        """
        Return True if the current category is the root one, False otherwise.

        The category is root when its parent is None.
        """
        return self.parent is None

    def is_leaf(self):
        """
        Return True if the current category is a leaf, False otherwise.

        The category is a leaf when it doesn't have children.
        """
        return not self.children

    def is_sibling(self, other):
        """
        Return True if other is sibling to the current category, False otherwise

        Parameters:
        other(Category)

        Returns:
        (bool)
        """
        return self.parent is other.parent and self is not other

    def get_by_depth(self, depth):
        """
        Return all categories at a given depth within the tree.

        Returning categories by depth from bottom up (i.e. negative depths) is not supported!

        Parameters:
        depth(int)

        Returns:
        categories(iterable of Category): categories found at the given depth
        """
        categories = []

        if not isinstance(depth, int):
            raise InvalidDepthError('Depth must be an integer')

        if depth == 0:
            return [self]
        elif depth == 1:
            categories = self.children
        else:
            depth = depth - 1
            for child in self.children:
                categories.extend(child.get_by_depth(depth))

        return categories

    def _add_child(self, child):
        """
        Add a child to the children of the current category.

        Checks that:
            Child has a different name than the current category or its ancestors.
            Child has a different name than its siblings.

        Parameters:
        child(Category): child to be added to the children

        Returns:
        None
        """
        if not isinstance(child, Category):
            raise NotACategoryError(child)

        # Check no ancestors with the same name
        if child.name in self.path:
            raise DuplicateNameError(child.name, self.path)

        # Check no siblings with the same name
        for ch in self.children:
            if ch.name == child.name:
                raise DuplicateNameError(child.name, child.path)

        self.children.append(child)
        child.parent = self

    def _remove_child(self, child):
        """
        Remove child from the children.

        Parameters:
        child(Category): child to be removed

        Returns:
        None
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def _add_parent(self, parent):
        """
        Add (new) parent to the current category.

        Makes sure that:
            If current category has a parent, add the new parent as child of the parent (grandparent)
            and remove the current category from grandparent's chidren

        Parameters:
        parent(Category): the new parent of the current category

        Returns:
        None
        """
        grand_parent = self.parent
        parent._add_child(self)
        if grand_parent:
            grand_parent.children.remove(self)
            grand_parent._add_child(parent)

    def _find_start(self, path):
        """
        Parameters:
        path(str,iterable,Path): path of the category that is searched for

        Returns:
        found(Category,None): the found category or None
        """
        found = None

        if self.name == path.root:
            found = self
        else:
            for child in self.children:
                found = child._find_start(path)
                # Stop when first occurrence is found
                # (even though there might be others somewhere)
                if found:
                    break

        return found

    def _find(self, path):
        """
        Parameters:
        path(str,iterable,Path): path of the category that is searched for

        Returns:
        found(Category,None): the found category or None
        """
        found = None
        if self.name == path.root:
            if len(path) == 1:
                found = self
            else:
                for child in self.children:
                    found = child._find(path[1:])
                    if found:
                        break
        return found

