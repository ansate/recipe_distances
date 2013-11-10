# I think there should be a recipe class: dict of ingredient -> measurement, list of verbs, function to compute distance
import os
import re
import json
from fractions import Fraction
from recipe import Recipe

recipes = os.listdir("ccc")

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
        return float(bits[0])
         

for recipe in recipes:
    by_recipe[recipe] = Recipe()
    f = open("ccc/" +recipe, "r")
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
nodes = [{"name": i} for i in recipes]

recipes = recipes[1:]

target = 0
source = 1
links = []
for recipe in recipes:
    #print recipe
    #value = int(by_recipe[arecipe].distance(by_recipe[recipe])*100)
    value = by_recipe[arecipe].distance(by_recipe[recipe])
    #print value
    links.append({"source": source, "target": target, "value": value})
    source = source + 1

print json.dumps({"nodes":nodes, "links":links})
