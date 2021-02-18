import requests
from bs4 import BeautifulSoup
from django.db import transaction

from django_apps.recipes.models import (
    Category,
    Cuisine,
    Diet,
    Recipe,
    Source,
    RecipeCategory,
    RecipeCuisine,
    RecipeDiet
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


def clean_url(url):
    url = str(url)
    end_of_string = len(url) - 1
    if url[end_of_string] == '/':
        url = url[:end_of_string]
    if url[:8] == 'https://':
        url = url[5:]
    if url[:7] == 'http://':
        url = url[4:]
    if url[:4] == 'www.':
        url = url[4:]
    return url


@transaction.atomic
def scrape_recipe(url):
    # If recipe already scraped, return.
    cleaned_url = clean_url(url)
    recipe = Recipe.objects.filter(url=cleaned_url).first()
    if recipe:
        return recipe

    # Get html from url
    page = requests.get(url)
    soup_html = BeautifulSoup(page.content, 'html.parser')

    # Scrape source info.
    source_name = scrape_recipe_source_name(soup_html)
    source_url = scrape_recipe_source_url(cleaned_url)
    print("~~~~~~~~~")
    print(source_name)
    print(source_url)

    Source.objects.get_or_create(
        website=source_url,
        name=source_name
    )

    source = Source.objects.get(
        website=source_url,
        name=source_name
    )

    # Create recipe instance.
    new_recipe = Recipe()
    new_recipe.title = scrape_recipe_title(soup_html)
    new_recipe.url = cleaned_url
    new_recipe.prep_time = scrape_recipe_prep_time(soup_html)
    new_recipe.cook_time = scrape_recipe_cook_time(soup_html)
    new_recipe.total_time = scrape_recipe_total_time(soup_html)
    new_recipe.servings_count = scrape_recipe_servings_count(soup_html)
    new_recipe.author = scrape_recipe_author(soup_html)
    new_recipe.description = scrape_recipe_description(soup_html)
    new_recipe.source = source
    new_recipe.save()
    new_recipe = Recipe.objects.get(url=cleaned_url)

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
        new_recipe.internet_images.add(internet_image)

    # Add categories
    categories_by_name = {
        category.name: category for category in
        Category.objects.all()
    }
    categories = scrape_recipe_categories(
        soup_html, categories_by_name)
    if len(categories) > 0:
        new_recipe_categories = [
            RecipeCategory(
                category=categories_by_name[category],
                recipe=new_recipe
            )
            for category in categories
        ]
        RecipeCategory.objects.bulk_create(new_recipe_categories)

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
            recipe=new_recipe
        )
        recipe_cuisine.save()

    # Add diets.
    diets_by_name = {
        diet.name: diet for diet in Diet.objects.all()
    }
    diets = scrape_recipe_diets(soup_html, diets_by_name)
    if len(diets) > 0:
        new_recipe_diets = [
            RecipeDiet(
                diet=diets_by_name[diet],
                recipe=new_recipe
            )
            for diet in diets
        ]
        RecipeDiet.objects.bulk_create(new_recipe_diets)
        ingredients = scrape_recipe_ingredients(soup_html)
        # If not ingredients, do nothing.
        if not ingredients:
            return
        # Else, get nutrition breakdown
        units_by_name_and_abbr = {
            unit.name: unit for unit in Unit.objects.all()}
        units_by_name_and_abbr.update(
            {unit.abbr: unit for unit in Unit.objects.all()})
        unsaved_ingredients = [
            parse_ingredient(ingredient, units_by_name_and_abbr)
            for ingredient in ingredients
        ]
        recipe.save_nutrition_facts(unsaved_ingredients)
        recipe.save_allergens(unsaved_ingredients)

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
