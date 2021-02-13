def scrape_directions_wprm(soup_html):
    directions = []
    elements = soup_html.select('.wprm-recipe-instruction-text')
    for element in elements:
        directions.append(element.get_text())
        print(element.get_text())
    return directions


def scrape_directions_step(soup_html):
    directions = []
    elements = soup_html.select('li[id*="instruction-step"]')
    for element in elements:
        # If elements returned, set title to text of first element.
        directions.append(element.get_text())
    return directions


def scrape_recipe_directions(soup_html):
    directions = scrape_directions_wprm(soup_html)
    if len(directions) == 0:
        directions = scrape_directions_step(soup_html)
    return directions
