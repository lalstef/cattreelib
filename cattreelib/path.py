from collections.abc import Iterable
from cattreelib.error import InvalidPathError


class Path:
    """
    Represents a sequence of nodes that lead from one node to another following parent-child relationship.

    For the sake of simplicity:
        - We assume that the PATH_SEPARATOR won't be found in any category name.
        - Wild card search is not supported (root/cat1/*/cat3).
        - Path starting or ending in PATH_SEPARATOR are invalid
              root/cat1/cat2/
              /root/cat1/cat2

    """
    SEPARATOR = '/'

    def __init__(self, nodes):
        if isinstance(nodes, str):
            nodes = nodes.split(Path.SEPARATOR)
        elif isinstance(nodes, Iterable):
            # list() is used so new object is created, instead of just reference to nodes
            nodes = list(nodes)
        elif isinstance(nodes, Path):
            # list() is used so new object is created, instead of just reference to nodes._nodes
            nodes = list(nodes._nodes)
        else:
            raise TypeError("Path must be str or iterable.")

        # Make sure that no node is None or empty string
        if not nodes:
            raise InvalidPathError(nodes)

        for node in nodes:
            if not node or not isinstance(node, str):
                raise InvalidPathError(nodes)

        self._nodes = nodes

    def __str__(self):
        return Path.SEPARATOR.join(self._nodes)

    def __repr__(self):
        return f"<Path: {self}>"

    def __getitem__(self, *args):
        return Path(self._nodes.__getitem__(*args))

    def __len__(self):
        return len(self._nodes)

    def __eq__(self, other):
        return self._nodes == Path(other)._nodes

    def __add__(self, other):
        self._nodes += Path(other).nodes
        return self

    @property
    def nodes(self):
        return self._nodes

    @property
    def root(self):
        return self._nodes[0]

    def add(self, node):
        self._nodes.append(node)
