"""File: repositories.py
Contains all functions demanded by the project description."""

import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime as dt

from helper import *
from ut import ut_print

import locale
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

def init_recipes(filename='recipes.xml', ns_prefix='rcp', ns_uri='http://www.brics.dk/ixwt/recipes'):
    """QUESTION 3: Import recipes from an XML file.
    Returns a dictionary of Recipe objects, indexed by their ID."""
    try:
        # XML namespace
        ns = {ns_prefix: ns_uri}

        tree = ET.parse(filename)
        ret = {}

        for recipe in tree.getroot().findall('rcp:recipe', ns):
            # Extract each field from the recipe
            title = recipe.find('rcp:title', ns).text

            rcpdate = dt.strptime(
                recipe.find('rcp:date', ns).text,
                "%a, %d %b %y"
            )

            ## Ingredient
            def parse_ingredients(ingredient):
                # Special handling for the ingredient amount
                amount = ingredient.attrib.get('amount', '*')
                if amount == '*':
                    amount = 0
                else:
                    amount = float(amount)

                preparation_elem = ingredient.find('rcp:preparation', ns)
                return Ingredient(
                    str(ingredient.attrib.get('name', None)),
                    amount,
                    str(ingredient.attrib.get('unit', None)),
                    list(map(
                        parse_ingredients,
                        ingredient.findall('rcp:ingredient', ns)
                    )),
                    list(map(
                        lambda x: x.text,
                        preparation_elem.findall('rcp:step', ns)
                    )) if preparation_elem is not None else None
                )

            ingredients = list(map(
                parse_ingredients,
                recipe.findall('rcp:ingredient', ns)
            ))

            preparation = list(map(
                lambda x: x.text,
                recipe.find('rcp:preparation', ns).findall('rcp:step', ns)
            ))

            comment_elem = recipe.find('rcp:comment', ns)
            comment = comment_elem.text if comment_elem is not None else None

            nutrition_elem = recipe.find('rcp:nutrition', ns)
            nutrition = NutritionInfo(
                float(nutrition_elem.attrib.get('calories')),
                float(nutrition_elem.attrib.get('fat').replace('%', '')),
                float(nutrition_elem.attrib.get('carbohydrates').replace('%', '')),
                float(nutrition_elem.attrib.get('protein').replace('%', ''))
            )

            related_elem = recipe.find('rcp:related', ns)
            related = (related_elem.attrib['ref'], related_elem.text) if related_elem is not None else None

            # Build dictionary
            ret[recipe.attrib['id']] = Recipe(
                title,
                rcpdate,
                ingredients,
                preparation,
                comment,
                nutrition,
                related
            )

        return ret
    except FileNotFoundError:
        print(f"Error importing recipes: {filename} file not found")
        return None


def get_recipe_titles(recipes: dict):
    """QUESTION 4: Get a list of recipe titles from a dictionary of Recipe objects."""
    return list(map(lambda x: x.title, recipes.values()))


def get_total_ingredient_count(recipes: dict, ing_name: str):
    """QUESTION 5: Get the total amount of a specific ingredient in all recipes."""
    return sum(map(
        lambda x: x.amount if ing_name in x.name else 0,
        flatten_ingredients(recipes)
    ))


def get_recipes_with_ingredient(recipes: dict, ing_name: str):
    """QUESTION 6: Get a list of recipes that contain a specific ingredient."""
    return list(filter(
        lambda x: any(map(  # If any ings in recipe contain ing_name
            lambda y: ing_name in y.name,
            flatten_ingredients(x.ingredients)
        )),
        recipes.values()
    ))


def get_all_ingredient_counts(recipes: dict, ing_name: str):
    """QUESTION 7: Get a dictionary with the count of a specific ingredient in all recipes."""
    return dict(zip(recipes.keys(),
                    map(lambda x: get_ingredient_count(x, ing_name), recipes.values())
                    ))


def filter_under_calories(recipes: dict, calories: float):
    """QUESTION 8: Get a list of recipes with less than a certain amount of calories."""
    return filter_recipes(recipes, lambda x: x.nutrition.calories < calories)


def get_amount_str(recipe: Recipe, ing_name):
    """QUESTION 9: Get a string with the amount and unit of a specific ingredient in a specific recipe."""
    # Get the unit.
    # We're assuming the XML always uses the same one for the same ingredient,
    # so we're just grabbing the first one.
    unit = next((i.unit for i in flatten_ingredients(recipe.ingredients) if ing_name in i.name))

    # ingredients = flatten_ingredients(recipe.ingredients)
    # matching_ingredients = [i for i in ingredients if ing_name in i.name]
    # for i in matching_ingredients:
    #     print(f"Matching ingredients: {i.name} {i.amount} ")

    return f"{ing_name} - {get_ingredient_count(recipe, ing_name)}{(" " + unit) if unit else ''}"


def get_prep_steps(recipe: Recipe, from_step: int = 0, to_step: int = None):
    """QUESTION 10: Get a list of preparation steps from a specific recipe."""
    return recipe.preparation[from_step:to_step]


def filter_above_steps(recipes: dict, steps: int):
    """QUESTION 11: Get a list of recipes with more than a certain number of steps."""

    def exceeds_step_count(recipe, steps):
        step_count = len(recipe.preparation)
        if step_count > steps:
            return True  # don't need to count the rest

        ingredients = flatten_ingredients(recipe.ingredients)
        ingredient_steps = sum(len(i.preparation) if i.preparation is not None else 0
                               for i in ingredients)
        return step_count + ingredient_steps > steps

    return filter_recipes(recipes, lambda recipe: exceeds_step_count(recipe, steps))


def filter_by_no_ingredient(recipes: dict, ingredient: str):
    """QUESTION 12: Get a list of recipes that do not contain a specific ingredient."""
    return filter_recipes(recipes, lambda x: not any(map(
        lambda y: ingredient in y.name,
        flatten_ingredients(x.ingredients)
    )))


"""Get recipes that share ingredients with a given recipe"""


def get_similar_recipes(recipes: dict, recipe1: Recipe):
    """QUESTION 13: Get a list of recipes that share ingredients with a given recipe."""
    ## Just to check if it works:
    # def dbg(x,y,z):
    #     ret=  z.name in y.name
    #     if ret:
    #         print(f"{x} shares {z.name} with {recipe1}")
    #     return ret

    return filter_recipes(recipes, lambda x: any(map(
        lambda y: any(map(
            lambda z: z.name in y.name,
            # lambda z: dbg(x,y,z),
            flatten_ingredients(recipe1.ingredients)
        )),
        flatten_ingredients(x.ingredients)
    )))


def max_calories(recipes: dict):
    """QUESTION 14: Get the recipe with the highest calorie count."""
    return max(recipes.values(), key=lambda x: x.nutrition.calories)


def get_most_common_unit(recipes: dict):
    """QUESTION 15: Get the most common unit used in all recipes."""
    c = Counter(map(lambda x: x.unit, flatten_ingredients(recipes)))
    c.pop('None')  # Remove the null value from the count, since we want actual units
    # The flaw of this approach is that you can't *not* count a value if you don't want to.
    return c.most_common(1)[0][0]


def get_diff_ingredient_count(recipes):
    """QUESTION 16: Get a list with the number of distinct ingredients in each recipe.
    Unlike other similar functions, this ignores amounts, since they're not comparable."""
    return list(map(
        lambda x: len(flatten_ingredients(x)),
        recipes.values()
    ))


def max_fat(recipes: dict):
    """QUESTION 17: Get the recipe with the highest fat content."""
    return max(recipes.values(), key=lambda x: x.nutrition.fat)


def get_most_common_ingredient(recipes: dict):
    """QUESTION 18: Get the most common ingredient used in all recipes."""
    c = Counter(map(lambda x: x.name, flatten_ingredients(recipes)))
    return c.most_common(1)[0][0]


def sort_by_ingredient_count(recipes: dict):
    """QUESTION 19: Sort recipes by the total amount of ingredients they contain."""
    ## To see if it works:
    # list(map(lambda x: print(f"{x}: {sum(map(lambda y: y.amount, flatten_ingredients(x.ingredients)))}"), recipes.values()))
    return sorted(recipes.values(),
                  key=lambda x: sum(map(lambda y: y.amount, flatten_ingredients(x.ingredients))),
                  reverse=True)  # desc


def get_ingredient_usages(recipes: dict):
    """QUESTION 20: Get a dictionary of ingredients and the recipes they are used in."""
    usages = defaultdict(lambda x: get_recipes_with_ingredient(recipes, x))

    ings = get_unique_ingredients(recipes)

    for ing in ings:
        usages[ing] = get_recipes_with_ingredient(recipes, ing)
    return usages


def get_recipe_repartition(recipes: dict):
    """QUESTION 21: Get a dictionary of the number of recipes with a specific number of steps."""
    # (Not sure I understood the question, hopefully this is alright)
    return Counter(map(lambda x: get_step_count(x), recipes.values()))


def get_easiest_recipe(recipes: dict):
    """QUESTION 22: Get the easiest recipe with the fewest steps."""
    return min(recipes.values(), key=lambda x: get_step_count(x))


# Unit testing
if __name__ == '__main__':
    recipes = ut_print(init_recipes)

    ut_print(get_recipe_titles, recipes)
    # ut(get_ingredient_count, recipes, 'egg')
    ut_print(get_total_ingredient_count, recipes, 'egg')
    ut_print(get_recipes_with_ingredient, recipes, 'olive oil')
    #ut(get_ingredient_count, get_recipes_with_ingredient(recipes, 'egg')[0], 'egg')
    ut_print(get_all_ingredient_counts, recipes, 'egg')
    ut_print(filter_under_calories, recipes, 500)
    ut_print(get_recipe, recipes, "Zuppa Inglese")
    ut_print(get_amount_str, get_recipe(recipes, "Zuppa Inglese"), "sugar")
    ut_print(get_prep_steps, get_recipe(recipes, "Zuppa Inglese"), 0, 2)
    ut_print(filter_above_steps, recipes, 5)
    ut_print(filter_by_no_ingredient, recipes, "butter")
    ut_print(get_similar_recipes, recipes, get_recipe(recipes, "Zuppa Inglese"))
    ut_print(max_calories, recipes)
    ut_print(get_most_common_unit, recipes)
    ut_print(max_fat, recipes)
    ut_print(get_most_common_ingredient, recipes)
    ut_print(sort_by_ingredient_count, recipes)
    ut_print(get_recipes_with_ingredient, recipes, 'beef')
    ut_print(get_recipe_repartition, recipes)
    ut_print(get_easiest_recipe, recipes)
    ut_print(get_diff_ingredient_count, recipes)
