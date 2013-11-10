class Recipe:
    def __init__(self):
        self.ingredients = dict()

    def add(self, ingredient, measure):
        self.ingredients[ingredient] = measure

    def num_ingredients(self):
        return len(self.ingredients)

    def distance(self, other):
        allingredients = set(self.ingredients.keys() + other.ingredients.keys())
        accum = 0
        for ingredient in allingredients:
            if(ingredient in self.ingredients):
                if(ingredient in other.ingredients):
                    diff = abs(float(self.ingredients[ingredient]) - float(other.ingredients[ingredient]))
                    maxing = max(self.ingredients[ingredient], other.ingredients[ingredient])
                    accum += diff/maxing
                else:
                    accum += 1
            else:
            # because I just constructed the set from these two recipes, I know every ingredient is in one of them
                accum += 1
        return accum
    
