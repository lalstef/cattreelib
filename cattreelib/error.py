class CategoryTreeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class EmptyTreeError(CategoryTreeError):
    def __init__(self, category):
        self.message = f"Category '{category}'' is empty and no operations can be performed on it."
        super().__init__(self.message)


class NotACategoryError(CategoryTreeError):
    def __init__(self, category):
        self.message = f"'{category}' is not an instance of Category."
        super().__init__(self.message)


class ParentLoopError(CategoryTreeError):
    def __init__(self, category):
        self.message = f"'{category}' cannot be set to be parent of itself."
        super().__init__(self.message)


class SameNameParentError(CategoryTreeError):
    def __init__(self, category):
        self.message = f"'{category}' cannot be set to be parent of itself."
        super().__init__(self.message)


class ChildrenNotIterableError(CategoryTreeError):
    def __init__(self):
        self.message = f"Children must be empty list or iterable of Categories, not None."
        super().__init__(self.message)


class DuplicateNameError(CategoryTreeError):
    def __init__(self, name, path):
        self.message = f"Name '{name}' already exist in branch '{path}'!"
        super().__init__(self.message)


class RootDeleteError(CategoryTreeError):
    def __init__(self):
        self.message = f"Root category cannot be deleted!"
        super().__init__(self.message)


class RootMoveError(CategoryTreeError):
    def __init__(self):
        self.message = f"Root category cannot be moved!"
        super().__init__(self.message)


class CategoryDoesNotExistError(CategoryTreeError):
    def __init__(self, path):
        self.message = f"Category '{path}' does not exist in the tree!"
        super().__init__(self.message)


class InvalidPathError(CategoryTreeError):
    def __init__(self, path):
        self.message = path
        super().__init__(self.message)


class InvalidDepthError(CategoryTreeError):
    pass
