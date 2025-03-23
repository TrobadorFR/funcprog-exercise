""" File: helper.py
This file contains helper functions that are used in the main program."""

from functools import reduce

from models import *


def flatten_ingredients(container):
    """
    HELPER: Flattens a list of ingredients, for MUCH easier iteration when hierarchy isn't relevant.
    This saves us having to implement recursion into everything else.
    Note that this does not remove references to composing ingredients from ingredient objects.
    :param container: any type that contains ingredients anywhere in its structure
    :return: list of all ingredients in the structure
    """
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
    """
    HELPER: Get the total amount of a specific ingredient in a specific recipe.
    This takes in account ingredient amount.
    :param recipe: Recipe object
    :param ing_name: ingredient name substring
    :return: amount of ingredient in recipe
    """
    return sum(map(
        lambda x: x.amount if ing_name in x.name else 0,
        flatten_ingredients(recipe.ingredients)
    ))


def filter_recipes(recipes: dict, filter_func):
    """
    HELPER: Filter recipes based on a given function.
    :param recipes: recipes dict
    :param filter_func: callable by which to filter recipes
    :return: list of recipes that pass the filter
    """
    return list(filter(filter_func, recipes.values()))


def get_step_count(recipe: Recipe):
    """
    HELPER: Get the total number of steps in a recipe.
    :param recipe: Recipe object
    :return: int steps count
    """
    overall_steps = len(recipe.preparation)
    ingredients = flatten_ingredients(recipe.ingredients)
    ingredient_steps = sum(len(i.preparation) if i.preparation is not None else 0
                           for i in ingredients)
    return overall_steps + ingredient_steps


def get_recipe(recipes: dict, title: str):
    """
    HELPER: Get a recipe by its title.
    Note: unlike with ingredients, title has to be exact.
    :param recipes: recipes dict
    :param title: EXACT title of recipe
    :return: Recipe object or None
    """
    return next(filter(lambda x: x.title == title, recipes.values()), None)


def get_unique_ingredients(recipes):
    """
    HELPER: Get a set of all unique ingredients in all recipes.
    :param recipes: recipes dict
    :return: set of Ingredient objects
    """
    return set(flatten_ingredients(recipes))
