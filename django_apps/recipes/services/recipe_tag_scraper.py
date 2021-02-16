
def convert_category_name(name):
    category_conversions = {
        'main': 'dinner',
    }
    for conversion in category_conversions:
        if conversion in name:
            return category_conversions[conversion]
    return name


def scrape_recipe_categories_mentioned(soup_html, all_category_names):
    html_str = soup_html.get_text()
    category_names = []
    for name in category_names:
        if name not in html_str:
            continue
        category_names.append(name)
    # If contradictory meals are mentioned, then
    # it is probably pulling them from a menu
    # and they are not specific to the recipe.
    # In this case, clear the list.
    if (
        'breakfast' in category_names and
        'dinner' in category_names
    ):
        return []

    if (
        'dessert' in category_names and
        'dinner' in category_names
    ):
        return []

    return category_names


def scrape_recipe_category_wprm(soup_html):
    # <span class="wprm-recipe-course wprm-block-text-normal">Salad</span>
    category = None
    elements = soup_html.select('span[class*="wprm-recipe-course "]')
    if len(elements) > 0:
        category_name = elements[0].get_text().lower()
        category = convert_category_name(category_name)
    return category


def scrape_recipe_category_tasty(soup_html):
    # <span data-tasty-recipes-customization="detail-value-color.color"
    # class="tasty-recipes-category">Appetizer</span>
    category = soup_html.find('span', {'class': 'tasty-recipes-category'})
    if category:
        category_name = category.get_text().lower()
        category = convert_category_name(category_name)
    return category


def scrape_recipe_categories_meta(soup_html):
    # <meta name="keywords" content="
    # recipes,appetizer,breakfast,brunch,
    # cocktail party,cottage cheese,pancake,
    # party,pea,green onion scallion,spring,spring pea,web">
    categories = []
    element = soup_html.find('meta', {'name': 'keywords'})
    if element:
        categories = str(element['content']).lower().split(',')
    return categories


def scrape_recipe_categories(soup_html, all_category_names):
    category_names = []
    # Get one category from plugin
    category = scrape_recipe_category_wprm(soup_html)
    if not category:
        category = scrape_recipe_category_tasty(soup_html)
    # Get many categories from meta data tags:
    categories = scrape_recipe_categories_meta(soup_html)
    # Compile categories so far:
    if category:
        categories.append(category)
    # Filter out category names not in our db.
    category_names = [
        name.strip() for name in categories
        if name.strip() in all_category_names
    ]
    # As a last resort, check for mentions of any category
    # anywhere on the page.
    if len(category_names) == 0:
        category_names = scrape_recipe_categories_mentioned(
            soup_html, all_category_names)
    return category_names


def scrape_recipe_diets(html_str, all_diet_names):
    diet_names = []
    return diet_names


def scrape_recipe_allergens(html_str, all_allergy_names):
    allergy_names = []
    return allergy_names


def scrape_recipe_cuisines(html_str, all_cuisine_names):
    cuisine_names = []
    return cuisine_names
