from django.test import TestCase

from django_apps.foods.models import Unit, Food

from django_apps.recipes.scraper.parse_ingredients import (
    parse_numerator,
    parse_denominator,
    parse_unit,
    parse_food_str,
    remove_modifiers
)


# To run:
# python manage.py test django_apps.recipes.tests.parser_tests
class ParserTestCase(TestCase):
    gram = Unit(
        name='gram'
    )
    cup = Unit(
        name='cup'
    )
    tbsp = Unit(
        name='tablespoon'
    )
    tspn = Unit(
        name='teaspoon'
    )
    ounce = Unit(
        name='ounce'
    )
    liter = Unit(
        name='liter'
    )
    units_by_name = {
        'gram': gram,
        'cup': cup,
        'tablespoon': tbsp,
        'teaspoon': tspn,
    }
    units_by_abbr = {
        'g': gram,
        'c': cup,
        'tbsp': tbsp,
        'tspn': tspn,
        'oz': ounce,
        'l': liter
    }

    def test_parse_numerator(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            3
        )

    def test_parse_numerator2(self):
        ingredient_str = '1 teaspoon kosher salt plus more'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            1
        )

    def test_parse_numerator3(self):
        ingredient_str = '1 oz (or 3/4 cup) shelled fresh peas (from about 1 pound pods) or frozen peas, thawed'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            1
        )

    def test_parse_numerator_with_whole_number_and_fraction(self):
        ingredient_str = '1 1/2cup Parmesan, grated'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            3
        )

    def test_parse_numerator_with_fraction(self):
        ingredient_str = '1/2cup Parmesan, grated'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            1
        )

    def test_parse_numerator_without_unit(self):
        ingredient_str = '1 1/2 small cantaloupe or Honey Kiss melon(about 1½ lb.)'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            3
        )

    def test_parse_numerator_w_dash(self):
        ingredient_str = '1-2 Tbsp olive oil'
        numerator = parse_numerator(ingredient_str)
        self.assertEqual(
            numerator,
            1
        )

    def test_parse_denominator(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        denominator = parse_denominator(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            denominator,
            1
        )

    def test_parse_denominator_with_fraction(self):
        ingredient_str = '1/2 cup Parmesan, grated'
        denominator = parse_denominator(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            denominator,
            2
        )

    def test_parse_denominator_without_unit(self):
        ingredient_str = '1/2 small cantaloupe or Honey Kiss melon(about 1½ lb.)'
        denominator = parse_denominator(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            denominator,
            2
        )

    def test_parse_unit(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        unit = parse_unit(ingredient_str, self.units_by_name,
                          self.units_by_abbr)
        self.assertEqual(
            unit,
            self.units_by_abbr['oz']
        )

    def test_parse_unit_w_dash(self):
        ingredient_str = '1-2 Tbsp olive oil'
        unit = parse_unit(ingredient_str, self.units_by_name,
                          self.units_by_abbr)
        self.assertEqual(
            unit,
            self.units_by_abbr['tbsp']
        )

    def test_parse_unit2(self):
        ingredient_str = '1 oz (or 3/4 cup) shelled fresh peas (from about 1 pound pods) or frozen peas, thawed'
        unit = parse_unit(ingredient_str, self.units_by_name,
                          self.units_by_abbr)
        self.assertEqual(
            unit,
            self.units_by_abbr['oz']
        )

    def test_parse_food(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'parmesan'
        )

    def test_parse_food2(self):
        ingredient_str = '1 teaspoon kosher salt plus more'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'kosher salt'
        )

    def test_parse_food3(self):
        ingredient_str = '3 large eggs'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'large eggs'
        )

    def test_parse_food4(self):
        ingredient_str = '2 ripe tomatoes, sliced (optional // organic when possible)'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'ripe tomatoes'
        )

    def test_parse_food_with_paren(self):
        ingredient_str = '1 cup shelled fresh peas (from about 1 pound pods) or frozen peas, thawed'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'peas'
        )

    def test_parse_food_with_paren_before_food(self):
        ingredient_str = '1 oz (or 3/4 cup) shelled fresh peas (from about 1 pound pods) or frozen peas, thawed'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'peas'
        )

    def test_parse_unit_no_unit(self):
        ingredient_str = '3 large eggs'
        unit = parse_unit(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            unit,
            None
        )

    def test_parse_food_no_unit(self):
        ingredient_str = '3 large eggs'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'large eggs'
        )

    def test_parse_food_plural_unit(self):
        ingredient_str = '2 tablespoons vegetable oil plus more for skillet'
        food_str = parse_food_str(
            ingredient_str, self.units_by_name, self.units_by_abbr)
        self.assertEqual(
            food_str,
            'vegetable oil'
        )

    def test_remove_modifiers(self):
        food_str = '(or 3/4 cup) shelled fresh peas (from about 1 pound pods) or frozen peas, thawed'
        food_str = remove_modifiers(food_str)
        self.assertEqual(
            food_str,
            'peas'
        )
