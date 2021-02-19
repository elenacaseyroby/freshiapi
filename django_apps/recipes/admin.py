from django.contrib import admin
# from django import forms

from .models import (
    Recipe, Direction, Ingredient, NutritionFact, RecipeInternetImage,
    RecipeAllergen, RecipeCategory, RecipeCuisine, RecipeDiet)
from .scraper.recipe_scraper import scrape_recipe


class RecipeAllergenInline(admin.TabularInline):
    model = RecipeAllergen
    extra = 0

    def allergen_name(self, obj):
        return obj.allergen.name or '--'

    fields = (
        'allergen_name',
    )
    readonly_fields = (
        'allergen_name',
    )


class RecipeCategoryInline(admin.TabularInline):
    model = RecipeCategory
    extra = 0

    def category_name(self, obj):
        return obj.category.name or '--'

    fields = (
        'category_name',
    )
    readonly_fields = (
        'category_name',
    )


class RecipeCuisineInline(admin.TabularInline):
    model = RecipeCuisine
    extra = 0

    def cuisine_name(self, obj):
        return obj.cuisine.name or '--'

    fields = (
        'cuisine_name',
    )
    readonly_fields = (
        'cuisine_name',
    )


class RecipeDietInline(admin.TabularInline):
    model = RecipeDiet
    extra = 0

    def diet_name(self, obj):
        return obj.diet.name or '--'

    fields = (
        'diet_name',
    )
    readonly_fields = (
        'diet_name',
    )


class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 1
    fields = (
        'step',
        'text'
    )


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    fields = (
        'food',
        'qty_numerator',
        'qty_denominator',
        'qty_unit',
    )


class RecipeInternetImageInline(admin.TabularInline):
    model = RecipeInternetImage
    extra = 0

    def url(self, obj):
        return obj.internet_image.url or '--'

    fields = (
        'url',
    )
    readonly_fields = (
        'url',
    )


class NutritionFactInline(admin.TabularInline):
    model = NutritionFact
    extra = 0

    # custom fields must be in readonly_fields
    def dv_percent(self, obj):
        if not obj.nutrient.dv_qty:
            return '--'
        recipe_nutrient_qty = float(obj.nutrient_qty)
        nutrient_dv_qty = float(obj.nutrient.dv_qty)
        percent = str(round(recipe_nutrient_qty / nutrient_dv_qty) * 100)
        return f'{percent}%'

    # custom fields must be in readonly_fields
    def nutrient_unit(self, obj):
        if not obj.nutrient.dv_unit:
            return '--'
        return obj.nutrient.dv_unit.abbr

    fields = (
        'nutrient',
        'nutrient_qty',
        'nutrient_unit',
        'dv_percent'
    )
    readonly_fields = (
        'nutrient',
        'nutrient_qty',
        'nutrient_unit',
        'dv_percent'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    inlines = [
        DirectionInline,
        RecipeInternetImageInline,
        NutritionFactInline,
        RecipeAllergenInline,
        RecipeCategoryInline,
        RecipeDietInline,
        RecipeCuisineInline,
    ]

    fields = (
        'url',
        'title',
        'servings_count',
        'author',
        'description',
        'prep_time',
        'cook_time',
        'total_time',
        'source',
        'nutrition_facts_complete',
    )
    readonly_fields = (
        'title',
        'servings_count',
        'author',
        'description',
        'prep_time',
        'cook_time',
        'total_time',
        'source',
        'nutrition_facts_complete',
        'nutrition_facts_complete',
    )
    # ingredients
    # directions
    # allergens
    # categories
    # diets

    def save_model(self, request, obj, form, change):
        # this will double save so must be commented:
        # super().save_model(request, obj, form, change)
        scrape_recipe(obj.url)


# show recipes and allow edits
# add custom recipe - don't show url
# scrape recipe - only show url
