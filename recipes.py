class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str) -> None:
        self.name = name
        self.quantity = quantity
        self.unit = unit
    @property
    def quantity(self) -> float:
        return self._quantity
    @quantity.setter
    def quantity(self, value: object) -> None:
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
