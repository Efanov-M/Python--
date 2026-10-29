# Должен получится следующий словарь
# cook_book ={'Омлет':[{'ingredient_name':'Яйцо','quantity':2,'measure':'шт.'},{'ingredient_name':'Молоко','quantity':100,'measure':'мл'},{'ingredient_name':'Помидор','quantity':2,'measure':'шт'}],
# 'Утка по-пекински':[{'ingredient_name':'Утка','quantity':1,'measure':'шт'},
# {'ingredient_name':'Вода','quantity':2,'measure':'л'},{'ingredient_name':'Мед','quantity':3,'measure':'ст.л'},{'ingredient_name':'Соевый соус','quantity':60,'measure':'мл'}],
# 'Запеченный картофель':[{'ingredient_name':'Картофель','quantity':1,'measure':'кг'},{'ingredient_name':'Чеснок','quantity':3,'measure':'зубч'},{'ingredient_name':'Сыр гауда',
# 'quantity':100,'measure':'г'},]}


class Ingredient:
    """
    Класс Ingredient описывает один ингредиент рецепта.

    Хранит:
    - название ингредиента
    - количество
    - единицу измерения

    Используется как элемент рецепта.
    """

    def __init__(self, name, quantity, measure):
        """
        Создаёт объект ингредиента.

        :param name: Название ингредиента (строка)
        :param quantity: Количество ингредиента (целое число)
        :param measure: Единица измерения (строка)
        """
        self.name = name
        self.quantity = quantity
        self.measure = measure

    def to_dict(self):
        """
        Преобразует объект ингредиента в словарь.

        Используется для формирования итоговой структуры cook_book.

        :return: dict вида:
                 {
                     "ingredient_name": <название>,
                     "quantity": <количество>,
                     "measure": <единица измерения>
                 }
        """
        return {
            "ingredient_name": self.name,
            "quantity": self.quantity,
            "measure": self.measure
        }


class Recipe:
    """
    Класс Recipe описывает один рецепт блюда.

    Содержит:
    - название блюда
    - список ингредиентов (объекты Ingredient)
    """

    def __init__(self, name,):
        """
         Создаёт объект рецепта.

        :param name: Название блюда (строка)
        """
        self.name = name
        self.ingredients = []

    def add_ingredient(self, ingredient):
        """
        Добавляет ингредиент в рецепт.

        :param ingredient: Объект класса Ingredient
        """
        self.ingredients.append(ingredient)

    def to_list(self):
        """
        Преобразует рецепт в список словарей ингредиентов.

        Каждый ингредиент конвертируется через ingredient.to_dict().

        :return: список словарей ингредиентов
        """
        result = []
        for ingredient in self.ingredients:
            result.append(ingredient.to_dict())
        return result



class CookBook:
    """
    Класс CookBook представляет сборник рецептов.

    Хранит рецепты в виде словаря:
    {
        "Название блюда": объект Recipe
    }
    """

    def __init__(self):
        """
        Создаёт пустую кулинарную книгу.
        """
        self.recipes = {}

    def add_recipe(self, recipe):
        """
        Добавляет рецепт в кулинарную книгу.

        :param recipe: Объект класса Recipe
        """
        self.recipes[recipe.name] = recipe

    def to_dict(self):
        """
        Преобразует всю кулинарную книгу в словарь формата cook_book.

        :return: dict вида:
                 {
                     "Название блюда": [список ингредиентов],
                     ...
                 }
        """
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
    """
    Формирует список покупок на основе выбранных блюд и количества персон.

    Для каждого блюда:
    - берёт ингредиенты
    - умножает количество на person_count
    - суммирует одинаковые ингредиенты

    :param book: Объект CookBook
    :param dishes: Список названий блюд (list[str])
    :param person_count: Количество человек (int)

    :return: dict вида:
             {
                 "Название ингредиента": {
                     "measure": <единица измерения>,
                     "quantity": <общее количество>
                 },
                 ...
             }
    """
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





