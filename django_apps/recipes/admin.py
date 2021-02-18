from django.contrib import admin
# from django import forms

from .models import Recipe
from .scraper.recipe_scraper import scrape_recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('url',)
    readonly_fields = (
        'title',
        'author',
        'description',
        'prep_time',
        'cook_time',
        'total_time',
    )
    exclude = ['nutrition_facts_complete', ]

    # generate_nutrition_facts = forms.Boolean(widget=forms.CheckboxInput())

    def save_model(self, request, obj, form, change):
        # obj.user = request.user
        scrape_recipe(obj.url)
        # super().save_model(request, obj, form, change)
