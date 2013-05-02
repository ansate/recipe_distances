# I think there should be a recipe class: dict of ingredient -> measurement, list of verbs, function to compute distance
import os
from recipe import Recipe

recipes = os.listdir("ccc")

arecipe = recipes[0]


by_recipe = {}

ingredient_lines = set()

for recipe in recipes:
    by_recipe[recipe] = Recipe()
    f = open("ccc/" +recipe, "r")
    ingredient_block = False

    for line in f:
        line = line.strip()
        if ingredient_block and line != "":
            by_recipe[recipe].add(line, 1)
        if ingredient_block and by_recipe[recipe].num_ingredients() > 0 and line == "":
            break
        if line.startswith("Ingredients"):
            ingredient_block = True

print by_recipe[arecipe].ingredients
for recipe in by_recipe.keys():
    print recipe
    print by_recipe[arecipe].distance(by_recipe[recipe])

