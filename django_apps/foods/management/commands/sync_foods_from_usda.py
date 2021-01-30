import pandas as pd
from django.db import models
from django.core.management.base import BaseCommand
from django_apps.foods.models import (
    USDACategory,
    USDAFood,
    Food, Unit,
    FoodUSDAFood,
    Nutrient,
    NutritionFact
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
        # Branded
        category_ids_by_keyword['gerber'] = 26
        category_ids_by_keyword['formula'] = 17
        category_ids_by_keyword['baby food'] = 17
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

    def sync_foods(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        try:
            food_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food.csv')
            food_portion_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_portion.csv')
            market_acquisition_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/market_acquisition.csv')
        # Throw error if csvs are not uploaded.
        except:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync foods: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food.csv,\
                food_portion.csv, market_acquisition.csv'
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

        # Create dict to sort serving_size by fdc_id
        # serving_size = {'qty': , 'unit': ,'display_qty': , 'display_unit': }
        grams = Unit.objects.get(name="gram")
        servings_by_fdc = {}
        for row in food_portion_df.index:
            one_serving_qty = round(float(
                food_portion_df['gram_weight'][row]), 2)
            # Skip foods with negative and thus inaccurate
            # serving qty.
            if one_serving_qty <= 0:
                continue

            one_serving_display_qty = (
                round(float(food_portion_df['amount'][row]), 2)
                if not food_portion_df['amount'][row] else
                None
            )
            fdc_id = int(food_portion_df['fdc_id'][row])
            servings_by_fdc[fdc_id] = {}
            servings_by_fdc[fdc_id]['display_unit'] = (
                str(food_portion_df['portion_description'][row])[:29]
                if (
                    food_portion_df['portion_description'][row] != 'Quantity not specified' and
                    not food_portion_df['portion_description'][row]
                )else
                None
            )
            servings_by_fdc[fdc_id]['display_qty'] = one_serving_display_qty
            servings_by_fdc[fdc_id]['unit'] = grams
            servings_by_fdc[fdc_id]['qty'] = one_serving_qty

        # Store usdafoods by fdc_id.
        all_usdafoods = USDAFood.objects.all()
        usdafoods_by_fdc = {
            usdafood.fdc_id: usdafood for usdafood in all_usdafoods}

        # Store foods by fdc_id.
        all_foods = Food.objects.all()
        foods_by_fdc = {food.fdc_id: food for food in all_foods}

        # Get usdacategory ids in our system
        usdacategory_ids = [i for i in USDACategory.objects.all().values_list(
            'usdacategory_id', flat=True)]

        # Iterate through foods to update/create foods and usdafoods
        foods_to_create = []
        foods_to_update = []
        usdafoods_to_create = []
        foods_usdafoods_to_create = []
        usdacategory_id_count = 0
        # Track food name by fdc_id to link foods to fdc_id later.
        fdc_id_by_food_names = {}
        for row in food_df.index:
            # Collect food properties.
            fdc_id = int(food_df['fdc_id'][row])
            name = food_df['description'][row][:99]
            # Skip if food doesn't have associated serving sizes.
            if fdc_id not in servings_by_fdc:
                continue
            data_type = str(food_df['data_type'][row])
            # Skip food if should be weeded out of data set.
            if self.weed_out_food(data_type, name, fdc_id_by_food_names):
                continue
            # Collect serving info
            one_serving_qty = servings_by_fdc[fdc_id]['qty']
            one_serving_unit = servings_by_fdc[fdc_id]['unit']
            one_serving_display_qty = servings_by_fdc[fdc_id]['display_qty']
            one_serving_display_unit = servings_by_fdc[fdc_id]['display_unit']
            usdacategory_id = (
                None
                if math.isnan(food_df['food_category_id'][row]) else
                int(food_df['food_category_id'][row])
            )
            usdacategory_id = self.get_category_id(
                data_type, usdacategory_id, name)

            # If usdafood record is new, add usdafood with fdc_id to create list.
            if fdc_id not in usdafoods_by_fdc:
                new_usdafood = USDAFood(fdc_id=fdc_id)
                usdafoods_to_create.append(new_usdafood)
            upc_code = upc_by_fdc[fdc_id] if fdc_id in upc_by_fdc else None

            # Some food.csv from usda don't have category ids.
            # Make sure you are using a csv with category ids.
            if usdacategory_id:
                usdacategory_id_count += 1

            # Add to list and use to link foods to fdc_id later.
            fdc_id_by_food_names[name] = fdc_id

            # If food exists in db
            if fdc_id in foods_by_fdc:
                food = foods_by_fdc[fdc_id]
                # Skip if food exists and is up to date.
                if (
                    food.name == name
                    and food.usdacategory_id == usdacategory_id
                    and food.upc_code == upc_code
                    and food.one_serving_qty == one_serving_qty
                    and food.one_serving_unit == one_serving_unit
                    and food.one_serving_display_qty == one_serving_display_qty
                    and food.one_serving_display_unit ==
                    one_serving_display_unit
                ):
                    continue
                # Add to foods to update if changes have been made.
                food.name = name
                food.usdacategory_id = usdacategory_id
                food.upc_code = upc_code
                food.one_serving_qty = one_serving_qty
                food.one_serving_unit = one_serving_unit
                food.one_serving_display_qty = one_serving_display_qty
                food.one_serving_display_unit = one_serving_display_unit
                foods_to_update.append(food)
                continue
            # If new, add to create list.
            new_food = Food()
            new_food.name = name
            new_food.usdacategory_id = usdacategory_id
            new_food.upc_code = upc_code
            new_food.one_serving_qty = one_serving_qty
            new_food.one_serving_unit = one_serving_unit
            new_food.one_serving_display_qty = one_serving_display_qty
            new_food.one_serving_display_unit = one_serving_display_unit
            foods_to_create.append(new_food)

        if usdacategory_id_count == 0:
            return self.stdout.write(self.style.ERROR(
                "Failed to sync foods: Check that nutrient.csv contains \
                food_category_id records for at least one row."
            ))
        created_foods = []
        try:
            # 1. Bulk create usdafoods.
            USDAFood.objects.bulk_create(usdafoods_to_create)
            # 2. Bulk update foods
            fields = ['name', 'usdacategory_id', 'upc_code', 'one_serving_qty',
                      'one_serving_unit', 'one_serving_display_qty',
                      'one_serving_display_unit']
            Food.objects.bulk_update(foods_to_update, fields)
            # 3. Bulk create foods
            created_foods = Food.objects.bulk_create(
                foods_to_create)
        except NameError:
            return self.stdout.write(self.style.ERROR(
                f'Failed to bulk create/updates foods and usdafoods:\
                {NameError}'
            ))

        # Store usdafoods by fdc_id.
        all_usdafoods = USDAFood.objects.all()
        usdafoods_by_fdc = {
            usdafood.fdc_id: usdafood for usdafood in all_usdafoods}

        # Interate through created foods to link
        # food ids to fdc_ids by food name (should be distinct)
        foods_usdafoods_to_create = []
        for food in created_foods:
            fdc_id = fdc_id_by_food_names[food.name]
            food_usdafood = FoodUSDAFood(
                food_id=food.id, usdafood=usdafoods_by_fdc[fdc_id])
            foods_usdafoods_to_create.append(food_usdafood)
        try:
            # Bulk create associations between Food and USDAFood
            # to link fdc_ids to foods.
            FoodUSDAFood.objects.bulk_create(foods_usdafoods_to_create)
        except NameError:
            return self.stdout.write(self.style.ERROR(
                f'Failed to bulk create food usda food associations: \
                {NameError}'
            ))
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced foods!'))

    def sync_nutrition_facts(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        try:
            food_nutrient_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_nutrient.csv')
            nutrient_df = pd.read_csv(
                'https://freshi-app.s3.amazonaws.com/food-sync-csvs/nutrient.csv')
        # Throw error if csvs are not uploaded.
        except NameError:
            return self.stdout.write(self.style.ERROR(
                'Failed to sync nutrition facts: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food_nutrient.csv, nutrient.csv'
            ))
        all_units = Unit.objects.all()
        # This will collapse all IU under IU, but we'll skip those anyway
        # because they are special cases.
        units_by_abbr = {unit.abbr: unit for unit in all_units}

        # Store nutrient units by usdanutrient_id.
        unit_by_usdanutrient_id = {}
        for row in nutrient_df.index:
            usdanutrient_id = int(nutrient_df['id'][row])
            unit_name = nutrient_df['unit_name'][row]
            if unit_name == 'G':
                unit = units_by_abbr['g']
            if unit_name == 'MG_ATE':
                unit = units_by_abbr['mg']
            if unit_name == 'MG':
                unit = units_by_abbr['mg']
            if unit_name == 'UG':
                unit = units_by_abbr['ug']
            if unit_name == 'IU':
                unit = units_by_abbr['IU']
            unit_by_usdanutrient_id[usdanutrient_id] = unit

        # Store nutrients by usdanutrient_id.
        all_nutrients = Nutrient.objects.all().prefetch_related(
            'usdanutrients')
        nutrients_by_usdanutrient_id = {}
        for nutrient in all_nutrients:
            for un_id in nutrient.usdanutrient_ids:
                nutrients_by_usdanutrient_id[un_id] = nutrient

        # Store foods by fdc_id.
        all_foods = Food.objects.all()
        foods_by_fdc = {food.fdc_id: food for food in all_foods}

        # Store nutrition facts by "fdc_id - usdanutrient_id"
        all_nutrition_facts = NutritionFact.objects.all().prefetch_related(
            'food.fdc_id', 'nutrient.usdanutrient_ids')
        nutrition_facts_by_id = {}
        for fact in all_nutrition_facts:
            for usdanutrient_id in fact.nutrient.usdanutrient_ids:
                key = f'{fact.food.fcd_id} - {usdanutrient_id}'
                nutrition_facts_by_id[key] = fact

        # Iterate through food_nutrient.csv rows.
        nutrients_to_update = []
        nutrition_facts_to_create = []
        for row in food_nutrient_df.index:
            fdc_id = int(food_nutrient_df['fdc_id'][row])
            usdanutrient_id = int(food_nutrient_df['nutrient_id'][row])
            # nutrient amount is per 100g of food
            nutrient_qty_per_100g = float(food_nutrient_df['gram_weight'][row])
            # Skip if fdc not associated w food in our db.
            if fdc_id not in foods_by_fdc:
                continue
            # Skip if usdanutrient_id not associated w nutrient in our db.
            if usdanutrient_id not in nutrients_by_usdanutrient_id:
                continue
            # Skip if nutrition fact exists.
            key = f'{fdc_id} - {usdanutrient_id}'
            if key in nutrition_facts_by_id:
                continue

            # If nutrient.unit has changed update nutrient.
            # Don't update for:
            # calories, vitamins a, e, c, d
            dont_update_nutrients = [
                'calories',
                'vitamin a',
                'vitamin e',
                'vitamin c',
                'vitamin d',
                'vitamin d2',
                'vitamin d3'
            ]
            nutrient = nutrients_by_usdanutrient_id[usdanutrient_id]
            updated_unit = unit_by_usdanutrient_id[usdanutrient_id]
            if (
                nutrient.name not in dont_update_nutrients
                and nutrient.unit is not updated_unit
            ):
                nutrient.unit = updated_unit
                nutrients_to_update.append(nutrient)

            # Calculate nutrition_fact.nutrient_qty
            food = foods_by_fdc[fdc_id]
            # all usda foods will have one_serving_qty in grams
            # divide by 100g and multiply by nutrient qty per 100g
            # to get nutrient_qty.
            nutrient_qty = nutrient_qty_per_100g * (food.one_serving_qty/100)
            new_nutrition_fact = NutritionFact(
                nutrient_qty=nutrient_qty,
                food=food,
                nutrient=nutrient)
            nutrition_facts_to_create.append(new_nutrition_fact)
        try:
            fields = ['unit']
            Nutrition.objects.bulk_update(nutrients_to_update, fields)
            NutritionFact.objects.bulk_create(nutrition_facts_to_create)
        except NameError:
            return self.stdout.write(self.style.ERROR(
                f'Failed to create new nutrition facts: {NameError}'
            ))
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced nutrition facts!'))

    def handle(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.

        # 1. Sync categories
        self.sync_categories()

        # 2. Sync foods with barcodes and serving size
        self.sync_foods()

        # 3. Sync nutrition facts
        # self.sync_nutrition_facts()

        self.stdout.write(self.style.SUCCESS(
            'Successfully synced categories, foods and nutrition facts!'))
