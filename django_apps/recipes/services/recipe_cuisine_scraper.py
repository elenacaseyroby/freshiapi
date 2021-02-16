def scrape_recipe_cuisine_wprm(soup_html):
    # <span class="wprm-recipe-cuisine">Cuisine</span>
    cuisine = None
    elements = soup_html.select('span[class*="wprm-recipe-cuisine "]')
    if len(elements) > 0:
        cuisine = elements[0].get_text().lower()
    return cuisine


def scrape_recipe_cuisine_tasty(soup_html):
    # <span class="tasty-recipes-label">Cuisine</span>
    cuisine = soup_html.find('span', {'class': 'tasty-recipes-label'})
    if cuisine:
        cuisine = cuisine.get_text().lower()
    return cuisine


def scrape_recipe_cuisine_mentioned(soup_html, all_cuisine_names):
    html_str = soup_html.get_text()
    for name in all_cuisine_names:
        if name in html_str:
            return name


def scrape_recipe_cuisines_meta(soup_html, all_cuisine_names):
    # <meta name="keywords" content="
    # recipes,appetizer,breakfast,brunch,
    # cocktail party,cottage cheese,pancake,
    # party,pea,green onion scallion,spring,spring pea,web">
    element = soup_html.find('meta', {'name': 'keywords'})
    if element:
        keywords = str(element['content']).lower().split(',')
        for keyword in keywords:
            if keyword.strip() in all_cuisine_names:
                return keyword
    return None


def scrape_recipe_cuisine(soup_html, all_cuisine_names):
    # First try plugins.
    cuisine = scrape_recipe_cuisine_wprm(soup_html)
    if not cuisine:
        cuisine = scrape_recipe_cuisine_tasty(soup_html)
    if cuisine in all_cuisine_names:
        return cuisine
    # Then try meta tags.
    cuisine = scrape_recipe_cuisines_meta(soup_html, all_cuisine_names)
    if cuisine:
        return cuisine
    # As a last resort, try to find cuisine name anywhere
    # on the page.
    cuisine = scrape_recipe_cuisine_mentioned(
        soup_html, all_cuisine_names)
    return cuisine
