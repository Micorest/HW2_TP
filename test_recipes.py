import pytest

from recipes import Ingredient, Recipe, ShoppingList

@pytest.mark.parametrize(
    "value",
    [
        -1,
        0
    ]
)
def test_ingredient_quantity_init_error(value):
    with pytest.raises(ValueError):
        Ingredient("Мука", value, "г")

@pytest.mark.parametrize(
    "value",
    [
        -1,
        0
    ]
)
def test_ingredient_quantity_change_error(value):
    ingredient = Ingredient("Мука", 100, "г")

    with pytest.raises(ValueError):
        ingredient.quantity = value

def test_ingredient_init_success():
    ingredient = Ingredient("Мука", 100, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 100
    assert ingredient.unit == "г"

def test_ingredient_quantity_success():
    ingredient = Ingredient("Мука", 100, "г")
    ingredient.quantity = 150
    assert ingredient.quantity == 150

def test_ingredient_str_success():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"

def test_ingredient_repr_success():
    ingredient = Ingredient("Мука", 100, "г")
    assert repr(ingredient) == "Ingredient('Мука', 100.0, 'г')"

def test_ingredient_eq_success():
    ingredient1 = Ingredient("Мука", 100, "г")
    ingredient2 = Ingredient("Мука", 500, "г")
    ingredient3 = Ingredient("Мука", 100, "кг")
    ingredient4 = Ingredient("Кофе", 100, "г")
    assert ingredient1 == ingredient2
    assert ingredient1 != ingredient3
    assert ingredient1 != ingredient4

@pytest.fixture
def pizza_recipe():
    return Recipe("Пицца",
                  [
                      Ingredient("Мука", 100, "г"),
                      Ingredient("Молоко", 200, "мл")
                  ])


def test_recipe(pizza_recipe):
    assert pizza_recipe.title == "Пицца"
    assert len(pizza_recipe.ingredients) == 2
    assert pizza_recipe.ingredients[0].name == "Мука"
    assert pizza_recipe.ingredients[0].quantity == 100
    assert pizza_recipe.ingredients[0].unit == "г"
    assert pizza_recipe.ingredients[1].name == "Молоко"
    assert pizza_recipe.ingredients[1].quantity == 200
    assert pizza_recipe.ingredients[1].unit == "мл"


def test_recipe_add_new_ingredient(pizza_recipe):
    pizza_recipe.add_ingredient(Ingredient("Томаты", 100, "г"))
    assert len(pizza_recipe.ingredients) == 3
    assert pizza_recipe.ingredients[2].name == "Томаты"
    assert pizza_recipe.ingredients[2].quantity == 100
    assert pizza_recipe.ingredients[2].unit == "г"


def test_recipe_add_exist_ingredient(pizza_recipe):
    pizza_recipe.add_ingredient(Ingredient("Молоко", 200, "мл"))
    assert len(pizza_recipe.ingredients) == 2
    assert pizza_recipe.ingredients[1].name == "Молоко"
    assert pizza_recipe.ingredients[1].quantity == 400
    assert pizza_recipe.ingredients[1].unit == "мл"


def test_recipe_scale_ratio_success(pizza_recipe):
    scaled_recipe = pizza_recipe.scale(2)
    assert scaled_recipe is not pizza_recipe
    assert scaled_recipe.ingredients[0].quantity == 200
    assert scaled_recipe.ingredients[1].quantity == 400


def test_recipe_scale_ratio_error(pizza_recipe):
    with pytest.raises(ValueError):
        pizza_recipe.scale(-1)


def test_recipe_len():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")
    recipe = Recipe("Много муки", [ing1, ing2])
    assert len(recipe) == 1


def test_shopping_list_add_recipe_success(pizza_recipe):
    sl = ShoppingList()
    sl.add_recipe(pizza_recipe, 2)
    assert len(sl._items) == 2
    assert sl._items[0][0].name == "Мука"
    assert sl._items[0][0].quantity == 200
    assert sl._items[0][0].unit == "г"
    assert sl._items[1][0].name == "Молоко"
    assert sl._items[1][0].quantity == 400.0
    assert sl._items[1][0].unit == "мл"


def test_shopping_list_add_recipe_error(pizza_recipe):
    sl = ShoppingList()
    with pytest.raises(ValueError):
        sl.add_recipe(pizza_recipe, 0)


def test_shopping_list_remove_recipe(pizza_recipe):
    sl = ShoppingList()
    sl.add_recipe(pizza_recipe, 1)
    sl.remove_recipe("Пицца")
    assert len(sl._items) == 0
    sl.remove_recipe("Много муки")
    assert len(sl._items) == 0


@pytest.fixture()
def milk_recipe():
    return Recipe("Молоко",
                  [
                      Ingredient(
                          "Молоко",
                          500,
                          "мл"
                      )
                  ])


@pytest.fixture()
def water_recipe():
    return Recipe("Вода",
                  [
                      Ingredient(
                          "Вода",
                          200,
                          "г"
                      )
                  ])


def test_shopping_list_get_list(pizza_recipe, milk_recipe):
    sl = ShoppingList()
    sl.add_recipe(pizza_recipe, 1)
    sl.add_recipe(milk_recipe, 1)
    result = sl.get_list()

    assert len(result) == 2
    assert result[0].name == "Молоко"
    assert result[0].quantity == 700
    assert result[0].unit == "мл"

    assert result[1].name == "Мука"
    assert result[1].quantity == 100
    assert result[1].unit == "г"


def test_shopping_list_add_operator(milk_recipe, water_recipe):
    sl1 = ShoppingList()
    sl1.add_recipe(milk_recipe, 2)

    sl2 = ShoppingList()
    sl2.add_recipe(water_recipe, 1)

    sl3 = sl1 + sl2

    assert isinstance(sl3, ShoppingList)
    assert sl3 is not sl1
    assert sl3 is not sl2
    assert len(sl3._items) == 2

    result = sl3.get_list()
    assert len(result) == 2
    assert result[0].name == "Вода"
    assert result[0].quantity == 200
    assert result[0].unit == "г"
    assert result[1].name == "Молоко"
    assert result[1].quantity == 1000
    assert result[1].unit == "мл"