import requests
from bs4 import BeautifulSoup

from django_apps.recipes.services.recipe_title_scraper import (
    scrape_recipe_title,
)

from django_apps.recipes.services.recipe_image_scraper import (
    scrape_recipe_image_url,
)

from django_apps.recipes.services.recipe_source_scraper import (
    scrape_recipe_source_url,
    scrape_recipe_source_name,
)
from django_apps.recipes.services.recipe_servings_scraper import (
    scrape_recipe_servings_count,
)
from django_apps.recipes.services.recipe_author_scraper import (
    scrape_recipe_author,
)


def scrape_recipe(url):
    page = requests.get(url)
    soup_html = BeautifulSoup(page.content, 'html.parser')
    title = scrape_recipe_title(soup_html)
    image_url = scrape_recipe_image_url(soup_html)
    source_name = scrape_recipe_source_name(soup_html)
    source_url = scrape_recipe_source_url(soup_html)
    servings_count = scrape_recipe_servings_count(soup_html)
    author = scrape_recipe_author(soup_html)
