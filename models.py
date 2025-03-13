from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Ingredient:
    name: str
    amount: float
    unit: str

@dataclass(frozen=True)
class NutritionInfo:
    calories: float
    fat: float # Convert from %age
    carbohydrates: float # Convert from %age
    protein: float # Convert from %age

@dataclass(frozen=True)
class Recipe:
    title: str
    date: date
    ingredients: [] # Nested list of Ingredient objects
    preparation: [str]
    comment: str
    nutrition: NutritionInfo
    related: [(str, str)]

# recipe = Recipe("test",
#                 date(1998, 10, 31),
#                 [None, None],
#                 ["slide to the left", "slide to the right"],
#                 "shake it",
#                 NutritionInfo(5, 5, 5, 5),
#                 None)

# print(recipe)