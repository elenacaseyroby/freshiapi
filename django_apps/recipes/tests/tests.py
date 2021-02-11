from django.test import TestCase
import requests
from bs4 import BeautifulSoup

from django_apps.recipes.services.recipe_title_scraper import (
    scrape_recipe_title,
)

# Create your tests here.

# To run:
# python manage.py test django_apps.recipes.tests.tests.ScrapeTitleTestCase


class ScrapeTitleTestCase(TestCase):
    def test_find_bon_appetit_title(self):
        url = 'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        title = scrape_recipe_title(soup_html)
        self.assertEqual(title, 'Seared Short Ribs With Mushrooms')

    def test_find_min_baker_title(self):
        url = 'https://minimalistbaker.com/easy-baked-cheesecake-vegan-gf/'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Easy Baked Cheesecake (Vegan + GF) | Minimalist Baker Recipes'
        )

    def test_find_dinner_at_the_zoo_title(self):
        url = 'https://www.dinneratthezoo.com/sesame-noodles/'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Sesame Noodles - Dinner at the Zoo'
        )

    def test_find_leites_title(self):
        url = 'https://leitesculinaria.com/80237/recipes-burrata-with-asparagus.html'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Burrata Cheese with Asparagus'
        )


# class ScrapeImageTestCase(TestCase):

    # class ScrapeSourceTestCase(TestCase):

    # class ScrapeServingsTestCase(TestCase):

    # class ScrapeTimeTestCase(TestCase):

    # class MatchIngredient(TestCase):

    # class MatchUnitTestCase(TestCase):

    # class MatchSourceTestCase(TestCase):

    # class ScrapeIngredientQty(TestCase):

    # class ScrapeIngredientUnit(TestCase):

    # class ScrapeIngredientsTestCase(TestCase):

    # class ScrapeIngredientsBySubgroupTestCase(TestCase):

    # class ScrapeDirectionsTestCase(TestCase):

    # class ScrapeDirectionsBySubgroupTestCase(TestCase):

    # class CalculateRecipeNutrients(TestCase):
    # mark incomplete if not all foods have nutrition facts

    # class LoginRequiredTestCase(TestCase):

    # class DynamicWebsiteTestCase(TestCase):

    # class ScrapeDietsTestCase(TestCase):

    # class ScrapeCuisinesTestCase(TestCase):

    # class ScrapeAllergensTestCase(TestCase):
