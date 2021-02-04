import pandas as pd
import numpy as np
from django.db import models, transaction
from django.core.management.base import BaseCommand
from django_apps.foods.models import (
    USDACategory,
    USDAFood,
    Food, Unit,
    FoodUSDAFood,
    Nutrient,
    NutritionFact,
    UnitConversion,
    Unit
)

import sys
import math


class Command(BaseCommand):
    """
    These methods sacrifice readability in favor of performance.
    """
    help = 'Sync foods from USDA food and nutrient data sets.'

    def get_category_id(self, data_type, usdacategory_id, name):
        # I know for this I should query db to get usdacategory
        # names in case they've changed.
        # I'm not doing that because it would be too many queries
        # and I think it's unlikely they will change.

        category_ids_by_data_type = {}
        # Legumes:
        category_ids_by_data_type['agricultural_acquisition'] = 16
        # Branded Foods:
        category_ids_by_data_type['branded_food'] = 26

        category_ids_by_keyword = {}
        # Branded
        category_ids_by_keyword['kroger'] = 26
        category_ids_by_keyword['ore-ida'] = 26
        # Restaurant Foods
        category_ids_by_keyword['pizza'] = 25
        category_ids_by_keyword['restaurant'] = 25
        # Dairy
        category_ids_by_keyword['milk'] = 1
        category_ids_by_keyword['yogurt'] = 1
        category_ids_by_keyword['egg'] = 1
        category_ids_by_keyword['cream'] = 1
        category_ids_by_keyword['kefir'] = 1
        category_ids_by_keyword['cheese'] = 1
        # Legumes
        category_ids_by_keyword['bean'] = 16
        category_ids_by_keyword['lentil'] = 16
        category_ids_by_keyword['tofu'] = 16
        category_ids_by_keyword['chickpea'] = 16
        # Pork
        category_ids_by_keyword['pork'] = 10
        category_ids_by_keyword['hog'] = 10
        category_ids_by_keyword['bacon'] = 10
        # Fish
        category_ids_by_keyword['pork'] = 15
        category_ids_by_keyword['tuna'] = 15
        category_ids_by_keyword['shrimp'] = 15
        category_ids_by_keyword['crab'] = 15
        category_ids_by_keyword['fish'] = 15
        category_ids_by_keyword['turtle'] = 15
        category_ids_by_keyword['clam'] = 15
        category_ids_by_keyword['oyster'] = 15
        category_ids_by_keyword['mussel'] = 15
        category_ids_by_keyword['lobster'] = 15
        category_ids_by_keyword['seafood'] = 15
        category_ids_by_keyword['halibut'] = 15
        category_ids_by_keyword['herring'] = 15
        category_ids_by_keyword['mackerel'] = 15
        category_ids_by_keyword['mullet'] = 15
        category_ids_by_keyword['perch'] = 15
        category_ids_by_keyword['ray'] = 15
        category_ids_by_keyword['sturgeon'] = 15
        category_ids_by_keyword['salmon'] = 15
        category_ids_by_keyword['trout'] = 15
        category_ids_by_keyword['tilapia'] = 15
        category_ids_by_keyword['whiting'] = 15
        category_ids_by_keyword['sea bass'] = 15
        category_ids_by_keyword['shark'] = 15
        category_ids_by_keyword['squid'] = 15
        category_ids_by_keyword['octopus'] = 15
        category_ids_by_keyword['roe'] = 15
        category_ids_by_keyword['abalone'] = 15
        category_ids_by_keyword['scallops'] = 15
        category_ids_by_keyword['carp'] = 15
        category_ids_by_keyword['eel'] = 15
        category_ids_by_keyword['flounder'] = 15
        category_ids_by_keyword['haddock'] = 15
        category_ids_by_keyword['porgy'] = 15
        category_ids_by_keyword['pike'] = 15
        category_ids_by_keyword['pompano'] = 15
        category_ids_by_keyword['cod'] = 15
        category_ids_by_keyword['eel'] = 15
        category_ids_by_keyword['croaker'] = 15
        # Baked
        category_ids_by_keyword['bread'] = 18
        category_ids_by_keyword['roll'] = 18
        category_ids_by_keyword['muffin'] = 18
        # Poultry
        category_ids_by_keyword['poultry'] = 5
        category_ids_by_keyword['chicken'] = 5
        category_ids_by_keyword['duck'] = 5
        category_ids_by_keyword['turkey'] = 5
        category_ids_by_keyword['quail'] = 5
        category_ids_by_keyword['goose'] = 5
        category_ids_by_keyword['hen'] = 5
        category_ids_by_keyword['pheasant'] = 5
        category_ids_by_keyword['dove'] = 5
        # Snack
        category_ids_by_keyword['dip'] = 23
        category_ids_by_keyword['chip'] = 23
        category_ids_by_keyword['cracker'] = 23
        category_ids_by_keyword['hummus'] = 23
        category_ids_by_keyword['puff'] = 23
        category_ids_by_keyword['popcorn'] = 23
        # Soup, Sauce
        category_ids_by_keyword['soup'] = 6
        category_ids_by_keyword['sauce'] = 6
        category_ids_by_keyword['gravy'] = 6
        # Beef
        category_ids_by_keyword['beef'] = 13
        category_ids_by_keyword['liver'] = 13
        category_ids_by_keyword['brain'] = 13
        category_ids_by_keyword['tongue'] = 13
        category_ids_by_keyword['burger'] = 13
        category_ids_by_keyword['tripe'] = 13
        # Lunchmeat & Sausages
        category_ids_by_keyword['lunch meat'] = 7
        category_ids_by_keyword['salami'] = 7
        category_ids_by_keyword['ham'] = 7
        category_ids_by_keyword['bologna'] = 7
        category_ids_by_keyword['sausage'] = 7
        category_ids_by_keyword['franfurter'] = 7
        category_ids_by_keyword['hot dog'] = 7
        # Game
        category_ids_by_keyword['lamb'] = 17
        category_ids_by_keyword['veal'] = 17
        category_ids_by_keyword['rabbit'] = 17
        category_ids_by_keyword['moose'] = 17
        category_ids_by_keyword['bear'] = 17
        category_ids_by_keyword['bison'] = 17
        category_ids_by_keyword['opossum'] = 17
        category_ids_by_keyword['caribou'] = 17
        category_ids_by_keyword['squirrel'] = 17
        category_ids_by_keyword['raccoon'] = 17
        category_ids_by_keyword['beaver'] = 17
        category_ids_by_keyword['armadillo'] = 17
        category_ids_by_keyword['ostrich'] = 17
        category_ids_by_keyword['deer'] = 17
        category_ids_by_keyword['goat'] = 17
        # Baby Foods
        category_ids_by_keyword['gerber'] = 3
        category_ids_by_keyword['formula'] = 3
        category_ids_by_keyword['baby food'] = 3
        # Breakfast
        category_ids_by_keyword['bar'] = 8
        category_ids_by_keyword['smoothie'] = 8
        category_ids_by_keyword['oatmeal'] = 8
        category_ids_by_keyword['granola'] = 8
        category_ids_by_keyword['kashi'] = 8
        category_ids_by_keyword['kellogs'] = 8
        category_ids_by_keyword['cereal'] = 8
        category_ids_by_keyword['bran'] = 8
        category_ids_by_keyword['waffle'] = 8
        category_ids_by_keyword['toast'] = 8
        # Grains
        category_ids_by_keyword['noodles'] = 20
        category_ids_by_keyword['pasta'] = 20
        category_ids_by_keyword['macaroni'] = 20
        category_ids_by_keyword['spaghetti'] = 20
        category_ids_by_keyword['rice'] = 20
        category_ids_by_keyword['grits'] = 20
        category_ids_by_keyword['quinoa'] = 20
        # Sweets
        category_ids_by_keyword['flan'] = 19
        category_ids_by_keyword['custard'] = 19
        category_ids_by_keyword['pudding'] = 19
        category_ids_by_keyword['chocolate'] = 19
        category_ids_by_keyword['vanilla'] = 19
        category_ids_by_keyword['caramel'] = 19
        category_ids_by_keyword['cake'] = 19
        category_ids_by_keyword['cookie'] = 19
        category_ids_by_keyword['crisp'] = 19
        category_ids_by_keyword['pie'] = 19
        category_ids_by_keyword['turnover'] = 19
        category_ids_by_keyword['cobbler'] = 19
        # Nut and seed
        category_ids_by_keyword['nut'] = 12
        category_ids_by_keyword['seed'] = 12
        # Beverage
        category_ids_by_keyword['tea'] = 14
        category_ids_by_keyword['drink'] = 14
        # Fruit & Juice
        category_ids_by_keyword['apple'] = 9
        category_ids_by_keyword['mango'] = 9
        category_ids_by_keyword['pinapple'] = 9
        category_ids_by_keyword['pear'] = 9
        category_ids_by_keyword['berries'] = 9
        category_ids_by_keyword['peach'] = 9
        category_ids_by_keyword['pomegranate'] = 9
        category_ids_by_keyword['banana'] = 9
        category_ids_by_keyword['grape'] = 9
        category_ids_by_keyword['tomato'] = 9
        category_ids_by_keyword['lime'] = 9
        category_ids_by_keyword['lemon'] = 9
        category_ids_by_keyword['guava'] = 9
        category_ids_by_keyword['papaya'] = 9
        category_ids_by_keyword['passion fruit'] = 9
        category_ids_by_keyword['nectar'] = 9
        category_ids_by_keyword['cantaloupe'] = 9
        category_ids_by_keyword['melon'] = 9
        category_ids_by_keyword['berry'] = 9
        # Veggie
        category_ids_by_keyword['vegetable protein'] = 11
        category_ids_by_keyword['chard'] = 11
        category_ids_by_keyword['broccoli'] = 11
        category_ids_by_keyword['beet'] = 11
        category_ids_by_keyword['kale'] = 11
        category_ids_by_keyword['mushroom'] = 11
        category_ids_by_keyword['corn'] = 11
        category_ids_by_keyword['bok choy'] = 11
        category_ids_by_keyword['cabbage'] = 11
        category_ids_by_keyword['lettuce'] = 11
        category_ids_by_keyword['spinach'] = 11
        category_ids_by_keyword['pepper'] = 11
        category_ids_by_keyword['onion'] = 11
        category_ids_by_keyword['collard'] = 11
        category_ids_by_keyword['greens'] = 11
        category_ids_by_keyword['turnip'] = 11
        category_ids_by_keyword['radish'] = 11
        category_ids_by_keyword['watercress'] = 11
        category_ids_by_keyword['carrot'] = 11
        category_ids_by_keyword['pea'] = 11
        category_ids_by_keyword['potato'] = 11
        category_ids_by_keyword['cucumber'] = 11
        category_ids_by_keyword['celery'] = 11
        category_ids_by_keyword['fennel'] = 11
        category_ids_by_keyword['squash'] = 11
        category_ids_by_keyword['seaweed'] = 11
        category_ids_by_keyword['artichoke'] = 11
        category_ids_by_keyword['asparagus'] = 11
        category_ids_by_keyword['sprouts'] = 11
        category_ids_by_keyword['cauliflower'] = 11
        category_ids_by_keyword['okra'] = 11
        category_ids_by_keyword['plantain'] = 11
        category_ids_by_keyword['yam'] = 11

        # 1. If category set, run with that.
        if usdacategory_id:
            return int(usdacategory_id)

        # 2. If data type is meaningful run with that.
        if data_type in category_ids_by_data_type:
            return int(category_ids_by_data_type[data_type])

        # 3. If name contains keywords run with that.
        normal_name = str(name).lower()
        for keyword in category_ids_by_keyword:
            if keyword in normal_name:
                return int(category_ids_by_keyword[keyword])

        return None

    def weed_out_food(self, data_type, name, fdc_id_by_food_names):
        # Weed out about 200 entries like this:
        # "328216","sub_sample_food","Niacin, Cheese,...
        # "328217","sub_sample_food","Proximates, Cheese,...
        if (
            str(data_type) == 'sub_sample_food' and
            str(name).contains(', Cheese')
        ):
            return True

        # We use fdc_id_by_food_names
        # to link fdc_id to new food objects
        # after they have been created.
        # To avoid adding new food objects with the
        # same name (foods with same name have multiple
        # fdc_ids in food.csv unfortunately),
        # weed out food if it's already in the list
        # of new food objects.
        if name in fdc_id_by_food_names:
            return True
        return False

    def get_display_unit(self, portion_description, modifier):
        # Choose which column to get the data from
        data = (
            portion_description
            if (
                portion_description != 'nan' and
                portion_description != '''
                Quantity not specified'''
            ) else
            modifier
        )
        # Return None if column is empty.
        if (
            data == 'nan' or
            data == 'Quantity not specified'
        ):
            return ''
        # Else return string
        return data

    def get_one_serving_description(self, portion_desc, modifier, amount):
        portion_desc = str(portion_desc)
        modifier = str(modifier)
        amount = str(amount)
        one_serving_display_qty = (
            ''
            if amount == 'nan' else
            amount
        )
        one_serving_display_unit = self.get_display_unit(
            portion_desc,
            modifier
        )
        return (
            f'{one_serving_display_qty} {one_serving_display_unit}'[:39]
            if (
                one_serving_display_qty != '' and
                one_serving_display_unit != ''
            ) else
            None
        )

    def get_servings_by_fdc(self):
        portion_cols = ['fdc_id', 'portion_description',
                        'modifier', 'gram_weight', 'amount']
        portion_dtypes = {
            'fdc_id': np.float,
            'portion_description': np.str,
            'modifier': np.str,
            'gram_weight': np.float,
            'amount': np.str,
        }
        try:
            food_portion_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_portion.csv',
                usecols=portion_cols,
                dtype=portion_dtypes)
        except:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync foods: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food_portion.csv'
            ))
        grams = Unit.objects.get(name="gram")
        servings_by_fdc = {}
        for row in food_portion_df.index:
            one_serving_qty = round(float(
                food_portion_df['gram_weight'][row]), 2)
            # Skip foods with negative and thus inaccurate
            # serving qty.
            if one_serving_qty <= 0:
                continue

            portion_desc = food_portion_df['portion_description'][row]
            modifier = food_portion_df['modifier'][row]
            amount = food_portion_df['amount'][row]
            fdc_id = int(food_portion_df['fdc_id'][row])
            servings_by_fdc[fdc_id] = {}
            servings_by_fdc[fdc_id]['description'] = \
                self.get_one_serving_description(
                    portion_desc,
                    modifier,
                    amount
            )
            servings_by_fdc[fdc_id]['unit'] = grams
            servings_by_fdc[fdc_id]['qty'] = one_serving_qty
        return servings_by_fdc

    def skip_food_is_true(
        self,
        row,
        food_df,
        fdc_id,
        fdc_with_nutrition_facts,
        existing_food_names,
        fdc_by_food_name
    ):
        # Skip if food doesn't have associated nutrition_facts
        if fdc_id not in fdc_with_nutrition_facts:
            return True

        # Skip about 200 entries like this:
        # "328216","sub_sample_food","Niacin, Cheese,...
        # "328217","sub_sample_food","Proximates, Cheese,...
        data_type = str(food_df['data_type'][row])
        name = str(food_df['description'][row])
        if (
            data_type == 'sub_sample_food' and
            ', Cheese' in name
        ):
            return True

        # There are multiple food objects with same
        # name in the csvs.
        # Skip foods with the same name that exist in
        # our db with the same name or foods in the csv
        # that have already been processed in this sync.
        if name in fdc_by_food_name or name in existing_food_names:
            return True
        return False

    def create_food_object(self, row, food_df, servings_by_fdc, upc_by_fdc, gram):
        food = Food()
        fdc_id = food_df['fdc_id'][row]
        data_type = food_df['data_type'][row]
        food.name = food_df['description'][row][:99]
        # Record serving size so that nutrition facts align.
        # If none, like in the case of some yogurts,
        # make serving size 100 grams.
        if fdc_id in servings_by_fdc:
            food.one_serving_qty = servings_by_fdc[fdc_id]['qty']
            food.one_serving_unit = servings_by_fdc[fdc_id]['unit']
            food.one_serving_description = servings_by_fdc[
                fdc_id
            ][
                'description'
            ]
            food.upc_code = upc_by_fdc[fdc_id] if fdc_id in upc_by_fdc else None
        else:
            food.one_serving_qty = 100
            food.one_serving_unit = gram
            food.one_serving_description = None
        usdacategory_id = (
            None
            if math.isnan(food_df['food_category_id'][row]) else
            int(food_df['food_category_id'][row])
        )
        food.usdacategory_id = self.get_category_id(
            data_type, usdacategory_id, food.name)
        return food

    def food_updated_is_true(self, updated_food, food_in_db):
        return not (
            updated_food.name == food_in_db.name and
            updated_food.one_serving_qty == food_in_db.one_serving_qty and
            updated_food.one_serving_unit == food_in_db.one_serving_unit and
            updated_food.upc_code == food_in_db.upc_code and
            updated_food.one_serving_description == food_in_db.one_serving_description
        )

    def get_food_to_update_by_fdc(self, foods_by_fdc, food, fdc_id):
        if fdc_id not in foods_by_fdc:
            return None
        food_in_db = foods_by_fdc[fdc_id]
        food_updated = self.food_updated_is_true(food, food_in_db)
        if not food_updated:
            return None
        food.id = food_in_db.id
        return food

    def get_food_to_update_by_name(self, foods_by_name, food):
        food_to_update = None
        usdafood_to_create = None
        food_usdafood_to_create = None
        if food.name not in foods_by_name:
            return food_to_update, usdafood_to_create, food_usdafood_to_create
        food_in_db = foods_by_name[food.name]
        food_updated = self.food_updated_is_true(food, food_in_db)
        if food_updated:
            food.id = food_in_db.id
            food_to_update = food
        return food_to_update

    def update_or_create_new_foods(
        self,
        foods_to_create,
        foods_to_update,
        usdafoods_to_create,
        foods_to_link_to_usdafoods,
        fdc_by_food_name
    ):
        # Create and update food and usdafood objects.
        food_fields = [
            'name', 'usdacategory_id', 'upc_code', 'one_serving_qty',
            'one_serving_unit', 'one_serving_description']
        print(f'{len(foods_to_update)} foods to update')
        Food.objects.bulk_update(foods_to_update, food_fields, batch_size=100)
        print('updated foods!')
        print(f'{len(foods_to_create)} foods to create')
        new_usdafoods = USDAFood.objects.bulk_create(usdafoods_to_create)
        print('created usdafoods!')
        new_foods = Food.objects.bulk_create(foods_to_create)
        print('created foods!')
        # Add new foods with ids to foods_to_link_to_usdafoods.
        foods_to_link_to_usdafoods.extend(new_foods)
        udsafoods_by_fdc = {uf.fdc_id: uf for uf in new_usdafoods}
        foods_usdafoods_to_create = []
        for food in foods_to_link_to_usdafoods:
            fdc = fdc_by_food_name[food.name]
            usdafood = udsafoods_by_fdc[fdc]
            foods_usdafoods_to_create.append(
                FoodUSDAFood(food=food, usdafood=usdafood)
            )
        FoodUSDAFood.objects.bulk_create(foods_usdafoods_to_create)
        print('linked foods to usdafoods!')
        return "Success"

    def get_nutrition_facts_dict(self):
        all_nutrition_facts = NutritionFact.objects.all()
        nutrition_facts_dict = {}
        for fact in all_nutrition_facts:
            food_id = fact.food_id
            nutrient_id = fact.nutrient_id
            if food_id not in nutrition_facts_dict:
                nutrition_facts_dict[food_id] = {}
            nutrition_facts_dict[food_id][nutrient_id] = fact
        return nutrition_facts_dict

    def get_unit_conversions_dict(self):
        all_unit_conversions = UnitConversion.objects.all()
        unit_conversions_dict = {}
        for conv in all_unit_conversions:
            if conv.from_unit_id not in unit_conversions_dict:
                unit_conversions_dict[conv.from_unit_id] = {}
            unit_conversions_dict[
                conv.from_unit_id
            ][
                conv.to_unit_id
            ] = conv.qty_conversion_coefficient

    def skip_nutrition_fact_is_true(
        self,
        fdc_id,
        foods_by_fdc,
        usdanutrient_id,
        nutrients_by_usdanutrient_id,
        nutrient_amount
    ):
        # Skip if fdc not associated w food in our db.
        if fdc_id not in foods_by_fdc:
            return True
        # Skip if usdanutrient_id not associated w nutrient in our db.
        if usdanutrient_id not in nutrients_by_usdanutrient_id:
            return True
        # Skip if no nutrient_amount
        if (
            nutrient_amount == 0 or
            math.isnan(nutrient_amount)
        ):
            return True
        return False

    def get_upc_by_fdc(self):
        market_cols = ['fdc_id', 'upc_code']
        market_dtypes = {'fdc_id': np.float, 'upc_code': np.str}
        try:
            market_acquisition_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/market_acquisition.csv',
                usecols=market_cols,
                dtype=market_dtypes)
        except:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync foods: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                market_acquisition.csv'
            ))
        upc_by_fdc = {}
        # Create dict to sort upc_code (bar codes) by fdc_id
        for row in market_acquisition_df.index:
            fdc_id = int(market_acquisition_df['fdc_id'][row])
            upc_code = None
            try:
                upc_code = int(market_acquisition_df['upc_code'][row])
            except:
                pass
            upc_by_fdc[fdc_id] = upc_code
        return upc_by_fdc

    def get_unit_by_usdanutrient_id(self):
        nutrient_cols = ['id', 'unit_name']
        nutrient_dtypes = {'id': np.float, 'unit_name': np.str}
        try:
            nutrient_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/nutrient.csv',
                usecols=nutrient_cols,
                dtype=nutrient_dtypes)
        # Throw error if csvs are not uploaded.
        except NameError:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync nutrition facts: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                nutrient.csv'
            ))
        units_by_abbr = {unit.abbr: unit for unit in Unit.objects.all()}
        unit_by_usdanutrient_id = {}
        for row in nutrient_df.index:
            usdanutrient_id = int(nutrient_df['id'][row])
            unit_name = nutrient_df['unit_name'][row]
            # In some cases like calories,
            # a nutrient will not have a unit in our system.
            # In these cases unit = None
            unit = None
            if unit_name == 'G':
                unit = units_by_abbr['g']
            if unit_name == 'MG_ATE':
                unit = units_by_abbr['mg']
            if unit_name == 'MG':
                unit = units_by_abbr['mg']
            if unit_name == 'UG':
                unit = units_by_abbr['ug']
            # Nutrients like vitamin a, c, e, d with unit
            # IU will also be set to unit = None
            # since we know that the unit in the csv and the unit
            # in our system is the same and that no conversion
            # is required.
            unit_by_usdanutrient_id[usdanutrient_id] = unit
        return unit_by_usdanutrient_id

    def get_nutrient_qty(
        self,
        row,
        food_nutrient_df,
        unit_by_usdanutrient_id,
        nutrients_by_usdanutrient_id,
        unit_conversions_dict,
        units_by_abbr,
        foods_by_fdc
    ):
        usdanutrient_qty = (
            0
            if math.isnan(food_nutrient_df['amount'][row]) else
            float(food_nutrient_df['amount'][row])
        )
        if usdanutrient_qty == 0:
            return 0
        # By default don't convert qty
        nutrient_qty_per_100g_food = float(usdanutrient_qty)
        # If nutrient has unit set (unlike calories), convert to
        # nutrient qty per usda nutrient unit to
        # nutrient qty per nutrient unit to
        usdanutrient_id = int(food_nutrient_df['nutrient_id'][row])
        nutrient = nutrients_by_usdanutrient_id[usdanutrient_id]
        usdanutrient_unit = unit_by_usdanutrient_id[usdanutrient_id]
        if (
            nutrient.dv_unit_id is not None and
            usdanutrient_unit is not None
        ):
            from_unit_id = usdanutrient_unit.id
            to_unit_id = nutrient.dv_unit_id
            # If units are different, calculate conversion
            if from_unit_id != to_unit_id:
                qty_conversion_coefficient = unit_conversions_dict[
                    from_unit_id
                ][
                    to_unit_id
                ]
                # nutrient amount is per 100g of food
                nutrient_qty_per_100g_food = float(
                    usdanutrient_qty * qty_conversion_coefficient
                )
        # Update nutrient_qty to be per food servings instead of
        # per 100 grams of food.
        fdc_id = int(food_nutrient_df['fdc_id'][row])
        food = foods_by_fdc[fdc_id]
        grams_food_per_serving = float(food.one_serving_qty)
        gram = units_by_abbr['g']
        if food.one_serving_unit_id != gram.id:
            from_unit_id = food.one_serving_unit_id
            to_unit_id = gram.id
            convert_to_grams = unit_conversions_dict[from_unit_id][to_unit_id]
            grams_food_per_serving = float(
                food.one_serving_qty * convert_to_grams
            )
        # all usda foods will have one_serving_qty in grams
        # divide by 100g and multiply by nutrient qty per 100g
        # to get nutrient_qty.
        food_100g = float(100)
        nutrient_qty_per_serving_food = (
            nutrient_qty_per_100g_food *
            (grams_food_per_serving / food_100g)
        )
        nutrient_qty = round(float(nutrient_qty_per_serving_food), 2)
        return nutrient_qty

    def get_fdc_ids_with_nutrition_facts(self):
        fn_cols = ['fdc_id']
        fn_dtypes = {
            'fdc_id': np.float
        }
        try:
            food_nutrient_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_nutrient.csv',
                usecols=fn_cols,
                dtype=fn_dtypes)
        # Throw error if csvs are not uploaded.
        except NameError:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync nutrition facts: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food_nutrient.csv'
            ))
        fdc_ids = [int(food_nutrient_df['fdc_id'][row])
                   for row in food_nutrient_df.index]
        return fdc_ids

    @transaction.atomic
    def sync_categories(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        try:
            category_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_category.csv')
        # Throw error if csvs are not uploaded.
        except:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync categories: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3: food_category.csv'
            ))

            # Get all categories in db.
        cats = USDACategory.objects.all()
        cats_by_id = {}
        for cat in cats:
            cats_by_id[cat.usdacategory_id] = cat
        cats_to_create = []
        cats_to_update = []
        # Iterate through each category.
        for row in category_df.index:
            cat_id = int(category_df['id'][row])
            cat_name = category_df['description'][row]
            # Skip if category exists and is up to date.
            if cat_id in cats_by_id:
                if cats_by_id[cat_id].name == cat_name:
                    continue
            # If updated add to update list.
            if cat_id in cats_by_id:
                cat_to_update = cats_by_id[cat_id]
                cat_to_update.name = cat_name
                cats_to_update.append(cat_to_update)
                continue
            # If new add to create list.
            cat_to_create = USDACategory(usdacategory_id=cat_id, name=cat_name)
            cats_to_create.append(cat_to_create)
        try:
            fields = ['name']
            USDACategory.objects.bulk_update(cats_to_update, fields)
            USDACategory.objects.bulk_create(cats_to_create)
        except:
            return self.stdout.write(self.style.ERROR(
                f'Failed to update or create usda categories: {NameError}'
            ))
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced categories!'))
        return 'Success'

    @transaction.atomic
    def sync_foods(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        food_cols = ['fdc_id', 'description', 'data_type', 'food_category_id']
        food_dtypes = {
            'fdc_id': np.float,
            'description': np.str,
            'data_type': np.str,
            'food_category_id': np.float
        }
        try:
            food_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food.csv',
                usecols=food_cols,
                dtype=food_dtypes)
        except:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync foods: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food.csv'
            ))
        # Get food data from other csvs
        # dicts
        upc_by_fdc = self.get_upc_by_fdc()
        servings_by_fdc = self.get_servings_by_fdc()
        # list
        fdc_ids_with_nutrition_facts = self.get_fdc_ids_with_nutrition_facts()

        # Get data from db that you will need to sync foods:
        foods_by_fdc = {
            food.fdc_id: food for food in Food.objects.all().prefetch_related(
                'usdafoods') if food.fdc_id}
        foods_by_name = {
            food.name: food for food in Food.objects.all().prefetch_related(
                'usdafoods')}
        gram = Unit.objects.get(name="gram")

        print("preloaded all food sync data")

        # Create lists to perform bulk operations from.
        foods_to_create = []
        foods_to_update = []
        usdafoods_to_create = []
        usdacategory_id_count = 0
        # Track fdc_id by food name and foods_to_link_to_usdafoods
        # to link foods to fdc_id later.
        fdc_by_food_name = {}
        foods_to_link_to_usdafoods = []
        for row in food_df.index:
            fdc_id = int(food_df['fdc_id'][row])
            # Skip food if doesn't meet criteria
            skip_food = self.skip_food_is_true(
                row,
                food_df,
                fdc_id,
                fdc_ids_with_nutrition_facts,
                foods_by_name,
                fdc_by_food_name
            )
            if skip_food:
                continue

            # Create food object from df data
            food = self.create_food_object(
                row, food_df, servings_by_fdc, upc_by_fdc, gram)

            # Track to make sure you are using food.csv with
            # food_category_id column data.
            if food.usdacategory_id:
                usdacategory_id_count += 1

            # Track fdc_id by food name for all foods processed by sync.
            # Use this to avoid saving foods with duplicated names
            # and to link foods to fdc_ids later.
            fdc_by_food_name[food.name] = fdc_id

            # Check if food in db with same fdc_id needs to be udpated.
            if fdc_id in foods_by_fdc:
                food_to_update = self.get_food_to_update_by_fdc(
                    foods_by_fdc, food, fdc_id)
                # If food has been updated, add to list.
                if food_to_update:
                    foods_to_update.append(food_to_update)

            # Check if food in db with same name needs to be udpated.
            elif food.name in foods_by_name:
                food_to_update = self.get_food_to_update_by_name(
                    foods_by_name, food
                )
                if food_to_update:
                    foods_to_update.append(food_to_update)
                # If food with name in db doesn't have fdc_id,
                # create usdafood with fdc_id and link to food.
                if not foods_by_name[food.name].usdafoods.exists():
                    usdafoods_to_create.append(USDAFood(fdc_id=fdc_id))
                    foods_to_link_to_usdafoods.append(food_to_update)

            # If food is new, add to foods_to_link_to_usdafoods after new
            # foods are bulk created and have ids set.
            else:
                fdc_by_food_name[food.name] = fdc_id
                usdafoods_to_create.append(USDAFood(fdc_id=fdc_id))
                foods_to_create.append(food)

        print("finished processing food.csv")
        # Throw error if using food.csv without food_category_id column data.
        if usdacategory_id_count == 0:
            return self.stdout.write(self.style.ERROR(
                "Failed to sync foods: Check that nutrient.csv contains \
                food_category_id records for at least one row."
            ))
        self.update_or_create_new_foods(
            foods_to_create,
            foods_to_update,
            usdafoods_to_create,
            foods_to_link_to_usdafoods,
            fdc_by_food_name
        )
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced foods!'))
        return 'Success'

    @transaction.atomic
    def sync_nutrition_facts(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        fn_cols = ['fdc_id', 'nutrient_id', 'amount']
        fn_dtypes = {
            'fdc_id': np.float,
            'nutrient_id': np.float,
            'amount': np.float,
        }
        try:
            food_nutrient_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_nutrient.csv',
                usecols=fn_cols,
                dtype=fn_dtypes)
        # Throw error if csvs are not uploaded.
        except NameError:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync nutrition facts: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food_nutrient.csv'
            ))

        # Get all data you'll need from db to perform the sync.
        nutrients_by_usdanutrient_id = {}
        all_nutrients = Nutrient.objects.all().prefetch_related(
            'usdanutrients')
        for nutrient in all_nutrients:
            for usdanutrient in nutrient.usdanutrients.all():
                nutrients_by_usdanutrient_id[
                    usdanutrient.usdanutrient_id] = nutrient

        foods_by_fdc = {
            food.fdc_id: food for food in Food.objects.all().prefetch_related(
                'usdafoods') if food.fdc_id}

        unit_conversions_dict = self.get_unit_conversions_dict()

        # This will collapse all IU under IU, but we'll skip those anyway
        # because they are special cases.
        unit_by_usdanutrient_id = self.get_unit_by_usdanutrient_id()

        units_by_abbr = {unit.abbr: unit for unit in Unit.objects.all()}

        print("Retrieved all data for nutrition fact sync!")

        # Create dict to aggregate nutrition facts for usdanutrients
        # tied to same nutrient in our database.
        nutrient_qtys = {}
        for row in food_nutrient_df.index:
            fdc_id = int(food_nutrient_df['fdc_id'][row])
            usdanutrient_id = int(food_nutrient_df['nutrient_id'][row])
            amount = int(food_nutrient_df['amount'][row])
            skip_nutrition_fact = self.skip_nutrition_fact_is_true(
                fdc_id,
                foods_by_fdc,
                usdanutrient_id,
                nutrients_by_usdanutrient_id,
                amount
            )
            if skip_nutrition_fact:
                continue
            nutrient_qty = self.get_nutrient_qty(
                row,
                food_nutrient_df,
                unit_by_usdanutrient_id,
                nutrients_by_usdanutrient_id,
                unit_conversions_dict,
                units_by_abbr,
                foods_by_fdc
            )
            # Aggregate nutrient_qty for each usdanutrient_id by nutrient_id.
            # Since there are multiple usda nutrients to our one nutrient
            # we will want to add the nutrient qty to the total nutrient qty
            # of the food/nutrient pair if we have already tracked a nutrient
            # qty for said food/nutrient pair.
            # ex different types of omega-3s that all add up to the total
            # omega-3s in a food, so we would want to add nutrient qtys to
            # find total.
            food = foods_by_fdc[fdc_id]
            nutrient = nutrients_by_usdanutrient_id[usdanutrient_id]
            if food.id in nutrient_qtys:
                if nutrient.id in nutrient_qtys[food.id]:
                    nutrient_qtys[food.id][nutrient.id] += nutrient_qty
                else:
                    nutrient_qtys[food.id][nutrient.id] = nutrient_qty

            else:
                nutrient_qtys[food.id] = {}
                nutrient_qtys[food.id][nutrient.id] = nutrient_qty
        print("finished processing food_nutrient.csv!")
        nutrition_facts_dict = self.get_nutrition_facts_dict()
        nutrition_facts_to_create = []
        nutrition_facts_to_update = []
        for food_id in nutrient_qtys:
            for nutrient_id in nutrient_qtys[food_id]:
                nutrient_qty = nutrient_qtys[food_id][nutrient_id]
                existing_fact = None
                if food_id in nutrition_facts_dict:
                    if nutrient_id in nutrition_facts_dict[food_id]:
                        existing_fact = nutrition_facts_dict[
                            food_id
                        ][
                            nutrient_id
                        ]
                # If nutrition fact exists and is updated, add to list.
                if existing_fact is not None:
                    if (
                        round(float(existing_fact.nutrient_qty), 2) !=
                        round(float(nutrient_qty), 2)
                    ):
                        nutrition_facts_to_update.append(NutritionFact(
                            id=existing_fact.id,
                            nutrient_qty=nutrient_qty
                        ))
                # Else create new nutrition fact and add to list.
                else:
                    nutrition_facts_to_create.append(NutritionFact(
                        id=existing_fact.id,
                        food_id=food_id,
                        nutrient_id=nutrient_id,
                        nutrient_qty=nutrient_qty
                    ))
        print("finished preparing nutrition facts to create and update!")
        fact_fields = ['nutrient_qty']
        print(f'{len(nutrition_facts_to_update)} facts to update')
        NutritionFact.objects.bulk_update(
            nutrition_facts_to_update, fact_fields, batch_size=100)
        print('nutrition facts updated!')
        print(f'{len(nutrition_facts_to_create)} facts to create')
        NutritionFact.objects.bulk_create(nutrition_facts_to_create)
        print('nutrition facts created!')
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced nutrition facts!'))
        return 'Success'

    def handle(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.

        # # 1. Sync categories
        sync_status = self.sync_categories()
        if sync_status != 'Success':
            return

        # # 2. Sync foods with barcodes and serving size
        sync_status = self.sync_foods()
        if sync_status != 'Success':
            return

        # 3. Sync nutrition facts
        sync_status = self.sync_nutrition_facts()
        if sync_status != 'Success':
            return

        self.stdout.write(self.style.SUCCESS(
            'Successfully synced categories, foods and nutrition facts!'))
