import pytest

from recipes import Ingredient, Recipe

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
def recipe():
    return Recipe("Пицца",
    [
        Ingredient("Мука", 100, "г"),
        Ingredient("Молоко", 200, "мл")
    ])

def test_recipe(recipe):
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 100
    assert recipe.ingredients[0].unit == "г"
    assert recipe.ingredients[1].name == "Молоко"
    assert recipe.ingredients[1].quantity == 200
    assert recipe.ingredients[1].unit == "мл"

def test_recipe_add_new_ingredient(recipe):
    recipe.add_ingredient(Ingredient("Томаты", 100, "г"))
    assert len(recipe.ingredients) == 3
    assert recipe.ingredients[2].name == "Томаты"
    assert recipe.ingredients[2].quantity == 100
    assert recipe.ingredients[2].unit == "г"

def test_recipe_add_exist_ingredient(recipe):
    recipe.add_ingredient(Ingredient("Молоко", 200, "мл"))
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[1].name == "Молоко"
    assert recipe.ingredients[1].quantity == 400
    assert recipe.ingredients[1].unit == "мл"

def test_recipe_scale_ratio_success(recipe):
    scaled_recipe = recipe.scale(2)
    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 200
    assert scaled_recipe.ingredients[1].quantity == 400

def test_recipe_scale_ratio_error(recipe):
    with pytest.raises(ValueError):
        scaled_recipe = recipe.scale(-1)

def test_recipe_len():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")
    recipe = Recipe("Много муки", [ing1, ing2])
    assert len(recipe) == 1
