from django.contrib import admin
# from django import forms

from .models import Recipe, Direction
from .scraper.recipe_scraper import scrape_recipe


class DirectionInline(admin.TabularInline):
    model = Direction
    fields = (
        'step',
        'text'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    inlines = [DirectionInline, ]

    fields = (
        'url',
        'title',
        'author',
        'description',
        'prep_time',
        'cook_time',
        'total_time',
        'source',
        'nutrition_facts_complete',
    )
    readonly_fields = (
        'nutrition_facts_complete',
    )
    # ingredients
    # directions
    # allergens
    # categories
    # diets

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        scrape_recipe(obj.url)


# show recipes and allow edits
# add custom recipe - don't show url
# scrape recipe - only show url
