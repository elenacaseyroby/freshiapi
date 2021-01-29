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


class FoodWithFdcId(Food):
    fdc_id = models.IntegerField()

    class Meta:
        proxy = True


class Command(BaseCommand):
    """
    These methods sacrifice readability in favor of performance.
    """
    help = 'Sync foods from USDA food and nutrient data sets.'

    def sync_categories(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        category_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com\
            /food-sync-csvs/food_category.csv')

        # Throw error if csvs are not uploaded.
        if not category_df:
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
            if cats_by_id[cat_id] and cats_by_id[cat_id].name == cat_name:
                continue
            # If updated add to update list.
            cat_to_update = cats_by_id[cat_id]
            if cats_by_id[cat_id]:
                cat_to_update.name = cat_name
                cats_to_update.append(cat_to_update)
                continue
            # If new add to create list.
            cat_to_create = USDACategory(usdacategory_id=cat_id, name=cat_name)
            cats_to_create.append(cat_to_create)
        try:
            USDACategory.objects.bulk_update(cats_to_update)
            USDACategory.objects.bulk_create(cats_to_create)
        except NameError:
            return self.stdout.write(self.style.ERROR(
                f'Failed to update or create usda categories: {NameError}'
            ))
        self.stdout.write(self.style.SUCCESS(
            'Successfully synced categories!'))

    def sync_foods(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.

        category_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com\
            /food-sync-csvs/food_category.csv')
        food_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com\
            /food-sync-csvs/food.csv')
        food_portion_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com\
            /food-sync-csvs/food_portion.csv')
        market_acquisition_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com\
            /food-sync-csvs/market_acquisition.csv')

        # Throw error if csvs are not uploaded.
        if not (
            category_df
            and food_df
            and food_portion_df
            and market_acquisition_df
        ):
            return self.stdout.write(self.style.ERROR(
                'Failed to sync foods: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food.csv, food_category.csv,\
                food_portion.csv, market_acquisition.csv'
            ))

        upc_by_fdc = {}
        # Create dict to sort upc_code (bar codes) by fdc_id
        for row in market_acquisition_df.index:
            fdc_id = int(market_acquisition_df['fdc_id'][row])
            upc_code = int(market_acquisition_df['upc_code'][row])
            upc_by_fdc[fdc_id] = upc_code

        # Create dict to sort serving_size by fdc_id
        # serving_size = {'qty': , 'unit': ,'display_qty': , 'display_unit': }
        grams = Unit.objects.get(name="gram")
        servings_by_fdc = {}
        for row in food_portion_df.index:
            fdc_id = int(food_portion_df['fdc_id'][row])
            servings_by_fdc[fdc_id]['display_unit'] = \
                food_portion_df['modifier'][row]
            servings_by_fdc[fdc_id]['display_qty'] = \
                int(food_portion_df['amount'][row])
            servings_by_fdc[fdc_id]['unit'] = grams
            servings_by_fdc[fdc_id]['qty'] = \
                int(food_portion_df['gram_weight'][row])

        # Iterate through foods to update/create foods and usdafoods
        all_usdafoods = USDAFood.objects.all()
        usdafoods_by_fdc = {}
        for usdafood in all_usdafoods:
            usdafoods_by_fdc[usdafood.fdc_id] = usdafood
        all_foods = Food.objects.all()
        foods_by_fdc = {}
        for food in all_foods:
            foods_by_fdc[food.fdc_id] = food
        foods_to_create = []
        foods_to_update = []
        usdafoods_to_create = []
        foods_usdafoods_to_create = []
        usdacategory_id_count = 0
        for row in food_df.index:
            fdc_id = int(food_df['fdc_id'][row])
            # If new, add usdafood with fdc_id to create list.
            if not usdafoods_by_fdc[fdc_id]:
                new_usdafood = USDAFood(fdc_id=fdc_id)
                usdafoods_to_create.append(new_usdafood)
            # sync: name, usdacategory_id, one_serving_qty
            # one_serving_unit, one_serving_display_qty,
            # one_serving_display_unit, upc_code
            name = food_df['description'][row]
            upc_code = upc_by_fdc[fdc_id]
            one_serving_qty = servings_by_fdc[fdc_id]['qty']
            one_serving_unit = servings_by_fdc[fdc_id]['unit']
            one_serving_display_qty = servings_by_fdc[fdc_id]['display_qty']
            one_serving_display_unit = servings_by_fdc[fdc_id]['display_unit']
            food = foods_by_fdc[fdc_id]
            usdacategory_id = int(food_df['food_category_id'][row])

            # Some food.csv from usda don't have category ids.
            # Make sure you are using a csv with category ids.
            if usdacategory_id:
                usdacategory_id_count += 1

            # Skip if food exists and is up to date.
            if (
                food.exists()
                and food.name == name
                and food.usdacategory_id == usdacategory_id
                and food.upc_code == upc_code
                and food.one_serving_qty == one_serving_qty
                and food.one_serving_unit == one_serving_unit
                and food.one_serving_display_qty == one_serving_display_qty
                and food.one_serving_display_unit == one_serving_display_unit
            ):
                continue
            # Add to foods to update if exists but not up to date.
            if food.exists():
                food.name = name
                food.usdacategory_id = usdacategory_id
                food.upc_code = upc_code
                food.one_serving_qty = one_serving_display_qty
                food.one_serving_unit = one_serving_unit
                food.one_serving_display_qty = one_serving_display_qty
                food.one_serving_display_unit = one_serving_display_unit
                foods_to_update.append(food)
                continue
            # If new, add to create list.
            new_food = FoodWithFdcId()
            new_food.name = name
            new_food.usdacategory_id = usdacategory_id
            new_food.upc_code = upc_code
            new_food.one_serving_qty = one_serving_display_qty
            new_food.one_serving_unit = one_serving_unit
            new_food.one_serving_display_qty = one_serving_display_qty
            new_food.one_serving_display_unit = one_serving_display_unit
            new_food.fdc_id = fdc_id
            foods_to_create.append(new_food)

        if usdacategory_id_count == 0:
            return self.stdout.write(self.style.ERROR(
                "Failed to sync foods: Check that nutrient.csv contains \
                food_category_id records for at least one row."
            ))

        try:
            # 1. Bulk create usdafoods.
            USDAFood.objects.bulk_create(usdafoods_to_create)
            # 2. Bulk update foods
            Food.objects.bulk_update(foods_to_update)
            # 3. Bulk create foods
            updated_foods = Food.objects.bulk_create(foods_to_update)
        except NameError:
            return self.stdout.write(self.style.ERROR(
                f'Failed to bulk create/updates foods and usdafoods:\
                {NameError}'
            ))

        # Interate through updated foods to link
        # food ids to fdc_ids
        foods_usdafoods_to_create = []
        for food in updated_foods:
            for food_with_fdc_id in foods_to_update:
                # Food matches food_with_fdc_id link fdc_id
                if (
                    food.name == food_with_fdc_id.name
                    and (food.usdacategory_id ==
                         food_with_fdc_id.usdacategory_id)
                    and (food.upc_code ==
                         food_with_fdc_id.upc_code)
                    and (food.one_serving_qty ==
                         food_with_fdc_id.one_serving_qty)
                    and (food.one_serving_unit ==
                         food_with_fdc_id.one_serving_unit)
                    and (food.one_serving_display_qty ==
                         food_with_fdc_id.one_serving_display_qty)
                    and (food.one_serving_display_unit ==
                         food_with_fdc_id.one_serving_display_unit)
                ):
                    food_usdafood = FoodUSDAFood(
                        food=food, fdc_id=food_with_fdc_id.fdc_id)
                    foods_usdafoods_to_create.append(food_usdafood)
                    break
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
        food_nutrient_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com\
            /food-sync-csvs/food_nutrient.csv')

        nutrient_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/nutrient.csv')

        # Throw error if csvs are not uploaded.
        if not (
            food_nutrient_df
            and nutrient_df
        ):
            return self.stdout.write(self.style.ERROR(
                'Failed to sync nutrition facts: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food_nutrient.csv, nutrient.csv'
            ))
        all_units = Unit.objects.all()
        units_by_abbr = {}
        for unit in all_units:
            # This will collapse all IU under IU, but we'll skip those anyway.
            units_by_abbr[unit.abbr] = unit

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

        # Store foods by usdanutrient_id.
        all_foods = Food.objects.all()
        foods_by_fdc = {}
        for food in all_foods:
            foods_by_fdc[food.fdc_id] = food

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
            # amount is per 100g of food
            nutrient_qty_per_100g = int(food_nutrient_df['amount'][row])
            # Skip if nutrition fact exists
            key = f'{fdc_id} - {usdanutrient_id}'
            if nutrition_facts_by_id[key]:
                continue

            # If nutrient.unit has changed update.
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
            food = foods_by_fdc[fdc_id]
            nutrient = nutrients_by_usdanutrient_id[usdanutrient_id]
            # all usda foods will have one_serving_qty in grams
            qty = nutrient_qty_per_100g * (food.one_serving_qty/100)
            new_nutrition_fact = NutritionFact(
                qty=qty,
                food=food,
                nutrient=nutrient)
            nutrition_facts_to_create.append(new_nutrition_fact)
        try:
            Nutrition.objects.bulk_update(nutrients_to_update)
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
        self.sync_nutrition_facts()

        self.stdout.write(self.style.SUCCESS(
            'Successfully synced foods!'))
