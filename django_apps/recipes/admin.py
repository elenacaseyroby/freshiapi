from django.contrib import admin
from django import forms
# from django import forms

from .models import (
    Direction,
    Ingredient,
    NutritionFact,
    Recipe,
    RecipeAllergen,
    RecipeCategory,
    RecipeCuisine,
    RecipeDiet,
    RecipeInternetImage,
)
from .scraper.recipe_scraper import scrape_recipe


class RecipeAllergenInline(admin.TabularInline):
    model = RecipeAllergen
    extra = 0

    def allergen_name(self, obj):
        return obj.contains_allergen.name or '--'

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
    extra = 0
    fields = (
        'step',
        'text'
    )


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0

    fields = (
        'food',
        'notes',
        'qty_numerator',
        'qty_denominator',
        'qty_unit',
    )
    readonly_fields = (
        'food',
        'notes',
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


class RecipeForm(forms.ModelForm):
    scrape_recipe_from_url = forms.BooleanField()
    help_texts = {
        'scrape_recipe_from_url':
        'Check this box to regenerate recipe from URL. \
            Be careful, this will reset all existing information.''',
    }
    fields = ('scrape_recipe_from_url', )

    def save(self, commit=True):
        return super(RecipeForm, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = Recipe


# class ScrapeRecipeForm(forms.BaseModelForm):
#     scrape_recipe_from_url = forms.BooleanField()
#     declared_fields = ('scrape_recipe_from_url', )

#     class Meta:
#         model = Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInline,
        DirectionInline,
        RecipeInternetImageInline,
        NutritionFactInline,
        RecipeAllergenInline,
        RecipeCategoryInline,
        RecipeDietInline,
        RecipeCuisineInline,
    ]
    form = RecipeForm

    def percent_ingredients_in_nutrition_facts(self, obj):
        if not obj.ingredients_in_nutrition_facts:
            return '--'
        else:
            return f'''{
                round(float(obj.ingredients_in_nutrition_facts) *
                      float(100))
            }%'''

    fields = (
        'url',
        'scrape_recipe_from_url',
        'title',
        'servings_count',
        'author',
        'description',
        'prep_time',
        'cook_time',
        'total_time',
        'source',
        'percent_ingredients_in_nutrition_facts',
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
        'percent_ingredients_in_nutrition_facts',
    )

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            url = form.cleaned_data['url']
            scrape_recipe_from_url = form.cleaned_data[
                'scrape_recipe_from_url']
            # If recipe doesn't exist, scrape info from url
            # and save new instance.
            if not obj.id and url:
                scrape_recipe(obj.url)
            # If recipe exists and box is checked to scrape url, scrape
            # info and store to existing recipe instance.
            elif url and scrape_recipe_from_url:
                scrape_recipe(obj.url, obj.id)
                # and box is not checked to scrape url, save all other info.
            # Else save recipe info.
            else:
                super().save_model(request, obj, form, change)
