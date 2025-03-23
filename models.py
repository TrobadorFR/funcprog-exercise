"""File: models.py
Holds data object classes for recipes and their components"""
from dataclasses import dataclass
from datetime import date
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Ingredient:
    name: str
    amount: float
    unit: str
    ingredients: List['Ingredient'] # Nested list of Ingredient objects
    preparation: List[str]

    def __repr__(self) -> str:
        """For shorter testing output with helper.ut()."""
        return self.name

@dataclass(frozen=True)
class NutritionInfo:
    calories: float
    fat: float # Convert from %
    carbohydrates: float # Convert from %
    protein: float # Convert from %

@dataclass(frozen=True)
class Recipe:
    title: str
    date: date
    ingredients: List[Ingredient] # Nested list of Ingredient objects
    preparation: List[str]
    comment: str
    nutrition: NutritionInfo
    related: Optional[List[Tuple[str, str]]]

    def __repr__(self) -> str:
        """For shorter testing output with helper.ut()."""
        return self.title

# recipe = Recipe("test",
#                 date(1998, 10, 31),
#                 [None, None],
#                 ["slide to the left", "slide to the right"],
#                 "shake it",
#                 NutritionInfo(5, 5, 5, 5),
#                 None)

# print(recipe)