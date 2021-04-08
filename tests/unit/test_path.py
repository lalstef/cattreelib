import pytest
from cattreelib.category import Path
from cattreelib.error import InvalidPathError


def test_init_from_str():
    path = Path('food')
    assert path._nodes == ['food']

    path = Path('food/fruits')
    assert path._nodes == ['food', 'fruits']

    path = Path('food/fruits/apple')
    assert path._nodes == ['food', 'fruits', 'apple']


def test_init_from_iterable():
    path = Path(['food', 'fruits', 'apple'])
    assert path._nodes == ['food', 'fruits', 'apple']

    path = Path(('food', 'fruits', 'apple'))
    assert path._nodes == ['food', 'fruits', 'apple']


def test_init_from_path():
    path = Path(Path('food'))
    assert path._nodes == ['food']


def test_invalid_path():
    with pytest.raises(TypeError):
        Path(None)

    with pytest.raises(TypeError):
        Path(10)

    with pytest.raises(InvalidPathError):
        Path([10, 7, 5])

    with pytest.raises(InvalidPathError):
        Path('')

    with pytest.raises(InvalidPathError):
        Path([])

    with pytest.raises(InvalidPathError):
        Path('/food/fruits/apple')

    with pytest.raises(InvalidPathError):
        Path('food//fruits/apple')

    with pytest.raises(InvalidPathError):
        Path('food/fruits/apple/')


def test_str():
    assert str(Path('food')) == 'food'
    assert str(Path(['food'])) == 'food'
    assert str(Path(['food', 'fruits'])) == 'food/fruits'


def test_equal():
    assert Path('food') == Path('food')
    assert Path(['food']) == Path(['food'])
    assert Path('food') == Path(['food'])
    assert Path('food/fruits/apple') == Path(['food', 'fruits', 'apple'])
    assert Path(['food', 'fruits', 'apple']) == Path(['food', 'fruits', 'apple'])
    assert Path('food/fruits/apple') == Path('food/fruits/apple')

    assert Path('food') != Path('apple')
    assert Path('food') != Path('food/apple')
    assert Path('food/fruits/apple') != Path(['food/fruits/apple'])

    assert Path('food') == 'food'
    assert Path('food') == ['food']
    assert Path('food/fruits') == 'food/fruits'
    assert Path('food/fruits') == ['food', 'fruits']


def test_getitem():
    pass


def test_len():
    assert len(Path('food')) == 1
    assert len(Path('food/fruits')) == 2
    assert len(Path('food/fruits/apple')) == 3


def test_add():
    # add Path
    path = Path('food')
    path = path + Path('fruits')
    assert path._nodes == ['food', 'fruits']

    # add string (single)
    path = Path('food')
    path = path + 'fruits'
    assert path._nodes == ['food', 'fruits']

    # add string (multiple)
    path = Path('food')
    path = path + 'fruits/apple'
    assert path._nodes == ['food', 'fruits', 'apple']

    # add iterable (single)
    path = Path('food')
    path = path + ['fruits']
    assert path._nodes == ['food', 'fruits', 'apple']

    # add iterable (multiple)
    path = Path('food')
    path = path + ['fruits', 'apple']
    assert path._nodes == ['food', 'fruits', 'apple']


def test_nodes():
    assert Path('food').nodes == ['food']
    assert Path('food/fruits/apple').nodes == ['food', 'fruits', 'apple']
    assert Path('apple/red').nodes == ['apple', 'red']


def test_root():
    assert Path('food').root == 'food'
    assert Path('fruits/apple').root == 'fruits'
    assert Path('food/fruits/apple').root == 'food'


def test_add():
    path = Path('food')
    path.add('fruits')
    assert path._nodes == ['food', 'fruits']

    path.add('apple')
    assert path._nodes == ['food', 'fruits', 'apple']
