from django.test import TestCase
from django_apps.foods.management.commands.sync_foods_from_usda import (
    Command as c
)
from django_apps.foods.models import Unit

import numpy as np
import pandas as pd
import os


# To run:
# python manage.py test django_apps.foods.tests.tests.GetValidFoodTestCase
class GetValidFoodTestCase(TestCase):
    # def setUp(self):

    def test_removes_code_at_end(self):
        usda_food_description = '''Grapefruit juice, white, shelf stable - NFY1213U4
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'grapefruit juice, white, shelf stable')

    def test_removes_code_at_end2(self):
        usda_food_description = '''Kale, Fresh, Unprepared - VA, TX 
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'kale, fresh, unprepared')

    def test_removes_bad_descriptor(self):
        usda_food_description = '''Vitamin C, Broccoli, raw (IN1,NY1) - NFY0904J9
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'broccoli, raw')

    def test_removes_measurements_in_later_descriptors(self):
        usda_food_description = '''WOLF BRAND Hot Chili Without Beans, 106 oz., 106 OZ
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'wolf brand hot chili without beans')

    def test_keeps_measurements_in_first_descriptor(self):
        usda_food_description = '''Diet Mtn Dew 7.5 Fluid Ounces Can
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'diet mtn dew 7.5 fluid ounces can')

    def test_cuts_off_descriptors_after_first_four(self):
        usda_food_description = '''Onion rings, breaded, par fried, frozen, prepared, heated in oven
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'onion rings, breaded, par fried, frozen')

    def test_cuts_off_after_open_paren(self):
        usda_food_description = '''Carrots, frozen, unprepared (Includes foods for USDA's Food Distribution Program)
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'carrots, frozen, unprepared')

    def test_removes_nutrient_descriptor(self):
        usda_food_description = '''Fatty Acids, Onion rings, frozen, ALEXIA (FL,MO) - NFY12068C
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'onion rings, frozen, alexia')

    def test_removes_region(self):
        usda_food_description = '''Oranges, Navel, Pass 2, Region 2, CY0109W, Yes,
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(food_name, 'oranges, navel')

    def test_dont_remove_lemon_lime(self):
        usda_food_description = '''LEMON-LIME THIRST QUENCHER POWDER, LEMON-LIME
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(
            food_name, 'lemon-lime thirst quencher powder, lemon-lime')


# To run:
# python manage.py test django_apps.foods.tests.tests.BatchSyncFoodsTestCase
class BatchSyncFoodsTestCase(TestCase):
    # def setUp(self):

    def test_foods_with_same_first_4_descriptors_are_collapsed(self):
        food_cols = ['fdc_id', 'description',
                     'data_type', 'food_category_id']
        food_dtypes = {
            'fdc_id': np.float,
            'description': np.str,
            'data_type': np.str,
            'food_category_id': np.float
        }
        food_batch_df = pd.read_csv(
            os.path.join(
                os.path.dirname(__file__),
                '../tests/data/collapse_names_tests/food.csv'
            ),
            usecols=food_cols,
            dtype=food_dtypes,
            sep=',',
            quotechar='"')
        upc_by_fdc = {}
        servings_by_fdc = {}
        foods_by_fdc = {}
        foods_by_name = {}
        # In real sync this will be a list of
        # all the foods with rows in the
        # food_nutrient.csv.  We only sync foods with
        # rows in this csv.  For this test, we will add
        # all foods from the food_batch_df to this list
        # so they all sync.
        fdc_ids_with_nutrition_facts = [
            food_batch_df['fdc_id'][row] for row in
            food_batch_df.index
        ]
        gram = Unit(
            id=1,
            name='gram',
            abbr='g'
        )
        gram.save()
        c.batch_sync_foods(
            self,
            food_batch_df,
            upc_by_fdc,
            servings_by_fdc,
            fdc_ids_with_nutrition_facts,
            gram,
            foods_by_fdc,
            foods_by_name
        )
        collapsed_food = Food.objects.get(
            name="squash, summer, yellow or green, cooked")
        collapsed_food_fdc_ids = [
            usdafood.fdc_id for usdafood in collapsed_food.usdafoods.all()]
        expected_fdc_ids = [
            343332, 343333, 343334, 343335, 343336, 343337, 343338, 343339,
            343340, 343341, 343342, 343343, 343344, 343345, 343346, 343347,
            343348, 343349, 343350, 343351, 343352, 343353, 343354, 343355]
        self.assertEqual(expected_fdc_ids, collapsed_food_fdc_ids)
