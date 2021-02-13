import re

measurements = [
    'cup',
    'cups',
    'teaspoons',
    'teaspoon',
    'tablespoons',
    'tablespoon',
    'ounces',
]


def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


def get_servings(servings_str):
    # If servings is an amount and not a count
    # return None and calculate servings count
    # later in the script.
    servings_str = servings_str.lower()
    for measurement in measurements:
        if measurement in servings_str:
            return None
    # Remove number from the string
    match = re.findall('^\D*(\d*).*', servings_str)
    for group in match:
        try:
            servings_count = int(group)
            return servings_count
        except:
            return None
    return None


def scrape_servings_bon_appetit(soup_html):
    # <p class="sc-iBPRYJ sc-fubCfw sc-jToBAC eLRJRO eqsdQP hemvdP">
    # 4  Servings</p>
    servings_count = None
    servings_string = soup_html.find(
        'p', class_="sc-iBPRYJ sc-fubCfw sc-jExWIn eLRJRO eqsdQP dqUvnp")
    if servings_string:
        servings_string = servings_string.get_text()
        servings_count = servings_string.lower().replace(' servings', '')
    if servings_count:
        servings_count = int(servings_count)
    return servings_count


def scrape_servings_wprm(soup_html):
    # <span class="
    # wprm-recipe-servings
    # wprm-recipe-details
    # wprm-recipe-servings-29500
    # wprm-recipe-servings-adjustable-tooltip
    # wprm-block-text-normal"
    # data-recipe="29500"
    # aria-label="Adjust recipe servings"
    # data-servings="SERVINGS_COUNT"
    # data-original-servings="SERVINGS_COUNT">
    # SERVINGS_COUNT
    # </span>
    servings_count = None
    # Find all elements with "wprm-recipe-name" in class
    elements = soup_html.select('span[class*="wprm-recipe-servings "]')
    if len(elements) > 0:
        # If elements returned, set title to text of first element.
        servings_count = int(elements[0].get_text())
    return servings_count


def scrape_servings_leites(soup_html):
    # <span itemprop="recipeYield" class="yield">4</span>
    servings_count = None
    servings_string = soup_html.find(
        'span',
        {'itemprop': 'recipeYield'}
    )
    if servings_string:
        servings_count = int(servings_string.get_text())
    return servings_count


def scrape_servings_epicurious(soup_html):
    # <dd class="yield" itemprop="recipeYield">Makes about 100 dumplings</dd>
    servings_count = None
    servings_string = soup_html.find(
        'dd',
        {'itemprop': 'recipeYield'}
    )
    if servings_string:
        servings_count = get_servings(servings_string.get_text())
    return servings_count


def scrape_recipe_servings_count(soup_html):
    servings_count = scrape_servings_bon_appetit(soup_html)
    if not servings_count:
        servings_count = scrape_servings_wprm(soup_html)
    if not servings_count:
        servings_count = scrape_servings_leites(soup_html)
    return servings_count
