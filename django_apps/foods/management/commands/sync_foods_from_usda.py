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

            one_serving_display_qty = round(
                float(food_portion_df['amount'][row]), 2)
            # If value is NaN, set a None
            if math.isnan(one_serving_display_qty):
                one_serving_display_qty = None
            fdc_id = int(food_portion_df['fdc_id'][row])
            servings_by_fdc[fdc_id] = {}
            servings_by_fdc[fdc_id]['display_unit'] = (
                str(food_portion_df['portion_description'][row])[:29]
                if food_portion_df['portion_description'][row] !=
                'Quantity not specified' else
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
            # Collect serving info
            one_serving_qty = servings_by_fdc[fdc_id]['qty']
            one_serving_unit = servings_by_fdc[fdc_id]['unit']
            one_serving_display_qty = servings_by_fdc[fdc_id]['display_qty']
            one_serving_display_unit = servings_by_fdc[fdc_id]['display_unit']
            usdacategory_id = None
            try:
                usdacategory_id = int(food_df['food_category_id'][row])
                usdacategory_id = (
                    usdacategory_id
                    if usdacategory_id in usdacategory_ids else
                    None
                )
            except:
                pass
            # Skip if food name has already been iterated.
            # There are multiple fcd_ids for foods
            # with identical upc_codes (bar codes) and names.
            # We will just take whatever comes first since it should
            # still be tied to all the same info like upc_code etc.
            if name in fdc_id_by_food_names:
                continue
            # If name hasn't been iterated, add it to list to record iteration
            # now and use to link foods to fdc_id later.
            fdc_id_by_food_names[name] = fdc_id
            # If usdafood record is new, add usdafood with fdc_id to create list.
            if fdc_id not in usdafoods_by_fdc:
                new_usdafood = USDAFood(fdc_id=fdc_id)
                usdafoods_to_create.append(new_usdafood)
            upc_code = upc_by_fdc[fdc_id] if fdc_id in upc_by_fdc else None

            # Some food.csv from usda don't have category ids.
            # Make sure you are using a csv with category ids.
            if usdacategory_id:
                usdacategory_id_count += 1

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
