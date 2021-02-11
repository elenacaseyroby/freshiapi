import requests
from bs4 import BeautifulSoup

from django_apps.recipes.services.recipe_title_scraper import (
    scrape_recipe_title,
)


def scrape_recipe(url):
    page = requests.get(url)
    soup_html = BeautifulSoup(page.content, 'html.parser')
    title = scrape_recipe_title(soup_html)
