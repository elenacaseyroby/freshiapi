from django.test import TestCase

from django_apps.foods.models import Unit, Food

from django_apps.recipes.scraper.parse_ingredients import (
    parse_numerator,
    parse_denominator,
    parse_unit,
    parse_food_str
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
    units_by_name = {
        'g': gram,
        'gram': gram,
        'c': cup,
        'cup': cup,
        'tbsp': tbsp,
        'tablespoon': tbsp,
        'tspn': tspn,
        'teaspoon': tspn,
        'oz': ounce,
    }

    def test_parse_numerator(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        numerator = parse_numerator(ingredient_str, self.units_by_name)
        self.assertEqual(
            numerator,
            3
        )

    def test_parse_denominator(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        denominator = parse_denominator(ingredient_str, self.units_by_name)
        self.assertEqual(
            denominator,
            1
        )

    def test_parse_unit(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        unit = parse_unit(ingredient_str, self.units_by_name,
                          self.units_by_name)
        self.assertEqual(
            unit,
            self.units_by_name['oz']
        )

    def test_parse_food(self):
        ingredient_str = '3oz. Parmesan, grated (about ¾ cup)'
        food_str = parse_food_str(ingredient_str, self.units_by_name)
        self.assertEqual(
            food_str,
            'parmesan'
        )
