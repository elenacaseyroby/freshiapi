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
    Source,
)

from django_apps.media.models import InternetImage
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
def scrape_recipe(url, recipe_id=None):
    # If recipe_id passed, the recipe will be updated.
    # Else, it will be added for the first time.
    # We only want to update a recipe like this
    # in certain cases. If we did it everytime
    # a user went to scrape a website, we would be replacing
    # and erasing valuable edits.

    cleaned_url = clean_url(url)
    # If meant to be a first time scrape
    # and recipe exists, do nothing.
    if not recipe_id:
        recipe = Recipe.objects.filter(url=cleaned_url).first()
        if recipe:
            return recipe

    # Get html from url
    page = requests.get(url)
    soup_html = BeautifulSoup(page.content, 'html.parser')

    # Scrape source info.
    source_url = scrape_recipe_source_url(cleaned_url)
    source_name = scrape_recipe_source_name(soup_html)
    if not source_name:
        source_name = source_url[:99]

    Source.objects.get_or_create(
        website=source_url,
        name=source_name
    )

    source = Source.objects.get(
        website=source_url,
        name=source_name
    )

    # Create or update recipe instance.
    recipe = Recipe()
    # If recipe_id passed, update recipe.
    if (recipe_id):
        recipe.id = recipe_id
    recipe.url = cleaned_url
    recipe.title = scrape_recipe_title(soup_html)
    if recipe.title is None:
        recipe.title = cleaned_url[:99]
    recipe.prep_time = scrape_recipe_prep_time(soup_html)
    recipe.cook_time = scrape_recipe_cook_time(soup_html)
    recipe.total_time = scrape_recipe_total_time(soup_html)
    # Make sure total time makes sense.
    # We only need to check if prep or cook time is set.
    if (recipe.prep_time is not None or recipe.cook_time is not None):
        prep = recipe.prep_time or timedelta(minutes=float(0))
        cook = recipe.cook_time or timedelta(minutes=float(0))
        # If total is none or smaller than prep and cook combine,
        # then set total to the sum of prep and cook.
        if (
            recipe.total_time is None or
            recipe.total_time < (prep + cook)
        ):
            recipe.total_time = prep + cook
    recipe.servings_count = scrape_recipe_servings_count(soup_html)
    recipe.author = scrape_recipe_author(soup_html)
    if recipe.author is None:
        recipe.author = source_name
    recipe.description = scrape_recipe_description(soup_html)
    recipe.source = source
    recipe.save()
    recipe = Recipe.objects.get(url=cleaned_url)

    # Store image url
    image_url = scrape_recipe_image_url(soup_html)
    if image_url:
        # Create internet image record to store url
        InternetImage.objects.get_or_create(
            url=image_url
        )
        internet_image = InternetImage.objects.get(
            url=image_url
        )
        # Add image to recipe
        recipe.internet_images.add(internet_image)

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
    # Get ingredients. DON'T SAVE.
    ingredient_strings = scrape_recipe_ingredients(soup_html)
    # If not ingredients, do nothing.
    if not ingredient_strings:
        recipe.nutrition_facts_completed = float(0)
        return
    # Else, get nutrition breakdown
    units_by_name = {
        unit.name: unit for unit in Unit.objects.all()}
    units_by_abbr = {
        unit.abbr: unit for unit in Unit.objects.all()}

    ingredients = []
    # Parse ingredient from scraped ingredient string.
    for ingredient in ingredient_strings:
        ingredient = parse_ingredient(ingredient, units_by_name, units_by_abbr)
        ingredients.append(ingredient)

    # Save ingredients.
    ingredients_to_create = []
    for ingredient in ingredients:
        # # Skip ingredients without matched food, since we aren't
        # # publishing anyway.
        # if ingredient.food_id is None:
        #     continue
        # Set recipe_id
        ingredient.recipe_id = recipe.id
        ingredients_to_create.append(ingredient)
    Ingredient.objects.bulk_create(ingredients_to_create)

    # Save nutrition facts & allergens
    recipe.save_nutrition_facts(ingredients)
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
