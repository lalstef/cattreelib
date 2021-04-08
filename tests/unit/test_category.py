import pytest
from tests.fixtures import tree, animal

from cattreelib.category import Category
from cattreelib.path import Path
from cattreelib.error import (
    NotACategoryError,
    ParentLoopError,
    SameNameParentError,
    ChildrenNotIterableError,
    RootDeleteError,
    RootMoveError,
    DuplicateNameError,
    CategoryDoesNotExistError,
    InvalidDepthError,
)


def test_path_property():
    big_cat = Category(name='big cat')
    assert big_cat.path == 'big cat'

    cat = Category(name='cat', children=[big_cat])
    assert big_cat.path == 'cat/big cat'
    assert cat.path == 'cat'

    animal = Category(name='animal', children=[cat])
    assert big_cat.path == 'animal/cat/big cat'
    assert cat.path == 'animal/cat'
    assert animal.path == 'animal'


def test_get_parent():
    animal = Category(name='animal')
    cat = Category(name='cat')
    cat._parent = animal
    assert cat.parent == animal


def test_set_parent():
    animal = Category(name='animal')
    animal.parent = None
    assert animal._parent == None

    creature = Category(name='creature')
    animal.parent = creature
    assert animal._parent == creature

    with pytest.raises(NotACategoryError):
        animal.parent = ''

    with pytest.raises(NotACategoryError):
        animal.parent = 5

    with pytest.raises(NotACategoryError):
        animal.parent = []

    with pytest.raises(ParentLoopError):
        animal.parent = animal

    with pytest.raises(SameNameParentError):
        animal.parent = Category(name='animal')


def test_get_children():
    animal = Category(name='animal')
    cat = Category(name='cat')
    dog = Category(name='dog')

    animal._children = [cat, dog]
    assert animal.children == [cat, dog]


def test_set_children():
    animal = Category(name='animal')
    cat = Category(name='cat')
    dog = Category(name='dog')

    animal.children = []
    assert animal._children == []

    animal.children = [cat]
    assert animal._children == [cat]

    animal.children = [cat, dog]
    assert animal._children == [cat, dog]

    with pytest.raises(ChildrenNotIterableError):
        animal.children = cat

    with pytest.raises(NotACategoryError):
        animal.children = [cat, 'dog']

    with pytest.raises(NotACategoryError):
        animal.children = [cat, 7]

    with pytest.raises(NotACategoryError):
        animal.children = [7]


def test_get(tree):
    found = tree.get('food')
    assert isinstance(found, Category)
    assert found.name == 'food'

    found = tree.get('fruits')
    assert isinstance(found, Category)
    assert found.name == 'fruits'

    found = tree.get('food/fruits')
    assert isinstance(found, Category)
    assert found.name == 'fruits'

    found = tree.get('food/apple')
    assert found is None

    found = tree.get('food/fruits/apple')
    assert isinstance(found, Category)
    assert found.name == 'apple'

    found = tree.get('food/fruits/apple/red')
    assert isinstance(found, Category)
    assert found.name == 'red'

    found = tree.get('fruits/apple/red')
    assert isinstance(found, Category)
    assert found.name == 'red'

    found = tree.get('apple/red')
    assert isinstance(found, Category)
    assert found.name == 'red'

    found = tree.get('red')
    assert isinstance(found, Category)
    assert found.name == 'red'

    found = tree.get('carrot')
    assert isinstance(found, Category)
    assert found.name == 'carrot'

    found = tree.get('apple/red/small')
    assert found is None

    found = tree.get('cars')
    assert found is None

def test_add(animal):
    bird = Category(name='bird')
    animal.add(bird)
    assert bird in animal._children

    wild_dog = Category(name='wild_dog')
    animal.add(wild_dog, 'dog')
    assert wild_dog in animal.get('dog')._children

    tiger = Category(name='tiger')
    animal.add(tiger, 'cat')
    assert tiger in animal.get('cat')._children

    white_lion = Category(name='white_lion')
    animal.add(white_lion, 'cat/lion')
    assert white_lion in animal.get('cat/lion')._children


def test_delete_root(animal):
    with pytest.raises(RootDeleteError):
        animal.delete('animal')


def test_delete_1_node_path(animal):
    animal.delete('mammal')
    assert animal._children == []

def test_delete_2_nodes_path(animal):
    mammal = animal.get('mammal')
    cat = animal.get('cat')

    animal.delete('mammal/cat')

    assert cat not in mammal._children
    assert cat._parent is None


def test_delete_3_nodes_path(animal):
    cat = animal.get('cat')
    lion = animal.get('lion')

    animal.delete('mammal/cat/lion')

    assert lion not in cat._children
    assert lion._parent is None


def test_delete_from_the_middle(animal):
    cat = animal.get('cat')
    lion = animal.get('lion')

    animal.delete('cat/lion')

    assert lion not in cat._children
    assert lion._parent is None


def test_delete_leaf(animal):
    cat = animal.get('cat')
    lion = animal.get('lion')

    animal.delete('lion')

    assert lion not in cat._children
    assert lion._parent is None


def test_move(animal):
    lion = animal.get('lion')
    dog = animal.get('dog')
    cat = animal.get('cat')

    # invalid move
    with pytest.raises(RootMoveError):
        animal.move('animal', 'lion')

    # valid move
    animal.move('lion', 'dog')
    assert lion._parent is dog
    assert lion in dog.children
    assert lion not in cat.children


def test_update(animal):
    cat = animal.get('cat')
    cat.update(name='cats', description='some description')
    assert cat.name == 'cats'
    assert cat.description == 'some description'


def test_update_same_name_parent(animal):
    cat = animal.get('cat')
    with pytest.raises(DuplicateNameError):
        cat.update(name='mammal')


def test_update_same_name_sibling(animal):
    cat = animal.get('cat')
    with pytest.raises(DuplicateNameError):
        cat.update(name='dog')


def test_leaves(tree):
    fruit_leaves = tree.get('fruits/apple').leaves
    apple_red = tree.get('apple/red')
    apple_green = tree.get('apple/green')
    apple_yellow = tree.get('apple/yellow')
    assert fruit_leaves == [apple_red, apple_green, apple_yellow]


def test_size(tree):
    assert tree.size() == 24
    assert tree.size('food') == 24
    assert tree.size('fruits/apple') == 4
    assert tree.size('vegetables/carrot') == 1

    with pytest.raises(CategoryDoesNotExistError):
        tree.size('cars')


def test_is_leaf():
    big_cat = Category('big cat')
    cat = Category('cat', children=[big_cat])
    animal = Category('animal', children=[cat])

    assert animal.is_leaf() is False
    assert cat.is_leaf() is False
    assert big_cat.is_leaf() is True


def test_is_root():
    big_cat = Category('big cat')
    cat = Category('cat', children=[big_cat])
    animal = Category('animal', children=[cat])

    assert animal.is_root() is True
    assert cat.is_root() is False
    assert big_cat.is_root() is False


def test_is_sibling(animal):
    dog = animal.get('dog')
    cat = animal.get('cat')
    lion = animal.get('lion')
    assert cat.is_sibling(cat) is False
    assert cat.is_sibling(dog) is True
    assert cat.is_sibling(lion) is False


def test_get_by_depth(tree):
    categories_depth_0 = tree.get_by_depth(0)
    assert categories_depth_0 == [tree]

    fruits = tree.get('fruits')
    vegetables = tree.get('vegetables')
    categories_depth_1 = tree.get_by_depth(1)
    assert categories_depth_1 == [fruits, vegetables]

    categories_depth_2 = tree.get_by_depth(2)
    assert categories_depth_2 == [
        tree.get('apple'),
        tree.get('grape'),
        tree.get('pear'),
        tree.get('pepper'),
        tree.get('carrot'),
        tree.get('tomato')
    ]

    with pytest.raises(InvalidDepthError):
        tree.get_by_depth('1')

    with pytest.raises(InvalidDepthError):
        tree.get_by_depth(None)


def test_add_child():
    animal = Category(name='animal')
    cat = Category(name='cat')
    animal._add_child(cat)

    assert cat in animal.children
    assert cat.parent is animal

    # sibling with same name
    with pytest.raises(DuplicateNameError):
        another_cat = Category(name='cat')
        animal._add_child(another_cat)

    # ancestor with same name
    with pytest.raises(DuplicateNameError):
        another_cat = Category(name='cat')
        cat._add_child(another_cat)

    with pytest.raises(NotACategoryError):
        animal._add_child('cat')

    with pytest.raises(NotACategoryError):
        animal._add_child(id(cat))

    with pytest.raises(NotACategoryError):
        animal._add_child([cat])


def test_remove_child():
    animal = Category(name='animal')
    cat = Category(name='cat')
    cat._parent = animal
    dog = Category(name='dog')
    dog._parent = animal
    animal._children = [cat, dog]

    animal._remove_child(cat)
    assert animal._children == [dog]
    assert cat.parent is None


def test_add_parent():
    # add on top of root
    animal = Category(name='animal')
    cat = Category(name='cat')
    cat._add_parent(animal)

    assert cat.parent is animal
    assert animal.children == [cat]

    # add instead of previous parent
    animal = Category(name='animal')
    lion = Category(name='lion')
    animal._children = [lion]
    lion._parent = animal

    cat = Category(name='cat')
    lion._add_parent(cat)

    assert lion.parent is cat
    assert cat.children == [lion]
    assert animal.children == [cat]


def test_find_start(tree):
    found = tree._find_start(Path('food'))
    assert isinstance(found, Category)
    assert found.name == 'food'

    found = tree._find_start(Path('fruits'))
    assert isinstance(found, Category)
    assert found.name == 'fruits'

    found = tree._find_start(Path('food/fruits'))
    assert isinstance(found, Category)
    assert found.name == 'food'

    found = tree._find_start(Path('food/apple'))
    assert isinstance(found, Category)
    assert found.name == 'food'

    found = tree._find_start(Path('food/fruits/apple'))
    assert isinstance(found, Category)
    assert found.name == 'food'

    found = tree._find_start(Path('food/fruits/apple/red'))
    assert isinstance(found, Category)
    assert found.name == 'food'

    found = tree._find_start(Path('fruits/apple/red'))
    assert isinstance(found, Category)
    assert found.name == 'fruits'

    found = tree._find_start(Path('apple/red'))
    assert isinstance(found, Category)
    assert found.name == 'apple'

    found = tree._find_start(Path('red'))
    assert isinstance(found, Category)
    assert found.name == 'red'

    found = tree._find_start(Path('carrot'))
    assert isinstance(found, Category)
    assert found.name == 'carrot'

    found = tree._find_start(Path('apple/red/small'))
    assert found.name == 'apple'

    found = tree._find_start(Path('cars'))
    assert found is None


def test_find(tree):
    found = tree._find(Path('food/fruits'))
    assert isinstance(found, Category)
    assert found.name == 'fruits'

    found = tree._find(Path('food/fruits/apple'))
    assert isinstance(found, Category)
    assert found.name == 'apple'

    found = tree._find(Path('food/fruits/apple/red'))
    assert isinstance(found, Category)
    assert found.name == 'red'

    found = tree._find(Path('fruits/apple'))
    assert found is None

    found = tree._find(Path('apple'))
    assert found is None

    found = tree._find(Path('apple/red'))
    assert found is None

    found = tree._find(Path('red'))
    assert found is None

    found = tree._find(Path('carrot'))
    assert found is None
