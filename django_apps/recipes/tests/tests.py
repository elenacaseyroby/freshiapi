from django.test import TestCase
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


def get_soup_html(url):
    page = requests.get(url)
    soup_html = BeautifulSoup(page.content, 'html.parser')
    return soup_html


# To run:
# python manage.py test django_apps.recipes.tests.tests.ScrapeTitleTestCase
class ScrapeTitleTestCase(TestCase):
    def test_find_bon_appetit_title(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms')
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title, 'Seared Short Ribs With Mushrooms Recipe | Bon Appétit')

    def test_find_min_baker_title(self):
        soup_html = get_soup_html(
            'https://minimalistbaker.com/easy-baked-cheesecake-vegan-gf/'
        )
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Easy Baked Cheesecake (Vegan + GF)'
        )

    def test_find_dinner_at_the_zoo_title(self):
        url = 'https://www.dinneratthezoo.com/sesame-noodles/'
        page = requests.get(url)
        soup_html = BeautifulSoup(page.content, 'html.parser')
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Sesame Noodles'
        )

    def test_find_leites_title(self):
        soup_html = get_soup_html(
            'https://leitesculinaria.com/80237/recipes-burrata-with-asparagus.html'
        )
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Burrata Cheese with Asparagus'
        )

    def test_find_food_title(self):
        soup_html = get_soup_html(
            'https://www.food.com/recipe/chili-lime-cumin-cod-131528'
        )
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Chili, Lime & Cumin Cod Recipe  - Food.com'
        )

    def test_find_epicurious_title(self):
        soup_html = get_soup_html(
            'https://www.epicurious.com/recipes-menus/sohui-kim-lunar-new-year-menu-korean-article'
        )
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'Sohui Kim’s Lunar New Year Menu: Silky Pork Dumplings, Good Luck Soup, and a Big Bowl of Kimchi | Epicurious'
        )

    def test_find_smitten_kitchen_title(self):
        soup_html = get_soup_html(
            'https://smittenkitchen.com/2020/05/simple-essential-bolognese/'
        )
        title = scrape_recipe_title(soup_html)
        self.assertEqual(
            title,
            'simple, essential bolognese'
        )


class ScrapeImageTestCase(TestCase):
    def test_find_bon_appetit_image(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://assets.bonappetit.com/photos/5ff8aaf6a2c5a800b6a67ef0/16:9/w_1280,c_limit/Family-Meal-Short-Ribs.jpg')

    def test_find_min_baker_image(self):
        soup_html = get_soup_html(
            'https://minimalistbaker.com/easy-baked-cheesecake-vegan-gf/'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://minimalistbaker.com/wp-content/uploads/2016/03/BAKED-Vegan-Gluten-Free-Cheesecake-made-in-the-BLENDER-vegan-glutenfree-cheesecake-recipe.jpg')

    def test_find_dinner_at_the_zoo_image(self):
        soup_html = get_soup_html(
            'https://www.dinneratthezoo.com/sesame-noodles/'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://www.dinneratthezoo.com/wp-content/uploads/2020/08/sesame-noodles-4.jpg')

    def test_find_leites_image(self):
        soup_html = get_soup_html(
            'https://leitesculinaria.com/80237/recipes-burrata-with-asparagus.html'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://s23991.pcdn.co/wp-content/uploads/2019/04/burrata-asparagus-pine-nuts-raisins-fp.jpg.optimal.jpg')

    def test_find_epicurious_image(self):
        soup_html = get_soup_html(
            'https://www.epicurious.com/recipes-menus/sohui-kim-lunar-new-year-menu-korean-article'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url, 'https://assets.epicurious.com/photos/6010782823e2f349f099cd0b/16:9/w_1280,c_limit/PorkTofuDumpling_HERO_012521_328_VOG_final.jpg')

    def test_find_smitten_kitchen_image(self):
        soup_html = get_soup_html(
            'https://smittenkitchen.com/2020/05/simple-essential-bolognese/'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url,
            'https://i1.wp.com/smittenkitchen.com/wp-content/uploads/2020/05/IMG_5632-scaled.jpg?fit=1200%2C800&ssl=1'
        )

    def test_find_budget_bytes_image(self):
        soup_html = get_soup_html(
            'https://www.budgetbytes.com/mediterranean-tuna-salad/'
        )
        image_url = scrape_recipe_image_url(soup_html)
        self.assertEqual(
            image_url,
            'https://www.budgetbytes.com/wp-content/uploads/2021/02/Mediterranean-Tuna-Salad-side.jpg'
        )


class ScrapeSourceTestCase(TestCase):

    def test_find_bon_appetit_source_name(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        )
        source_name = scrape_recipe_source_name(soup_html)
        self.assertEqual(
            source_name,
            'Bon Appétit'
        )

    def test_find_bon_appetit_source_url(self):
        url = 'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        source_url = scrape_recipe_source_url(url)
        self.assertEqual(
            source_url,
            'bonappetit.com'
        )


class ScrapeServingsTestCase(TestCase):

    def test_find_bon_appetit_servings_count(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            4
        )

    def test_find_wordpress_recipe_maker_servings_count(self):
        soup_html = get_soup_html(
            'https://minimalistbaker.com/easy-baked-cheesecake-vegan-gf/'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            8
        )

    def test_find_dinner_at_zoo_servings_count(self):
        soup_html = get_soup_html(
            'https://www.dinneratthezoo.com/sesame-noodles/'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            4
        )

    def test_find_leites_servings_count(self):
        soup_html = get_soup_html(
            'https://leitesculinaria.com/80237/recipes-burrata-with-asparagus.html'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            4
        )

    def test_website_with_different_yield_count(self):
        soup_html = get_soup_html(
            'https://www.foodandwine.com/recipes/old-fashioned-banana-bread'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            None
        )


class ScrapeAuthorTestCase(TestCase):

    def test_find_bon_appetit_author(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        )
        author = scrape_recipe_author(soup_html)
        self.assertEqual(
            author,
            'Molly Baz'
        )

    def test_find_epicurious_author(self):
        soup_html = get_soup_html(
            'https://www.epicurious.com/recipes/food/views/pork-and-chive-dumplings-sohui-kim'
        )
        author = scrape_recipe_author(soup_html)
        self.assertEqual(
            author,
            'Sohui Kim'
        )

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
