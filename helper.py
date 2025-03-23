""" File: helper.py
This file contains helper functions that are used in the main program."""

from functools import reduce

from models import *


def flatten_ingredients(container):
    """HELPER: Flattens a list of ingredients, for MUCH easier iteration when hierarchy isn't relevant"""
    ingredients = []
    if isinstance(container, dict):  # Is this the recipes dict?
        ingredients.extend(
            reduce(lambda acc, recipe: acc + flatten_ingredients(recipe.ingredients),
                   container.values(), [])
        )
    elif isinstance(container, list):
        ingredients.extend(
            reduce(lambda acc, ingredient: acc + flatten_ingredients(ingredient),
                   container, [])
        )
    elif isinstance(container, Recipe):
        ingredients.extend(container.ingredients)
        if container.ingredients:
            ingredients.extend(flatten_ingredients(container.ingredients))
    elif isinstance(container, Ingredient):
        ingredients.append(container)
        # Add any nested ingredients
        if container.ingredients:
            ingredients.extend(flatten_ingredients(container.ingredients))
    return ingredients


def get_ingredient_count(recipe: Recipe, ing_name: str):
    """HELPER: Get the total amount of a specific ingredient in a specific recipe."""
    return sum(map(
        lambda x: x.amount if ing_name in x.name else 0,
        flatten_ingredients(recipe.ingredients)
    ))


def filter_recipes(recipes: dict, filter_func):
    """HELPER: Filter recipes based on a given function."""
    return list(filter(filter_func, recipes.values()))


def get_step_count(recipe: Recipe):
    """HELPER: Get the total number of steps in a recipe."""
    overall_steps = len(recipe.preparation)
    ingredients = flatten_ingredients(recipe.ingredients)
    ingredient_steps = sum(len(i.preparation) if i.preparation is not None else 0
                           for i in ingredients)
    return overall_steps + ingredient_steps


def get_recipe(recipes: dict, title: str):
    """HELPER: Get a recipe by its title."""
    return next(filter(lambda x: x.title == title, recipes.values()), None)


def get_unique_ingredients(recipes):
    """HELPER: Get a set of all unique ingredients in all recipes."""
    return set(flatten_ingredients(recipes))
