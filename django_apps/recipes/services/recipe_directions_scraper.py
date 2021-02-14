from bs4 import BeautifulSoup


def scrape_directions_wprm(soup_html):
    directions = []
    elements = soup_html.select('.wprm-recipe-instruction-text')
    for element in elements:
        directions.append(element.get_text())
    return directions


def scrape_directions_step(soup_html):
    directions = []
    elements = soup_html.select('li[id*="instruction-step"]')
    for element in elements:
        # If elements returned, set title to text of first element.
        directions.append(element.get_text())
    return directions


def scrape_directions_bon_appetit(soup_html):
    directions = []
    container = soup_html.find(
        'div', {'data-testid': 'InstructionsWrapper'})
    container = str(container)
    soup_html = BeautifulSoup(container, 'html.parser')
    direction_texts = soup_html.select('p')
    for direction in direction_texts:
        directions.append(direction.get_text())
    return directions


def scrape_recipe_directions(soup_html):
    directions = scrape_directions_wprm(soup_html)
    if len(directions) == 0:
        directions = scrape_directions_step(soup_html)
    if len(directions) == 0:
        directions = scrape_directions_bon_appetit(soup_html)
    return directions
