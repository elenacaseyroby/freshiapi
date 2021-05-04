import pandas as pd
import numpy as np
from django.db import transaction
from django.core.management.base import BaseCommand
from django_apps.foods.models import (
    USDACategory,
    USDAFood,
    Food,
    FoodUSDAFood,
    Nutrient,
    NutritionFact,
    UnitConversion,
    Unit
)

import math


class Command(BaseCommand):
    """
    These methods sacrifice readability in favor of performance.
    """
    help = 'Sync foods from USDA food and nutrient data sets.'

    food_attributes_to_update = ['upc_code',]

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
        category_ids_by_keyword['egg '] = 1
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
        category_ids_by_keyword[' hog '] = 10
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
        category_ids_by_keyword[' ray'] = 15
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
        category_ids_by_keyword[' cod'] = 15
        category_ids_by_keyword[' eel'] = 15
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
        category_ids_by_keyword[' hen'] = 5
        category_ids_by_keyword['pheasant'] = 5
        category_ids_by_keyword[' dove'] = 5
        # Snack
        category_ids_by_keyword[' dip'] = 23
        category_ids_by_keyword['chips'] = 23
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
        category_ids_by_keyword[' ham '] = 7
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
        category_ids_by_keyword[' bar'] = 8
        category_ids_by_keyword['smoothie'] = 8
        category_ids_by_keyword['oatmeal'] = 8
        category_ids_by_keyword['granola'] = 8
        category_ids_by_keyword['kashi'] = 8
        category_ids_by_keyword['kellogs'] = 8
        category_ids_by_keyword['cereal'] = 8
        category_ids_by_keyword['bran '] = 8
        category_ids_by_keyword['waffle'] = 8
        category_ids_by_keyword['toast '] = 8
        # Grains
        category_ids_by_keyword['noodles'] = 20
        category_ids_by_keyword['pasta'] = 20
        category_ids_by_keyword['macaroni'] = 20
        category_ids_by_keyword['spaghetti'] = 20
        category_ids_by_keyword[' rice'] = 20
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
        category_ids_by_keyword[' pie'] = 19
        category_ids_by_keyword['turnover'] = 19
        category_ids_by_keyword['cobbler'] = 19
        # Nut and seed
        category_ids_by_keyword[' nut'] = 12
        category_ids_by_keyword['seed'] = 12
        # Beverage
        category_ids_by_keyword[' tea '] = 14
        category_ids_by_keyword['drink'] = 14
        # Fruit & Juice
        fruits = [
            'apple', 'mango', 'pinapple', 'pear', 'berries',
            'peach', 'pomegranate', 'banana', 'grape', 'tomato',
            'lime', 'lemon', 'guava', 'papaya', 'passion fruit',
            'nectar', 'cantaloupe', 'melon'
        ]
        for fruit in fruits:
            category_ids_by_keyword[fruit] = 9
        # Veggie
        veggies = [
            'vegetable protein', 'chard', 'broccoli', 'broccolini',
            'beet', 'kale', 'mushroom', 'corn', 'bok choy', 'cabbage',
            'lettuce', 'spinach', 'pepper', 'onion', 'collard', 'greens',
            'turnip', 'radish', 'watercress', 'carrot', 'pea', 'potato',
            'cucumber', 'celery', 'fennel', 'squash', 'seaweed', 'artichoke',
            'asparagus', 'sprouts', 'cauliflower', 'okra', 'plantain', ' yam',
            'sweet potato'
        ]
        for veggie in veggies:
            category_ids_by_keyword[veggie] = 11

        name = str(name).lower().strip()

        # If category is branded food, but food is named
        # for ex. "broccoli" or "apple"
        # put in fruits or veggies category.
        if usdacategory_id == 26:
            if name in veggies:
                return 11
            if name in fruits:
                return 9

        # If category set return category
        if usdacategory_id:
            return int(usdacategory_id)

        # 2. If data type is meaningful return category based on that.
        if data_type in category_ids_by_data_type:
            return int(category_ids_by_data_type[data_type])

        # 3. If name contains keywords return category based on that.
        for keyword in category_ids_by_keyword:
            if keyword in name:
                return int(category_ids_by_keyword[keyword])

        return None

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
                '''Failed to sync foods: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3:
                food_portion.csv'''
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
        fdc_ids_with_nutrition_facts,
    ):
        # Skip if food doesn't have associated nutrition_facts
        if fdc_id not in fdc_ids_with_nutrition_facts:
            return True

        # Skip about 200 entries like this:
        # "328216","sub_sample_food","Niacin, Cheese,...
        # "328217","sub_sample_food","Proximates, Cheese,...
        data_type = str(food_df['data_type'][row])
        name = food_df['description'][row][:99]
        if (
            data_type == 'sub_sample_food' and
            ', Cheese' in name
        ):
            return True
        return False

    def get_valid_food_name(self, description):
        desc = description.lower()
        # Cut off anything past these words:
        desc = desc.split(" -")[0].strip()
        desc = desc.split("- ")[0].strip()
        desc = desc.split(" ns ")[0].strip()
        desc = desc.split(" yes ")[0].strip()
        desc = desc.split("region")[0].strip()
        desc = desc.split(", pass ")[0].strip()
        desc = desc.split("n/a")[0].strip()
        desc = desc.split("(")[0].strip()

        # Remove bad descriptors
        bad_descriptors = [
            'folate', 'minerals', 'tdf', 'niacin',
            'fatty acids', 'selenium', 'vitamin c', 'vitamin k',
            'carotenoids', 'proximates']
        for bad_descriptor in bad_descriptors:
            if bad_descriptor in desc:
                desc = desc.lstrip(bad_descriptor).strip()
        # Only include first 4 sections
        measurements = [
            ' oz', 'oz.', ' lb', ' qt', ' ct', ' count', ' pc',
            ' piece', ' fl oz', ' ounce', ' pound', ' fluid ounces']
        descriptors = desc.split(",")
        name = ''
        for count, descriptor in enumerate(descriptors):
            descriptor = descriptor.strip()
            if count == 0 or name == '':
                name = descriptor
            elif descriptor != '':
                # skip descriptors containing measurements
                # if not first descriptor.
                contains_measurements = False
                for measurement in measurements:
                    if measurement in descriptor:
                        contains_measurements = True
                if not contains_measurements:
                    name = f'{name}, {descriptor}'

            if count >= 3:
                break
        return name[:99]

    def create_food_object(
            self, row, food_df, servings_by_fdc, upc_by_fdc, gram):
        food = Food()
        fdc_id = food_df['fdc_id'][row]
        data_type = food_df['data_type'][row]
        description = food_df['description'][row]
        food.name = self.get_valid_food_name(description)
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
            food.upc_code = (
                upc_by_fdc[fdc_id]
                if fdc_id in upc_by_fdc else
                None
            )
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
        # don't update name if changes.
        for prop in self.food_attributes_to_update:
            if getattr(updated_food, prop) != getattr(food_in_db, prop):
                return False
        return True

    def get_food_to_update_by_fdc(self, foods_by_fdc, food, fdc_id):
        if fdc_id not in foods_by_fdc:
            return None
        food_in_db = foods_by_fdc[fdc_id]
        food_updated = self.food_updated_is_true(food, food_in_db)
        if not food_updated:
            return None
        # Don't update category to none if category exists in db
        if (
            food.usdacategory_id is None and
            food_in_db.usdacategory_id is not None
        ):
            food.usdacategory_id = food_in_db.usdacategory_id
        food.id = food_in_db.id
        # don't update name
        food.name = food_in_db.name
        return food

    def get_food_to_update_by_name(self, foods_by_name, food):
        if food.name not in foods_by_name:
            return None
        food_in_db = foods_by_name[food.name]
        food_updated = self.food_updated_is_true(food, food_in_db)
        if not food_updated:
            return None
        # Don't update category to none if category exists in db
        if (
            food.usdacategory_id is None and
            food_in_db.usdacategory_id is not None
        ):
            food.usdacategory_id = food_in_db.usdacategory_id
        food.id = food_in_db.id
        return food

    def update_or_create_new_foods(
        self,
        foods_to_create,
        foods_to_update,
        usdafoods_to_create,
        foods_to_link_to_usdafoods,
        fdcs_by_food_name
    ):
        # Create and update food and usdafood objects.
        print(f'{len(foods_to_update)} foods to update')
        Food.objects.bulk_update(foods_to_update, self.food_attributes_to_update, batch_size=100)
        print('updated foods!')
        print(f'{len(foods_to_create)} foods to create')
        new_usdafoods = USDAFood.objects.bulk_create(
            usdafoods_to_create, batch_size=100)
        print('created usdafoods!')
        new_foods = Food.objects.bulk_create(foods_to_create, batch_size=100)
        print('created foods!')
        # Add new foods with ids to foods_to_link_to_usdafoods.
        foods_to_link_to_usdafoods.extend(new_foods)
        udsafoods_by_fdc = {uf.fdc_id: uf for uf in new_usdafoods}
        foods_usdafoods_to_create = []
        fdc_ids_commited_in_sync = []
        for food in foods_to_link_to_usdafoods:
            for fdc_id in fdcs_by_food_name[food.name]:
                # Skip if fdc_id is not new to the db or
                # if already added to list to be committed:
                if (
                    fdc_id not in udsafoods_by_fdc or
                    fdc_id in fdc_ids_commited_in_sync
                ):
                    continue

                usdafood = udsafoods_by_fdc[fdc_id]
                foods_usdafoods_to_create.append(
                    FoodUSDAFood(food=food, usdafood=usdafood)
                )
                # Track fdc_ids already added to be committed
                # in this sync.
                fdc_ids_commited_in_sync.append(fdc_id)
        FoodUSDAFood.objects.bulk_create(
            foods_usdafoods_to_create, batch_size=100)
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
                '''Failed to sync foods: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3:
                market_acquisition.csv'''
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
                '''Failed to sync nutrition facts: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3:
                nutrient.csv'''
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
                '''Failed to sync nutrition facts: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3:
                food_nutrient.csv'''
            ))
        fdc_ids = [int(food_nutrient_df['fdc_id'][row])
                   for row in food_nutrient_df.index]
        return fdc_ids

    @transaction.atomic
    def batch_sync_foods(
        self,
        food_batch_df,
        upc_by_fdc,
        servings_by_fdc,
        fdc_ids_with_nutrition_facts,
        gram,
        foods_by_fdc,
        foods_by_name,
    ):
        # Create lists to perform bulk operations from.
        foods_to_create = []
        foods_to_update = []
        usdafoods_to_create = []
        # Track fdc_id by food name and foods_to_link_to_usdafoods
        # to link foods to fdc_id later.
        fdcs_by_food_name = {}
        foods_to_link_to_usdafoods = []
        for row in food_batch_df.index:
            fdc_id = int(food_batch_df['fdc_id'][row])
            print(fdc_id)
            # Skip food if doesn't meet criteria
            skip_food = self.skip_food_is_true(
                row,
                food_batch_df,
                fdc_id,
                fdc_ids_with_nutrition_facts
            )
            if skip_food:
                continue

            # Create food object from df data
            food = self.create_food_object(
                row, food_batch_df, servings_by_fdc, upc_by_fdc, gram)

            # Match on fdc_id in database
            if fdc_id in foods_by_fdc:
                food_to_update = self.get_food_to_update_by_fdc(
                    foods_by_fdc, food, fdc_id)
                # If food has been updated, add to list.
                if food_to_update:
                    foods_to_update.append(food_to_update)

            # Match on name in database
            elif food.name in foods_by_name:
                food_to_update = self.get_food_to_update_by_name(
                    foods_by_name, food
                )
                if food_to_update:
                    foods_to_update.append(food_to_update)
                # Create usdafood record for fdc_id
                usdafoods_to_create.append(USDAFood(fdc_id=fdc_id))
                # Add to list to link to this food
                foods_to_link_to_usdafoods.append(foods_by_name[food.name])
                # Store fdc_id by food_name to link later
                if food.name not in fdcs_by_food_name:
                    fdcs_by_food_name[food.name] = []
                fdcs_by_food_name[food.name].append(fdc_id)
            # Match on name of food that has already been processed
            # in this sync.
            elif food.name in fdcs_by_food_name:
                usdafoods_to_create.append(USDAFood(fdc_id=fdc_id))
                # Store fdc_id by food_name to link later
                # Since food is new, it will be added to
                # foods_to_linke_to_usdafoods after bulk_created.
                fdcs_by_food_name[food.name].append(fdc_id)
            # Else, food is new and must be created.
            else:
                print("new food!")
                foods_to_create.append(food)
                usdafoods_to_create.append(USDAFood(fdc_id=fdc_id))
                # Store fdc_id by food_name to link later
                # Add to foods_to_link_to_usdafoods
                # after new foods are bulk created and have ids set.
                fdcs_by_food_name[food.name] = []
                fdcs_by_food_name[food.name].append(fdc_id)
        self.update_or_create_new_foods(
            foods_to_create,
            foods_to_update,
            usdafoods_to_create,
            foods_to_link_to_usdafoods,
            fdcs_by_food_name
        )

    def get_usdanutrient_amounts(
        self,
        food_nutrient_df,
        foods_by_fdc_id,
        nutrients_by_usdanutrient_id
    ):
        nutrient_amounts = {}
        for row in food_nutrient_df.index:
            fdc_id = int(food_nutrient_df['fdc_id'][row])
            usdanutrient_id = int(food_nutrient_df['nutrient_id'][row])
            amount = int(food_nutrient_df['amount'][row])
            # Skip if fdc not associated w food in our db.
            if fdc_id not in foods_by_fdc_id:
                continue
            # Skip if usdanutrient_id not associated w nutrient in our db.
            if usdanutrient_id not in nutrients_by_usdanutrient_id:
                continue
            # Skip if no nutrient_amount
            if (
                amount == 0 or
                math.isnan(amount)
            ):
                continue
            food = foods_by_fdc_id[fdc_id]
            if food.id not in nutrient_amounts:
                nutrient_amounts[food.id] = {}
            # Flatten so only most recent amount for usdanutrient and food
            # is stored. Do not aggregate.
            nutrient_amounts[food.id][usdanutrient_id] = amount
        return nutrient_amounts

    def aggregate_nutrient_qty(
        self,
        nutrient_amounts,
        conversions,
        nutrients_by_usdanutrient_id,
        units_by_abbr,
        foods_by_id
    ):
        # Aggregate nutrient_qty for each usdanutrient_id by nutrient_id.
        # Since there are multiple usda nutrients to our one nutrient
        # we will want to add the nutrient qty to the total nutrient qty
        # of the food/nutrient pair if we have already tracked a nutrient
        # qty for said food/nutrient pair.
        # ex different types of omega-3s that all add up to the total
        # omega-3s in a food, so we would want to add nutrient qtys to
        # find total.
        unit_by_usdanutrient_id = self.get_unit_by_usdanutrient_id()
        nutrient_qtys = {}
        for food_id in nutrient_amounts:
            if food_id not in nutrient_qtys:
                nutrient_qtys[food_id] = {}
            for usdanutrient_id in nutrient_amounts[food_id]:
                nutrient = nutrients_by_usdanutrient_id[usdanutrient_id]
                usdanutrient_amount = nutrient_amounts[
                    food_id
                ][
                    usdanutrient_id
                ]
                from_unit = unit_by_usdanutrient_id[usdanutrient_id]
                to_unit_id = nutrient.dv_unit_id
                # If usdanutrient unit and nutrient unit exist and are
                # different, convert to nutrient unit from usdanutrient
                # unit.
                if (
                    from_unit is not None and
                    to_unit_id is not None and
                    from_unit.id != to_unit_id

                ):
                    usdanutrient_qty = usdanutrient_amount * \
                        conversions[from_unit.id][to_unit_id]
                # If usda nutrient or nutrient doesn't have unit
                # then don't convert based on nutrient unit. Or
                # if units are equal and no conversion is necessary
                # Ex. Calories don't have a unit in our system
                else:
                    usdanutrient_qty = usdanutrient_amount

                # Convert from nutrient_qty per 100g of food
                # to nutrient_qty per one serving of food.
                food = foods_by_id[food_id]
                to_food_qty = food.one_serving_qty
                to_food_unit_id = food.one_serving_unit_id
                from_food_qty = 100
                from_food_unit_id = units_by_abbr['g'].id
                # If units are the same, don't convert.
                if from_food_unit_id == to_food_unit_id:
                    from_food_qty_in_to_unit = from_food_qty
                # Else, convert.
                else:
                    from_food_qty_in_to_unit = (
                        from_food_qty *
                        conversions[from_food_unit_id][to_food_unit_id]
                    )
                nutrient_qty = usdanutrient_qty * \
                    (to_food_qty / from_food_qty_in_to_unit)
                if nutrient.id not in nutrient_qtys[food_id]:
                    nutrient_qtys[food_id][nutrient.id] = nutrient_qty
                else:
                    nutrient_qtys[food_id][nutrient.id] += nutrient_qty
        return nutrient_qtys

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
                '''Failed to sync categories: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3: food_category.csv'''
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
            cat_to_create = USDACategory(
                usdacategory_id=cat_id, name=cat_name)
            cats_to_create.append(cat_to_create)
        try:
            fields = ['name']
            USDACategory.objects.bulk_update(
                cats_to_update, fields, batch_size=100)
            USDACategory.objects.bulk_create(cats_to_create, batch_size=100)
        except:
            return self.stdout.write(self.style.ERROR(
                f'Failed to update or create usda categories: {NameError}'
            ))
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced categories!'))
        return 'Success'

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
                '''Failed to sync foods: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3:
                food.csv'''
            ))
        # Get food data from other csvs
        # dicts
        upc_by_fdc = self.get_upc_by_fdc()
        servings_by_fdc = self.get_servings_by_fdc()
        # list
        fdc_ids_with_nutrition_facts = self.get_fdc_ids_with_nutrition_facts()

        # Get data from db that you will need to sync foods:
        gram = Unit.objects.get(name="gram")

        print("preloaded all food sync data")

        foods_count = len(food_df.index)
        batch_size = 50000
        from_index = 0
        # Iterate through foods.csv in reverse so
        # fruits and veggies categorized first.
        while from_index < foods_count:
            to_index = from_index + batch_size
            if to_index > foods_count:
                to_index = foods_count
            # Refresh dicts with foods from db.
            foods_by_fdc = {
                fuf.usdafood.fdc_id: fuf.food for fuf in
                FoodUSDAFood.objects.all().prefetch_related(
                    'food', 'usdafood')}
            foods_by_name = {
                food.name: food for food in Food.objects.all(
                ).prefetch_related('usdafoods')}
            food_batch_df = food_df.iloc[from_index:to_index]
            self.batch_sync_foods(
                food_batch_df,
                upc_by_fdc,
                servings_by_fdc,
                fdc_ids_with_nutrition_facts,
                gram,
                foods_by_fdc,
                foods_by_name
            )
            print(
                f'''finished processing food.csv batch row
                {from_index} to row {to_index}'''
            )
            from_index = to_index
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
                '''Failed to sync nutrition facts: Please make
                sure the following USDA FoodData Central csvs
                are uploaded to the freshi-app/food-sync-csvs
                bucket in AWS S3:
                food_nutrient.csv'''
            ))

        # Get all data you'll need from db to perform the sync.
        nutrients_by_usdanutrient_id = {}
        all_nutrients = Nutrient.objects.all().prefetch_related(
            'usdanutrients')
        for nutrient in all_nutrients:
            for usdanutrient in nutrient.usdanutrients.all():
                nutrients_by_usdanutrient_id[
                    usdanutrient.usdanutrient_id] = nutrient

        foods_by_fdc_id = {
            fuf.usdafood.fdc_id: fuf.food for fuf in
            FoodUSDAFood.objects.all().prefetch_related(
                'food', 'usdafood')}

        conversions = self.get_unit_conversions_dict()
        # This will collapse all IU under IU, but we'll skip those anyway
        # because they are special cases.
        units_by_abbr = {unit.abbr: unit for unit in Unit.objects.all()}
        foods_by_id = {food.id: food for food in Food.objects.all()}
        print("Retrieved all data for nutrition fact sync!")

        usdanutrient_amounts = self.get_usdanutrient_amounts(
            food_nutrient_df,
            foods_by_fdc_id,
            nutrients_by_usdanutrient_id
        )
        nutrient_qtys = self.aggregate_nutrient_qty(
            usdanutrient_amounts,
            conversions,
            nutrients_by_usdanutrient_id,
            units_by_abbr,
            foods_by_id
        )
        print("finished processing food_nutrient.csv!")

        nutrition_facts = self.get_nutrition_facts_dict()
        nutrition_facts_to_create = []
        nutrition_facts_to_update = []
        for food_id in nutrient_qtys:
            for nutrient_id in nutrient_qtys[food_id]:
                nutrient_qty = nutrient_qtys[food_id][nutrient_id]
                # Skip if nutrient_qty is None or 0:
                if nutrient_qty is None or nutrient_qty == 0:
                    continue
                existing_fact = None
                if food_id in nutrition_facts:
                    if nutrient_id in nutrition_facts[food_id]:
                        existing_fact = nutrition_facts[
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
        NutritionFact.objects.bulk_create(
            nutrition_facts_to_create, batch_size=100)
        print('nutrition facts created!')
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced nutrition facts!'))
        return 'Success'

    def handle(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket./

        # 1. Sync categories
        sync_status = self.sync_categories()
        if sync_status != 'Success':
            return

        # 2. Sync foods with barcodes and serving size
        # TODO: Currently once an fdc_id has been assigned
        # to a food in our system, it does not get reassigned to
        # a different food.  This could be bad if we change the
        # get_valid_food_name function since it could create new food
        # objects that would need their fdc_ids reassigned to them.
        sync_status = self.sync_foods()
        if sync_status != 'Success':
            return

        # 3. Sync nutrition facts
        sync_status = self.sync_nutrition_facts()
        if sync_status != 'Success':
            return

        self.stdout.write(self.style.SUCCESS(
            'Successfully synced categories, foods and nutrition facts!'))
