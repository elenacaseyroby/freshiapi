# freshi

## Syncing foods and nutrition facts from USDA FoodData Central
1. Make sure nutrients, nutrients_usdanutrients, units, unit_conversions are all filled in the db already.
2. Add the following FoodData Central csvs to our Amazon S3 bucket freshi-app/food-sync-csvs: food.csv, nutrient.csv, food_nutrient.csv, food_portion.csv, market_acquisition.csv, food_category.csv 
3. Run this management command in your virtual env: `python manage.py sync_foods_from_usda`
