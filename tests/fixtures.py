import pytest

from cattreelib import Category


@pytest.fixture
def tree():
    return Category(
        name='food',
        children=[
            Category(
                name='fruits',
                children=[
                    Category(
                        name='apple',
                        children=[
                            Category(name='red'),
                            Category(name='green'),
                            Category(name='yellow'),
                        ]
                    ),
                    Category(
                        name='grape',
                        children=[
                            Category(name='muscat'),
                            Category(name='shiraz'),
                            Category(name='merlot'),
                            Category(name='cabernet sauvignon'),
                        ]
                    ),
                    Category(
                        name='pear',
                        children=[
                            Category(name='asian'),
                            Category(name='european'),
                            Category(name='chinese'),
                        ]
                    ),
                ]
            ),
            Category(
                name='vegetables',
                children=[
                    Category(
                        name='pepper',
                        children=[
                            Category(name='red'),
                            Category(name='green'),
                            Category(name='yellow'),
                        ]
                    ),
                    Category(name='carrot'),
                    Category(
                        name='tomato',
                        children=[
                            Category(name='red'),
                            Category(name='green'),
                        ]
                    ),
                ]
            ),
        ]
    )


@pytest.fixture
def animal():
    animal = Category(name='animal')
    mammal = Category(name='mammal')
    cat = Category(name='cat')
    dog = Category(name='dog')
    lion = Category(name='lion')
    animal._children = [mammal]
    mammal._parent = animal
    mammal._children = [dog, cat]
    dog._parent = mammal
    cat._parent = mammal
    cat._children = [lion]
    lion._parent = cat

    return animal
