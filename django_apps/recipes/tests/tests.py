from django.test import TestCase
import requests
from bs4 import BeautifulSoup

from django_apps.recipes.services.recipe_title_scraper import (
    scrape_recipe_title,
)

from django_apps.recipes.services.recipe_image_scraper import (
    scrape_recipe_image_url,
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


class ScrapeImageTestCase(TestCase):
    def test_find_bon_appetit_image(self):
        url = 'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://assets.bonappetit.com/photos/5ff8aaf6a2c5a800b6a67ef0/16:9/w_1280,c_limit/Family-Meal-Short-Ribs.jpg')

    def test_find_min_baker_image(self):
        url = 'https://minimalistbaker.com/easy-baked-cheesecake-vegan-gf/'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://minimalistbaker.com/wp-content/uploads/2016/03/BAKED-Vegan-Gluten-Free-Cheesecake-made-in-the-BLENDER-vegan-glutenfree-cheesecake-recipe.jpg')

    def test_find_dinner_at_the_zoo_image(self):
        url = 'https://www.dinneratthezoo.com/sesame-noodles/'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://www.dinneratthezoo.com/wp-content/uploads/2020/08/sesame-noodles-4.jpg')

    def test_find_leites_image(self):
        url = 'https://leitesculinaria.com/80237/recipes-burrata-with-asparagus.html'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://s23991.pcdn.co/wp-content/uploads/2019/04/burrata-asparagus-pine-nuts-raisins-fp.jpg.optimal.jpg')

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
