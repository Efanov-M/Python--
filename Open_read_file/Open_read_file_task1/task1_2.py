# Должен получится следующий словарь
# cook_book ={'Омлет':[{'ingredient_name':'Яйцо','quantity':2,'measure':'шт.'},{'ingredient_name':'Молоко','quantity':100,'measure':'мл'},{'ingredient_name':'Помидор','quantity':2,'measure':'шт'}],
# 'Утка по-пекински':[{'ingredient_name':'Утка','quantity':1,'measure':'шт'},
# {'ingredient_name':'Вода','quantity':2,'measure':'л'},{'ingredient_name':'Мед','quantity':3,'measure':'ст.л'},{'ingredient_name':'Соевый соус','quantity':60,'measure':'мл'}],
# 'Запеченный картофель':[{'ingredient_name':'Картофель','quantity':1,'measure':'кг'},{'ingredient_name':'Чеснок','quantity':3,'measure':'зубч'},{'ingredient_name':'Сыр гауда',
# 'quantity':100,'measure':'г'},]}


class Ingredient:

    def __init__(self, name, quantity, measure):
        self.name = name
        self.quantity = quantity
        self.measure = measure

    def to_dict(self):
        return {
            "ingredient_name": self.name,
            "quantity": self.quantity,
            "measure": self.measure
        }


class Recipe:

    def __init__(self, name,):
        self.name = name
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def to_list(self):
        result = []
        for ingredient in self.ingredients:
            result.append(ingredient.to_dict())
        return result



class CookBook:

    def __init__(self):
        self.recipes = {}

    def add_recipe(self, recipe):
        self.recipes[recipe.name] = recipe

    def to_dict(self):
        result = {}
        for name, recipe in self.recipes.items():
            result[name] = recipe.to_list()
        return result

with open("recipes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

i = 0
book = CookBook()
while i < len(lines):
    recipe_name = lines[i].strip()
    i += 1
    recipe_name = Recipe(recipe_name)

    ingredient_count = int(lines[i].strip())
    i += 1
    for _ in range(ingredient_count):
        line = lines[i].strip()
        name, quantity, measure = line.split('|')

        ingredient = Ingredient(name.strip(),int(quantity.strip()),measure.strip())

        recipe_name.add_ingredient(ingredient)
        i += 1

    book.add_recipe(recipe_name)



    if i < len(lines) and lines[i].strip() == "":
        i += 1
# book_cook = book.to_dict()
# print(book_cook)



def get_shop_list_by_dishes(book, dishes, person_count):
    shop_list = {}

    for dish_name in dishes:
        recipe = book.recipes[dish_name]

        for ingredient in recipe.ingredients:
            name = ingredient.name
            measure = ingredient.measure
            quantity = ingredient.quantity * person_count

            if name not in shop_list:
                shop_list[name] = {
                    'measure': measure,
                    'quantity': quantity
                }
            else:
                shop_list[name]['quantity'] += quantity
    # print(f'Для корпоратива нужно : {shop_list}')
    return shop_list


# get_shop_list_by_dishes(book, ['Омлет', 'Фахитос'], 5)





