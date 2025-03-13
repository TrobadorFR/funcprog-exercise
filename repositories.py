import xml.etree.ElementTree as ET
from datetime import datetime as dt
from functools import reduce
from pprint import pprint

from models import *
from helper import ut


# class RecipesXMLImporter:
#     """Imports all recipes from an XML file into a Recipe object collection"""
#     def __init__(self, filename = 'recipes.xml'):
#         self.tree: ET = ET.parse(filename)

def parse_ingredients(ingredient):


def init_recipes(filename='recipes.xml'):
    try:
        tree = ET.parse(filename)
        ret = {}
        ns = {'rcp': 'http://www.brics.dk/ixwt/recipes'}

        for recipe in tree.getroot().findall('rcp:recipe', ns):
            title = recipe.find('rcp:title', ns).text

            date = dt.strptime(
                recipe.find('rcp:date', ns).text,
                "%a, %d %b %y"
            )

            ## Ingredient
            # TODO: Handle nested ingredients.
            # Put code in get_ingredients and call it with the root ingredient.
            # I'll need a way to get only the direct children ingredients.
            # Maybe XPath?
            # End result should be nested list with Ingredient as the leaves.
            # Use recursivity... somehow.
            def keep_number(x):
                return x if x.isdigit() else '0'

            ingredients = list(map(
                lambda x: Ingredient(
                    str(x.attrib.get('name', None)),
                    float(keep_number(x.attrib.get('amount', '*'))),
                    str(x.attrib.get('unit', None))
                ),
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
                date,
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

def get_recipe_titles(recipes : dict):
    return list(map(lambda x: x.title, recipes.values()))

def get_ingredient_count(recipes : dict, ingredient : str):
    return sum(map(
        lambda x: sum(map(
            lambda y: y.amount if ingredient in y.name else 0
        , x.ingredients))
    , recipes.values()))

if __name__ == '__main__':
    recipes = ut(init_recipes)
    ut(get_recipe_titles, recipes)
    ut(get_ingredient_count, recipes, 'egg')


# I just realized there are some ingredients that are nested in the xml
# which is going to make the model and import more complex