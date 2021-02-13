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

from django_apps.recipes.services.recipe_description_scraper import (
    scrape_recipe_description,
)

from django_apps.recipes.services.recipe_ingredient_scraper import (
    scrape_recipe_ingredients,
)

from django_apps.recipes.services.recipe_directions_scraper import (
    scrape_recipe_directions,
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
            'https://www.bonappetit.com/recipe/chocolate-biscoff-banoffee-pie')
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

    def test_epicurious_yield_count(self):
        soup_html = get_soup_html(
            'https://www.epicurious.com/recipes/food/views/pork-and-chive-dumplings-sohui-kim'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            100
        )

    def test_smitten_kitchen_yield_count(self):
        soup_html = get_soup_html(
            'https://smittenkitchen.com/2015/09/broccoli-cheddar-soup/'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            4
        )

    def test_tasty_servings_count(self):
        soup_html = get_soup_html(
            'https://cookieandkate.com/best-granola-bars-recipe/'
        )
        servings_count = scrape_recipe_servings_count(soup_html)
        self.assertEqual(
            servings_count,
            16
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


class ScrapeDescriptionTestCase(TestCase):

    def test_find_bon_appetit_desc(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc,
            'When we crave beef but don’t want a capital-S steak, we opt for a smaller cut (hello, short ribs!), then pile on lots of meaty mushrooms.'
        )

    def test_find_dinner_at_zoo_desc(self):
        soup_html = get_soup_html(
            'https://www.dinneratthezoo.com/sesame-noodles/'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc,
            'These sesame noodles are Asian noodles tossed in a savory peanut and sesame sauce. A quick and easy meal option!'
        )

    def test_find_leites_desc(self):
        soup_html = get_soup_html(
            'https://leitesculinaria.com/80237/recipes-burrata-with-asparagus.html'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc,
            "This burrata with asparagus dish is a quick and easy appetizer that's made with burrata cheese, asparagus, raisins, pine nuts, and prosciutto."
        )

    def test_food_and_wine_desc(self):
        soup_html = get_soup_html(
            'https://www.foodandwine.com/recipes/old-fashioned-banana-bread'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc,
            'This old-fashioned banana bread is from Lisa Ritter of Los Angeles&rsquo;s Big Sugar Bakeshop. The moist center and crisp crust has been a family hit for generations.'
        )

    def test_epicurious_desc(self):
        soup_html = get_soup_html(
            'https://www.epicurious.com/recipes/food/views/pork-and-chive-dumplings-sohui-kim'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc[:116],
            'Once you are on a national TV show called Throwdown with Bobby Flay, and you best him with these dumplings, whatever'
        )

    def test_smitten_kitchen_desc(self):
        soup_html = get_soup_html(
            'https://smittenkitchen.com/2015/09/broccoli-cheddar-soup/'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc,
            None
        )

    def test_tasty_desc(self):
        soup_html = get_soup_html(
            'https://cookieandkate.com/best-granola-bars-recipe/'
        )
        desc = scrape_recipe_description(soup_html)
        self.assertEqual(
            desc,
            "This granola bar recipe is so easy and delicious! These wholesome granola bars are naturally sweetened, gluten free, and the perfect healthy snack."
        )


class ScrapeIngredientsTestCase(TestCase):

    def test_find_ingredient_strings(self):
        soup_html = get_soup_html(
            'https://ohsheglows.com/2020/04/25/cozy-at-home-spicy-any-veggie-soup/'
        )
        ingredients = scrape_recipe_ingredients(soup_html)
        expected_ingredients = [
            '1 tablespoon (15 mL) coconut oil or olive oil',
            '2 1/2 cups (625 mL) water',
            '1 (14-ounce/398 mL) can light coconut milk',
            '1 (14-ounce/398 mL) can fire-roasted diced tomatoes*',
            '3 cups (190 g) broccoli florets (1 1/2-inch florets)**',
            '2 cups (270 g) peeled, seeded, and chopped butternut squash (1/2-inch cubes)',
            '1 1/2 cups (195 g) chopped peeled carrots (1/2-inch thick coins)',
            '1 1/2 cups (160 g) frozen cut green beans***',
            '2 teaspoons red pepper flakes, or to taste****',
            '1 teaspoon fine sea salt, or to taste',
            '1 teaspoon garlic powder',
            '1 cup (170 g) uncooked red lentils',
            '2 tablespoons (30 mL) apple cider vinegar, or to taste',
            'Herbamare, for garnish (optional)'
        ]
        self.assertEqual(
            ingredients,
            expected_ingredients
        )

    def test_find_ingredient_strings_wprm(self):
        soup_html = get_soup_html(
            'https://www.101cookbooks.com/braided-onion-bread/'
        )
        ingredients = scrape_recipe_ingredients(soup_html)
        expected_ingredients = [
            '3 tablespoons extra virgin olive oil',
            '4 cups chopped yellow onion (~2 large)',
            'Fine grain sea salt',
            '1 cup aged cheddar cheese, grated',
            '1/3 cup toasted sesame seeds',
            '4 1/2 cups / 540g unbleached all-purpose flour, plus more if needed',
            '2 tablespoons sugar',
            '1 1/2 teaspoons fine grain sea salt',
            '2 1/2 teaspoon (1 packet) active dry yeast',
            '1 1/2 cups warm milk or oat milk (120F)',
            '1 egg, beaten',
            '8 tablespoons unsalted butter, room temperature',
            '1 egg yolk'
        ]
        self.assertEqual(
            ingredients,
            expected_ingredients
        )

    def test_find_ingredient_strings_jetpack(self):
        soup_html = get_soup_html(
            'https://smittenkitchen.com/2008/08/crisp-rosemary-flatbread/'
        )
        ingredients = scrape_recipe_ingredients(soup_html)
        expected_ingredients = [
            '1 3/4 cups (230 grams) unbleached all-purpose flour',
            '1 tablespoon chopped rosemary plus 2 (6-inch) sprigs (optional)',
            '1 teaspoon baking powder',
            '3/4 teaspoon kosher salt',
            '1/2 cup (120 ml) water',
            '1/3 cup (80 ml) olive oil plus more for brushing',
            'Flaky sea salt such as Maldon'
        ]
        self.assertEqual(
            ingredients,
            expected_ingredients
        )

    def test_find_ingredient_strings_tasty(self):
        soup_html = get_soup_html(
            'https://cookieandkate.com/veggie-sesame-noodles-recipe/'
        )
        ingredients = scrape_recipe_ingredients(soup_html)
        expected_ingredients = [
            '8 ounces soba noodles or spaghetti noodles of choice*',
            "⅓ cup reduced sodium tamari (or soy sauce, just be sure it’s reduced sodium or it will taste too salty)",
            '¼ cup toasted sesame oil',
            '2 tablespoons lime juice (about 1 medium lime)',
            '½ teaspoon red pepper flakes, to taste (scale back or omit if sensitive to spice)',
            '2 ½ cups thinly sliced red cabbage (about 10 ounces or ¼th medium cabbage)',
            '3 whole carrots, peeled and then sliced into ribbons with vegetable peeler (about 1 ½ cups)',
            '1 red bell pepper, sliced into very thin strips',
            '1 bunch green onions, chopped',
            '½ cup chopped cilantro',
            'Optional: 2 cups shelled edamame, steamed'
        ]
        self.assertEqual(
            ingredients,
            expected_ingredients
        )

    def test_find_ingredient_strings_bon_appetit(self):
        soup_html = get_soup_html(
            'https://www.bonappetit.com/recipe/seared-short-ribs-with-mushrooms'
        )
        ingredients = scrape_recipe_ingredients(soup_html)
        expected_ingredients = [
            '1',
            'lb. 1½"-thick boneless beef short ribs 1',
            'tsp. kosher salt, plus more',
            'Freshly ground black pepper ½',
            'cup finely chopped hot cherry peppers or other hot pickled chiles, plus 3 '
            'Tbsp. brine 1½',
            'tsp. honey 5',
            'Tbsp. extra-virgin olive oil, divided 1¼',
            'lb. mixed wild mushrooms (such as maitake and/or oyster), stems removed, '
            'torn into 1½" pieces 1',
            'large shallot, thinly sliced crosswise 5',
            'garlic cloves, thinly sliced ½',
            'cup finely chopped dill'
        ]
        self.assertEqual(
            ingredients,
            expected_ingredients
        )


class ScrapeDirectionsTestCase(TestCase):
    def test_scrape_directions_wprm(self):
        soup_html = get_soup_html(
            'https://www.101cookbooks.com/cavatelli/'
        )
        directions = scrape_recipe_directions(soup_html)
        self.assertEqual(
            directions[0],
            'Preheat oven to 400F.'
        )

    def test_scrape_directions_step(self):
        soup_html = get_soup_html(
            'https://cookieandkate.com/veggie-sesame-noodles-recipe/'
        )
        directions = scrape_recipe_directions(soup_html)
        self.assertEqual(
            directions[0],
            "Cook the soba noodles according to the package directions. Once they’re done cooking, drain them in a colander and rinse them well under cool water. Transfer the drained noodles to a large serving bowl and set aside."
        )

    # class ScrapeTimeTestCase(TestCase):
    #     def test_find_total_time_bon_appetit(self):

    # def test_find_prep_time_bon_appetit(self):

    # def test_find_cook_time_bon_appetit(self):

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
