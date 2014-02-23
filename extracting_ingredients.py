# I think there should be a recipe class: dict of ingredient -> measurement, list of verbs, function to compute distance
import os
import re
import json
import itertools
from fractions import Fraction
from recipe import Recipe

recipes = []
rdirs = ["pancakes"]
for rdir in rdirs:
    for filename in os.listdir(rdir):
        recipes.append(os.path.join(rdir,filename))

arecipe = recipes[0]

by_recipe = {}

ingredient_lines = set()

def parse_line(line):
    iparse = re.compile("\A\* ([\d\s/]*)(.*)")
    match = re.search(iparse, line)
    raw_meas = match.group(1)
    ingredient = match.group(2)
    return ingredient, clean_measure(raw_meas)

def clean_measure(raw):
    raw = raw.strip()
    bits = raw.split(" ")
    if "/" in bits[0]:
        bits[0] = float(Fraction(bits[0]))

    if len(bits) > 1 and "/" in bits[1]:
        return float(bits[0]) + float(Fraction(bits[1]))
    else:
        try: 
            return float(bits[0])
        except:
            return 1
         

for recipe in recipes:
    #print recipe
    by_recipe[recipe] = Recipe()
    f = open( recipe, "r")
    ingredient_block = False

    for line in f:
        line = line.strip()
        if ingredient_block and line != "":
            ingredient, measure = parse_line(line)
            by_recipe[recipe].add(ingredient, measure)
        if ingredient_block and by_recipe[recipe].num_ingredients() > 0 and line == "":
            break
        if line.startswith("Ingredients"):
            ingredient_block = True

# following http://bl.ocks.org/mbostock/4062045
#nodes = [{"name": i} for i in recipes]
nodes = []
for recipe in recipes:
    bits = recipe.split("/")
    nodes.append({"group": bits[0], "name": bits[1]}) 

indices = range(0, len(recipes))

links = []
for pair in itertools.combinations(indices, 2):
    recipex = recipes[pair[0]]
    recipey = recipes[pair[1]]
    value = by_recipe[recipex].distance(by_recipe[recipey])
    links.append({"source": pair[0], "target": pair[1], "value": value})


print json.dumps({"nodes":nodes, "links":links})
