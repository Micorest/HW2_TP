class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str) -> None:
        self.name = name
        self.quantity = quantity
        self.unit = unit
    @property
    def quantity(self) -> float:
        return self._quantity
    @quantity.setter
    def quantity(self, value: float | int | str) -> None:
        value_float = float(value)
        if value_float > 0:
            self._quantity = value_float
        else:
            raise ValueError("Количество должно быть положительным")
    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title: str, ingredients: list[Ingredient]) -> None:
        self.title = title
        self.ingredients = ingredients
    def add_ingredient(self, ingredient: Ingredient) -> None:
        if ingredient in self.ingredients:
            self.ingredients[self.ingredients.index(ingredient)].quantity += ingredient.quantity
        else:
            self.ingredients.append(ingredient)
    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return isinstance(ratio, (int, float)) and ratio > 0
    def scale(self, ratio) -> 'Recipe':
        # не говорилось про проверку, но включил
        if not self.is_valid_ratio(ratio):
            raise ValueError("Некорректный коэффициент масштабирования")
        return self.__class__(
            self.title,
            [
                Ingredient(
                    ingredient.name,
                    ingredient.quantity * ratio,
                    ingredient.unit
                )

                for ingredient in self.ingredients
            ]
        )
    def __len__(self) -> int:
        # вдруг при __init__ был задан не правильно, а в ТЗ написано "уникальные"
        uni_ingredients = []
        for ingredient in self.ingredients:
            if ingredient not in uni_ingredients:
                uni_ingredients.append(ingredient)
        return len(uni_ingredients)
    def __str__(self) -> str:
        return f"{self.title}:\n" + "\n".join(str(ingredient) for ingredient in self.ingredients)

class ShoppingList:
    def __init__(self) -> None:
        self._items: list[tuple[Ingredient, str]] = []
    def add_recipe(self, recipe: Recipe, portions: float) -> None:
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, scaled_recipe.title))
    def remove_recipe(self, title: str) -> None:
        self._items = [item for item in self._items if item[1] != title]
    def get_list(self) -> list[Ingredient]:
        uni_ingredient_to_quantity = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in uni_ingredient_to_quantity:
                uni_ingredient_to_quantity[key] += ingredient.quantity
            else:
                uni_ingredient_to_quantity[key] = ingredient.quantity
        result = []
        for key in uni_ingredient_to_quantity:
            result.append(
                Ingredient(
                    key[0],
                    uni_ingredient_to_quantity[key],
                    key[1]
                )
            )
        result.sort(key=lambda x: x.name)
        return result
    def __add__(self, other: object) -> 'ShoppingList':
        if not isinstance(other, ShoppingList):
            raise TypeError("Можно складывать только ShoppingList")
        result = ShoppingList()
        result._items = self._items + other._items
        return result