import requests
from bs4 import BeautifulSoup
from django.db import transaction
from datetime import timedelta

from django_apps.recipes.models import (
    Category,
    Cuisine,
    Diet,
    Ingredient,
    Recipe,
    RecipeCategory,
    RecipeCuisine,
    RecipeDiet,
    RecipeInternetImage,
    Source,
)
from django_apps.foods.models import Unit

from django_apps.recipes.scraper.recipe_title_scraper import (
    scrape_recipe_title,
)

from django_apps.recipes.scraper.recipe_image_scraper import (
    scrape_recipe_image_url,
)

from django_apps.recipes.scraper.recipe_source_scraper import (
    scrape_recipe_source_url,
    scrape_recipe_source_name,
)
from django_apps.recipes.scraper.recipe_servings_scraper import (
    scrape_recipe_servings_count,
)
from django_apps.recipes.scraper.recipe_author_scraper import (
    scrape_recipe_author,
)
from django_apps.recipes.scraper.recipe_description_scraper import (
    scrape_recipe_description,
)

from django_apps.recipes.scraper.recipe_ingredient_scraper import (
    scrape_recipe_ingredients,
)

from django_apps.recipes.scraper.recipe_time_scraper import (
    scrape_recipe_prep_time,
    scrape_recipe_cook_time,
    scrape_recipe_total_time,
)

from django_apps.recipes.scraper.recipe_category_scraper import (
    scrape_recipe_categories,
)

from django_apps.recipes.scraper.recipe_cuisine_scraper import (
    scrape_recipe_cuisine,
)

from django_apps.recipes.scraper.recipe_diets_scraper import (
    scrape_recipe_diets,
)

from django_apps.recipes.scraper.parse_ingredients import (
    parse_ingredient
)

import re


def clean_url(url):
    url = str(url)
    cleaned_url = None
    matches = re.match('^https://www.(.+)', url)
    if matches:
        cleaned_url = matches[1]
    if not cleaned_url:
        matches = re.match('^http://www.(.+)', url)
        if matches:
            cleaned_url = matches[1]
    if not cleaned_url:
        matches = re.match('^www.(.+)', url)
        if matches:
            cleaned_url = matches[1]
    if not cleaned_url:
        matches = re.match('^https://(.+)', url)
        if matches:
            cleaned_url = matches[1]
    if not cleaned_url:
        matches = re.match('^http://(.+)', url)
        if matches:
            cleaned_url = matches[1]
    matches = re.match('(.+)/$', cleaned_url)
    if matches:
        cleaned_url = matches[1]
    if cleaned_url is None:
        cleaned_url = url
    return cleaned_url


@transaction.atomic
def scrape_recipe(url, update_recipe_id=None):
    # If update_recipe_id passed, the recipe will be updated.
    # Else, it will be added for the first time.
    # We only want to update a recipe like this
    # in certain cases. If we did it everytime
    # a user went to scrape a website, we would be replacing
    # and erasing valuable edits.

    cleaned_url = clean_url(url)
    print('recipe id:' + str(update_recipe_id))
    # If meant to be first time scrape (not update) and recipe exists,
    # return existing recipe.
    if not update_recipe_id:
        recipe = Recipe.objects.filter(url=cleaned_url).first()
        if recipe:
            return recipe

    # Fake the user-agent like we're a browser so that
    # we can scrape sites that block scripts. By default
    # the user-agent will announce that we are a script
    # by being set to something like "Python-urllib/2.6".
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
    # Get html from url
    page = requests.get(url, headers=headers)
    soup_html = BeautifulSoup(page.content, 'html.parser')

    # Scrape source info.
    source_url = scrape_recipe_source_url(cleaned_url)
    source_name = scrape_recipe_source_name(soup_html)

    # Check if source exists.
    source = Source.objects.filter(
        website=source_url
    ).first()

    # If not, save new source.
    if not source:
        source = Source(
            website=source_url,
            name=source_name
        )
        source.save()

    # Create/update recipe
    recipe = Recipe()
    # If recipe_id passed, prepare to update recipe.
    if (update_recipe_id):
        # set recipe_id so updates are made to existing recipe.
        recipe.id = update_recipe_id
    recipe.url = cleaned_url
    recipe.title = scrape_recipe_title(soup_html)
    recipe.author = scrape_recipe_author(soup_html)
    recipe.description = scrape_recipe_description(soup_html)
    recipe.source = source
    recipe.prep_time = scrape_recipe_prep_time(soup_html)
    recipe.cook_time = scrape_recipe_cook_time(soup_html)
    recipe.total_time = scrape_recipe_total_time(soup_html)

    # Make sure total time makes sense.
    prep = recipe.prep_time or timedelta(minutes=float(0))
    cook = recipe.cook_time or timedelta(minutes=float(0))
    total = recipe.total_time or timedelta(minutes=float(0))
    # If total is none or smaller than prep and cook combine,
    # then set total to the sum of prep and cook.
    if (prep + cook) > total:
        recipe.total_time = prep + cook

    recipe.servings_count = scrape_recipe_servings_count(soup_html)
    recipe.save()
    recipe = Recipe.objects.get(url=cleaned_url)

    # Only add tags if recipe is new.
    # Might want to change this later, but fine for a first run.
    if not update_recipe_id:
        # Store image url
        image_url = scrape_recipe_image_url(soup_html)
        if image_url:
            # Create internet image record to store url
            RecipeInternetImage.objects.get_or_create(
                url=image_url,
                recipe_id=recipe.id
            )

        # Add categories
        categories_by_name = {
            category.name: category for category in
            Category.objects.all()
        }
        categories = scrape_recipe_categories(
            soup_html, categories_by_name)
        if len(categories) > 0:
            recipe_categories = [
                RecipeCategory(
                    category=categories_by_name[category],
                    recipe=recipe
                )
                for category in categories
            ]
            RecipeCategory.objects.bulk_create(recipe_categories)

        # Add cuisine
        cuisines_by_name = {
            cuisine.name: cuisine for cuisine in
            Cuisine.objects.all()
        }
        cuisine = scrape_recipe_cuisine(
            soup_html, cuisines_by_name)
        if cuisine:
            recipe_cuisine = RecipeCuisine(
                cuisine=cuisines_by_name[cuisine],
                recipe=recipe
            )
            recipe_cuisine.save()

        # Add diets.
        diets_by_name = {
            diet.name: diet for diet in Diet.objects.all()
        }
        diets = scrape_recipe_diets(soup_html, diets_by_name)
        if len(diets) > 0:
            recipe_diets = [
                RecipeDiet(
                    diet=diets_by_name[diet],
                    recipe=recipe
                )
                for diet in diets
            ]
            RecipeDiet.objects.bulk_create(recipe_diets)
    # Get ingredients. 
    ingredient_strings = scrape_recipe_ingredients(soup_html)
    # If not ingredients, do nothing.
    if not ingredient_strings:
        recipe.ingredients_in_nutrition_facts = float(0)
        return
    elif update_recipe_id:
        # If updating recipe, prepare by
        # deleting recipe ingredients, so updated ingredients can be saved.
        # Lazy: fix & use diff later.
        ingredients = Ingredient.objects.filter(recipe_id=update_recipe_id).all()
        ingredients.delete()
    # Else, get nutrition breakdown
    units_by_name = {
        unit.name: unit for unit in Unit.objects.all()}
    units_by_abbr = {
        unit.abbr: unit for unit in Unit.objects.all()}

    ingredients = []
    # Parse ingredient from scraped ingredient string.
    for ingredient_str in ingredient_strings:
        ingredient = parse_ingredient(ingredient_str, units_by_name, units_by_abbr)
        if ingredient:
            ingredient.recipe_id = recipe.id
            ingredients.append(ingredient)
    # Save ingredients.
    Ingredient.objects.bulk_create(ingredients)

    # Save nutrition facts & allergens
    recipe_ingredient_count = len(ingredient_strings)
    recipe.save_nutrition_facts(ingredients, recipe_ingredient_count)
    recipe.save_allergens(ingredients)

# TODO:
# def add_ingredients_and_directions_to_recipe(recipe):
#     # Get html from url
#     page = requests.get(recipe.url)
#     soup_html = BeautifulSoup(page.content, 'html.parser')
#     # Add ingredients.
#     ingredients = scrape_recipe_ingredients(soup_html)
#     if len(ingredients) > 0:
#         units_by_name = {
#             unit.name: unit
#             for unit in Unit.objects.all()
#         }
#         for ingredient in ingredients:
#             ingredient = create_ingredient(
#                 ingredient, recipe, units_by_name)

#     # Add directions.
#     directions = scrape_recipe_directions(soup_html)
#     if len(directions) > 0:
#         Direction.objects.bulk_create([
#             Direction(
#                 step=count+1,
#                 text=direction,
#                 recipe=recipe
#             )
#             for count, direction in enumerate(directions)
#         ])
