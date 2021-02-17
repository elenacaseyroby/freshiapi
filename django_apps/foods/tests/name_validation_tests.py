from django.test import TestCase
from django_apps.foods.management.commands.sync_foods_from_usda import (
    Command as c
)
from django_apps.foods.models import Unit

import numpy as np
import pandas as pd
import os


# To run:
# python manage.py test django_apps.foods.tests.name_validation_tests
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

    def test_maintain_foods_with_pass_in_name(self):
        usda_food_description = '''PASSION FRUIT JUICE FROM CONCENTRATE, PASSION FRUIT
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(
            food_name, 'passion fruit juice from concentrate, passion fruit')

    def test_remove_name_pass_and_beyond(self):
        usda_food_description = '''Broccoli, Pass 2, Region 1, AR1, NFY010D0L","11","2019-04-01
        '''
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(
            food_name, 'broccoli')

    def test_cape_cod_foods(self):
        usda_food_description = 'CAPE COD, POPCORN DUOS'
        food_name = c.get_valid_food_name(self, usda_food_description)
        self.assertEqual(
            food_name, 'cape cod, popcorn duos')
