# Simple Category tree



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



## Usage

```python
from cattreelib import Category

animal = Category(name="animal")
animal.is_root()
>>> True

animal.is_leaf()
>>> True

lion = Category(name='lion')
tiger = Category(name='tiger')
cat = Category(name="cat", children=[lion, tiger])

lion.is_leaf()
>>> True

lion.is_sibling(tiger)
>>> True

animal.add(cat)
cat.is_root()
>>> False

dog = Category(name="dog", parent=animal)
wild_dog = Category(name='wild dog')
animal.add(wild_dog, 'dog')
>>> CategoryDoesNotExistError: Category 'dog' does not exist in the tree!

animal.add(dog)
animal.add(wild_dog, 'dog')
wild_dog in dog.children
>>> True

white_tiger = Category(name='white tiger')
animal.add(white_tiger, 'cat/tiger')
white_tiger.parent is tiger
>>> True

animal.get('cat/tiger/white tiger')
>>> <Category: white tiger>

animal.move('white tiger', 'dog')
animal.get('cat/tiger/white tiger')
>>> None

animal.get('dog/white tiger')
>>> <Category: white tiger>

animal.delete('animal/dog/white tiger')
animal.get('animal/dog/white tiger')
>>> None

animal.get('cat')
>>> <Category: cat>

animal.update(name='mammal')
animal.get('animal')
>>> None

animal.get('mammal')
>>> <Category: mammal>

animal.get('mammal/cat')
>>> <Category: cat>

animal.get_by_depth(0)
>>> [<Category: mammal>]

animal.get_by_depth(1)
>>> [<Category: cat>, <Category: dog>]

animal.get_by_depth(2)
>>> [<Category: lion>, <Category: tiger>, <Category: wild dog>]

animal.get_by_depth(3)
>>> []

animal.size()
>>> 6

white_tiger.size()
>>> 1

cat.size()
>>> 3
```



## Installation

```
# Install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Clone the library
git clone https://github.com/lalstef/cattreelib.git

# Install dependencies
cd cattreelib
poetry install
```

## Tests

```
pytest --cov-report=html  --cov=cattreelib
```
