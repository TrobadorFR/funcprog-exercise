"""File: models.py
Holds data object classes for recipes and their components"""
from dataclasses import dataclass
from datetime import date
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Ingredient:
    """Data object for an ingredient in a recipe."""
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
    """Data object component for nutrition information."""
    calories: float
    fat: float # Convert from %
    carbohydrates: float # Convert from %
    protein: float # Convert from %

@dataclass(frozen=True)
class Recipe:
    """Data object for a recipe."""
    title: str
    date: date
    ingredients: List[Ingredient] # Nested list of Ingredient objects
    preparation: List[str]
    comment: str
    nutrition: NutritionInfo
    related: Optional[List[Tuple[str, str]]]
    # It's not really clear from the XML what 'related' should be, type-wise, so I went with my gut!
    # This is a list of recipe id/comment pairs, which is nullable by way of Optional.

    def __repr__(self) -> str:
        """For shorter testing output with helper.ut()."""
        return self.title