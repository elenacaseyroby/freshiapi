from bs4 import BeautifulSoup


def scrape_ingredients_bon_appetit(soup_html):
    ingredients = []
    ingredients_container = soup_html.select(
        'div[class*="recipe__ingredient-list"]')
    if ingredients_container:
        ingredients_container = str(ingredients_container)
        soup_html = BeautifulSoup(ingredients_container, 'html.parser')
        items = soup_html.select('.sc-iBPRYJ')
        ingredient = ""
        for item in items:
            item_text = item.get_text()
            if (
                'servings' in item_text.lower() or
                'ingredients' in item_text.lower()
            ):
                continue
            ingredient = f'{ingredient} {item_text}'
            # qty in <p> and ingredient in <div>
            # if div add ingredient to list and clear for next round
            if '<div' in str(item):
                ingredients.append(ingredient.strip())
                ingredient = ""
    return ingredients


def scrape_ingredients_oh_she_glows(soup_html):
    ingredients = []
    elements = soup_html.select('.ingredients .ingredient')
    for element in elements:
        ingredients.append(element.get_text())
    return ingredients


def scrape_ingredients_wprm(soup_html):
    # <li class="wprm-recipe-ingredient">
    # <span class="wprm-recipe-ingredient-amount">3</span>
    # <span class="wprm-recipe-ingredient-unit">tablespoons</span>
    # <span class="wprm-recipe-ingredient-name">extra virgin olive oil</span>
    ingredients = []
    elements = soup_html.select('.wprm-recipe-ingredient')
    for el in elements:
        ingredients.append(el.get_text().replace('\n', ' ').strip())
    return ingredients


def scrape_ingredients_jetpack(soup_html):
    # <li
    # class="jetpack-recipe-ingredient
    # p-ingredient ingredient"
    # itemprop="recipeIngredient">1 small yellow onion</li>
    ingredients = []
    elements = soup_html.select('.jetpack-recipe-ingredient')
    for el in elements:
        ingredients.append(el.get_text())
    return ingredients


def scrape_ingredients_tasty(soup_html):
    # <div class="tasty-recipe-ingredients">
    # <ul><li><span data-amount="1"
    # data-unit="cup">1 cup</span>other text</li></ul>
    # </div>
    ingredients = []
    elements = soup_html.select('.tasty-recipe-ingredients')
    for el in elements:
        ingredients.append(el.get_text().replace('\n', ' ').strip())
        print(el.get_text().replace('\n', ' ').strip())
    return ingredients


def scrape_ingredients(soup_html):
    # <div class="tasty-recipe-ingredients">
    # <ul><li><span data-amount="1"
    # data-unit="cup">1 cup</span>other text</li></ul>
    # </div>
    ingredients = []
    elements = soup_html.select('.ingredient')
    for el in elements:
        ingredients.append(el.get_text())
    return ingredients


def scrape_recipe_ingredients(soup_html):
    ingredients = scrape_ingredients_oh_she_glows(soup_html)
    if len(ingredients) == 0:
        ingredients = scrape_ingredients_bon_appetit(soup_html)
    if len(ingredients) == 0:
        ingredients = scrape_ingredients_wprm(soup_html)
    if len(ingredients) == 0:
        ingredients = scrape_ingredients(soup_html)
    if len(ingredients) == 0:
        ingredients = scrape_ingredients_jetpack(soup_html)
    if len(ingredients) == 0:
        ingredients = scrape_ingredients_tasty(soup_html)
    return ingredients
