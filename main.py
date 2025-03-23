"""File: main.py
Simple PyQt5 GUI for testing the functions. Intended entry point for the project.
Has a list to pick a function from, a box displaying the output,
and another to show the function source code."""
import re
import sys
import inspect
import locale
from PyQt5.QtWidgets import *

import repositories as rps
from design import Ui_Form # Généré avec Qt Designer
from ut import *


# def get_functions():
#     attrs = list(map(
#         lambda x: getattr(repositories, x),
#         dir(repositories)
#     ))
#
#     functions = sorted(list(filter(
#         lambda attr: callable(attr) and attr.__module__ == repositories.__name__,
#         attrs
#     )),
#         key=lambda x: int(re.search(r"QUESTION (\d+)", inspect.getsource(x)).group(1))
#         if re.search(r"QUESTION (\d+)", inspect.getsource(x)) else float('inf')
#     )
#
#     return functions

instructions = """Sélectionnez une des fonctions dans la liste de gauche pour l'exécuter. La sortie sera affichée dans cette boîte. 

Vous pouvez aussi voir le code source de la fonction dans la boîte à droite. Elles sont toutes commentées (en anglais par convention). D'autres fonctions sont définies et utilisées, et visibles dans le fichier helper.py.

Toutes les fonctions sont numérotées avec le numéro de la question à laquelle elles répondent."""

tests = (
    ("---INSTRUCTIONS---", None, None),
    ("3. init_recipes", rps.init_recipes, lambda fn, rcp: fn()),
    ("4. get_recipe_titles", rps.get_recipe_titles, lambda fn, rcp: fn(rcp)),
    ("5. get_total_ingredient_count", rps.get_total_ingredient_count, lambda fn, rcp: fn(rcp, 'egg')),
    ("6. get_recipes_with_ingredient", rps.get_recipes_with_ingredient, lambda fn, rcp: fn(rcp, 'egg')),
    ("7. get_all_ingredient_counts", rps.get_all_ingredient_counts, lambda fn, rcp: fn(rcp, 'egg')),
    ("8. filter_under_calories", rps.filter_under_calories, lambda fn, rcp: fn(rcp, 500)),
    ("9. get_amount_str", rps.get_amount_str, lambda fn, rcp: fn(rps.get_recipe(rcp, "Zuppa Inglese"), "sugar")),
    ("10. get_prep_steps", rps.get_prep_steps, lambda fn, rcp: fn(rps.get_recipe(rcp, "Zuppa Inglese"), 0, 2)),
    ("11. filter_above_steps", rps.filter_above_steps, lambda fn, rcp: fn(rcp, 5)),
    ("12. filter_by_no_ingredient", rps.filter_by_no_ingredient, lambda fn, rcp: fn(rcp, 'butter')),
    ("13. get_similar_recipes", rps.get_similar_recipes, lambda fn, rcp: fn(rcp, rps.get_recipe(rcp, "Zuppa Inglese"))),
    ("14. max_calories", rps.max_calories, lambda fn, rcp: fn(rcp)),
    ("15. get_most_common_unit", rps.get_most_common_unit, lambda fn, rcp: fn(rcp)),
    ("16. get_diff_ingredient_count", rps.get_diff_ingredient_count, lambda fn, rcp: fn(rcp)),
    ("17. max_fat", rps.max_fat, lambda fn, rcp: fn(rcp)),
    ("18. get_most_common_ingredient", rps.get_most_common_ingredient, lambda fn, rcp: fn(rcp)),
    ("19. sort_by_ingredient_count", rps.sort_by_ingredient_count, lambda fn, rcp: fn(rcp)),
    ("20. get_recipes_with_ingredient", rps.get_recipes_with_ingredient, lambda fn, rcp: fn(rcp, 'beef')),
    ('21. get_recipe_repartition', rps.get_recipe_repartition, lambda fn, rcp: fn(rcp)),
    ('22. get_easiest_recipe', rps.get_easiest_recipe, lambda fn, rcp: fn(rcp)),
)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.setWindowTitle("Grégoire Brosset - Programmation Fonctionnelle - Projet recettes")

    # Populate test list
    ui.functionList.addItems(
        list(map(
            lambda x: x[0],
            tests
        ))
    )

    recipes = rps.init_recipes()
    print(recipes)


    def on_selection(self: int):
        """
        Slot; signaled by function list. Runs test corresponding to the selected entry.
        :param self: function list index
        """
        if self == 0: # Instructions
            ui.outputText.setText(instructions)
            ui.sourceText.setText("")
            return
        test = tests[self]
        ui.outputText.setText(ut_repr(test[2], test[1], recipes)) # Run the test
        ui.sourceText.setText(inspect.getsource(test[1]))

    ui.functionList.currentRowChanged.connect(on_selection)

    Form.show()
    sys.exit(app.exec_())