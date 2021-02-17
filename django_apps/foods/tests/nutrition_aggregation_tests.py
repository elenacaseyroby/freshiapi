from django.test import TestCase
from django_apps.foods.management.commands.sync_foods_from_usda import (
    Command as c
)
from django_apps.foods.models import Unit, Food, Nutrient

import numpy as np
import pandas as pd
import os


# To run:
# python manage.py test django_apps.foods.tests.nutrition_aggregation_tests
class GetValidFoodTestCase(TestCase):
    # Mock this functions for tests.
    def get_unit_by_usdanutrient_id(self):
        mg = Unit(
            id=2,
            name="milligram"
        )
        return {
            1089: mg,
            1008: None
        }

    def test_usdanutrient_amounts(self):
        corn = Food(
            id=1,
            name='corn',
        )
        foods_by_fdc_id = {
            428135: corn,
            359627: corn,
            343000: corn,
            572158: corn,
            663228: corn,
            507375: corn,
            384528: corn,
            480952: corn
        }
        iron = Nutrient(
            id=2,
            name='iron'
        )
        nutrients_by_usdanutrient_id = {
            1089: iron,
        }
        fn_cols = ['fdc_id', 'nutrient_id', 'amount']
        fn_dtypes = {
            'fdc_id': np.float,
            'nutrient_id': np.float,
            'amount': np.float,
        }
        food_nutrient_df = pd.read_csv(
            os.path.join(
                os.path.dirname(__file__),
                '../tests/data/food_nutrient.csv'
            ),
            usecols=fn_cols,
            dtype=fn_dtypes
        )
        usdanutrient_amounts = c.get_usdanutrient_amounts(
            self,
            food_nutrient_df,
            foods_by_fdc_id,
            nutrients_by_usdanutrient_id
        )
        expected_usdanutrient_amounts = {}
        expected_usdanutrient_amounts[corn.id] = {}
        # 15mg iron
        expected_usdanutrient_amounts[corn.id][1089] = 15
        self.assertEqual(
            usdanutrient_amounts,
            expected_usdanutrient_amounts
        )

    def test_aggregate_nutrient_qtys(self):
        corn = Food(
            id=1,
            name='corn',
            one_serving_qty=128.00,
            one_serving_unit_id=1,
        )
        foods_by_id = {
            1: corn,
        }
        iron = Nutrient(
            id=2,
            name='iron',
            dv_unit_id=2  # mg
        )
        nutrients_by_usdanutrient_id = {
            1089: iron,
        }
        gram = Unit(
            id=1,
            name='gram',
        )
        units_by_abbr = {
            'g': gram,
        }
        # from_unit_id = unit_by_usdanutrient_id[usdanutrient_id].id
        #         to_unit_id = nutrient.dv_unit_id
        conversions = {}
        conversions[gram.id] = {}
        conversions[gram.id][2] = 1000  # g to mg
        conversions[2] = {}
        conversions[2][2] = 1
        conversions[gram.id][gram.id] = 1
        usdanutrient_amounts = {}
        usdanutrient_amounts[corn.id] = {}
        usdanutrient_amounts[corn.id][1089] = 15
        nutrient_qtys = c.aggregate_nutrient_qty(
            self,
            usdanutrient_amounts,
            conversions,
            nutrients_by_usdanutrient_id,
            units_by_abbr,
            foods_by_id
        )
        expected_nutrient_qtys = {}
        expected_nutrient_qtys[corn.id] = {}
        # 15mg iron * (128g/100g) = 19.2mg
        expected_nutrient_qtys[corn.id][2] = 19.2
        self.assertEqual(
            nutrient_qtys,
            expected_nutrient_qtys
        )

    def test_aggregate_nutrient_qtys_when_nutrient_has_no_unit(self):
        corn = Food(
            id=1,
            name='corn',
            one_serving_qty=128.00,
            one_serving_unit_id=1,
        )
        foods_by_id = {
            1: corn,
        }
        calories = Nutrient(
            id=1,
            name='calories',
            dv_unit_id=None
        )
        nutrients_by_usdanutrient_id = {
            1008: calories,
        }
        gram = Unit(
            id=1,
            name='gram',
        )
        units_by_abbr = {
            'g': gram,
        }
        conversions = {}
        conversions[gram.id] = {}
        conversions[gram.id][gram.id] = 1
        usdanutrient_amounts = {}
        usdanutrient_amounts[corn.id] = {}
        usdanutrient_amounts[corn.id][1008] = 367
        nutrient_qtys = c.aggregate_nutrient_qty(
            self,
            usdanutrient_amounts,
            conversions,
            nutrients_by_usdanutrient_id,
            units_by_abbr,
            foods_by_id
        )
        expected_nutrient_qtys = {}
        expected_nutrient_qtys[corn.id] = {}
        # 367 cal * (128g/100g) = 19.2mg
        expected_nutrient_qtys[corn.id][1] = 469.76
        self.assertEqual(
            nutrient_qtys,
            expected_nutrient_qtys
        )

    def test_aggregate_nutrient_qtys_if_conversion_from_unit_to_same_unit_dne(
        self
    ):
        gram = Unit(
            id=1,
            name='gram',
        )
        conversions = {}
        conversions[gram.id] = {}
        # leave out conversion[gram.id][gram.id] = 1
        corn = Food(
            id=1,
            name='corn',
            one_serving_qty=128.00,
            one_serving_unit_id=1,
        )
        foods_by_id = {
            1: corn,
        }
        calories = Nutrient(
            id=1,
            name='calories',
            dv_unit_id=None
        )
        nutrients_by_usdanutrient_id = {
            1008: calories,
        }
        units_by_abbr = {
            'g': gram,
        }
        usdanutrient_amounts = {}
        usdanutrient_amounts[corn.id] = {}
        usdanutrient_amounts[corn.id][1008] = 367
        nutrient_qtys = c.aggregate_nutrient_qty(
            self,
            usdanutrient_amounts,
            conversions,
            nutrients_by_usdanutrient_id,
            units_by_abbr,
            foods_by_id
        )
        expected_nutrient_qtys = {}
        expected_nutrient_qtys[corn.id] = {}
        # 367 cal * (128g/100g) = 19.2mg
        expected_nutrient_qtys[corn.id][1] = 469.76
        self.assertEqual(
            nutrient_qtys,
            expected_nutrient_qtys
        )
