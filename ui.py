"""File: ui.py
Simple PyQt5 GUI for testing the functions. Intended entry point for the project.
Has a list to pick a function from, a box displaying the output,
and another to show the function source code."""
import re
import sys
# import inspect
# import PyQt5 as qt
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import repositories as rps
from design import Ui_Form

import locale
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

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

tests = (
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



    ui.functionList.addItems(
        list(map(
            lambda x: x[0],
            tests
        ))
    )

    recipes = rps.init_recipes()

    ui.functionList.currentRowChanged.connect(
        lambda x: ui.outputText.setText(
            tests[x][2](tests[x][1], recipes)
        )
    )


    Form.show()
    sys.exit(app.exec_())

    # app = QApplication([])
    # app.setStyle("Fusion")
    # app.setPalette(QApplication.style().standardPalette())
    #
    # window = QWidget()
    # window.setWindowTitle("Recipe Manager")
    # window.setGeometry(100, 100, 800, 600)
    #
    # layout = QVBoxLayout()
    #
    # # Create a list of functions
    # functions = QListWidget()
    # functions.addItems(["ut", "Recipe", "Ingredient", "NutritionInfo"])
    #
    # # Create a text box to display the output
    # output = QTextEdit()
    # output.setReadOnly(True)
    #
    # # Create a text box to display the function source code
    # source = QTextEdit()
    # source.setReadOnly(True)
    #
    # # Add the widgets to the layout
    # layout.addWidget(functions)
    # layout.addWidget(output)
    # layout.addWidget(source)
    #
    # # Set the layout for the window
    # window.setLayout(layout)
    #
    # # Show the window
    # window.show()
    # app.exec_()


