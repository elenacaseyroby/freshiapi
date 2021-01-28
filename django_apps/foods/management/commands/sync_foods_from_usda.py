from django.core.management.base import BaseCommand
from django_apps.foods.models import USDACategory

import pandas as pd


class Command(BaseCommand):
    help = 'Sync foods from USDA food and nutrient data sets.'

    def sync_categories(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.
        category_df = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_category.csv')

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
        cats_to_create = []
        cats_to_update = []
        for row in category_df.index:
            cat_id = category_df['id'][row]
            cat_name = category_df['description'][row]
            # Skip if category exists and is up to date.
            if cats.filter(usdacategory_id=cat_id, name=cat_name).exists():
                continue
            # If updated add to update list.
            cat_to_update = cats.filter(usdacategory_id=cat_id)
            if cat_to_update.exists():
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

    def handle(self, *args, **options):
        # Prereqs: must upload csvs to /freshi-app/food-sync-csvs
        # s3 bucket.

        food_csv = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food.csv')
        food_category_csv = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_category.csv')
        food_nutrient_csv = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_nutrient.csv')
        food_portion_csv = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/food_portion.csv')
        market_acquisition_csv = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/market_acquisition.csv')
        nutrient_csv = pd.read_csv(
            'https://freshi-app.s3.amazonaws.com/food-sync-csvs/nutrient.csv')

        # Throw error if csvs are not uploaded.
        if not (
            food_csv
            and food_category_csv
            and food_nutrient_csv
            and food_portion_csv
            and market_acquisition_csv
            and nutrient_csv
        ):
            return self.stdout.write(self.style.ERROR(
                'Failed to sync food: Please make \
                sure the following USDA FoodData Central csvs \
                are uploaded to the freshi-app/food-sync-csvs \
                bucket in AWS S3:\
                food.csv, food_category.csv, food_nutrient.csv,\
                food_portion.csv, market_acquisition.csv, nutrient.csv'
            ))

        # Throw error if food.food_category_id doesn't exist for any foods, ask for
        # different version of db with that field filled out.
        # 1. Sync categories

        # find diffs
        # update
        # 2. Sync foods with barcodes and serving size
        # find diffs
        # update
        # 3. Sync nutrition facts
        # find diffs
        # update

        self.stdout.write(self.style.SUCCESS(
            'Successfully synced foods!'))
