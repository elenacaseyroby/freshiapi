import requests
from bs4 import BeautifulSoup
from django.db import transaction

from models import (
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

from django_apps.recipes.services.recipe_title_scraper import (
    scrape_recipe_title,
)

from django_apps.recipes.services.recipe_image_scraper import (
    scrape_recipe_image_url,
)

from django_apps.recipes.services.recipe_source_scraper import (
    scrape_recipe_source_url,
    scrape_recipe_source_name,
)
from django_apps.recipes.services.recipe_servings_scraper import (
    scrape_recipe_servings_count,
)
from django_apps.recipes.services.recipe_author_scraper import (
    scrape_recipe_author,
)
from django_apps.recipes.services.recipe_description_scraper import (
    scrape_recipe_description,
)

from django_apps.recipes.services.recipe_ingredient_scraper import (
    scrape_recipe_ingredients,
)

from django_apps.recipes.services.recipe_directions_scraper import (
    scrape_recipe_directions,
)

from django_apps.recipes.services.recipe_time_scraper import (
    scrape_recipe_prep_time,
    scrape_recipe_cook_time,
    scrape_recipe_total_time,
)

from django_apps.recipes.services.recipe_category_scraper import (
    scrape_recipe_categories,
)

from django_apps.recipes.services.recipe_cuisine_scraper import (
    scrape_recipe_cuisine,
)

from django_apps.recipes.services.recipe_diets_scraper import (
    scrape_recipe_diets,
)


def clean_url(url):
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
    source_url = scrape_recipe_source_url(soup_html)
    source = Source.objects.get_or_create(
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
    new_recipe = new_recipe.save()

    # Store image url
    image_url = scrape_recipe_image_url(soup_html)
    internet_image = InternetImage.objects.get_or_create(
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
    new_recipe_categories = [
        RecipeCategory(
            category=categories_by_name[category],
            recipe=new_recipe
        )
        for category in categories
    ]
    RecipeCategory.objects.bulk_update(new_recipe_categories)

    # Add cuisine
    cuisines_by_name = {
        cuisine.name: cuisine for cuisine in
        Cuisine.objects.all()
    }
    cuisine = scrape_recipe_cuisine(
        soup_html, cuisines_by_name)
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
    new_recipe_diets = [
        RecipeDiet(
            diet=diets_by_name[diet],
            recipe=new_recipe
        )
        for diet in diets
    ]
    RecipeDiet.objects.bulk_create(new_recipe_diets)

    # Add ingredients and directions.
    units_by_name = {
        unit.name: unit
        for unit in Unit.objects.all()
    }
    # get qty - tests!!
    # get unit - tests!!
    # fuzzywuzzy match food name - need tests for this!!!
    ingredients = scrape_recipe_ingredients(soup_html)
    directions = scrape_recipe_directions(soup_html)
