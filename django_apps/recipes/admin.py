from django.contrib import admin
from django import forms
# from django.forms.models import BaseInlineFormSet

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
# from .scraper.parse_ingredients import get_closest_matching_food


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


# class IngredientForm(forms.ModelForm):
#     update_food = forms.CharField(required=False)
#     fields = ('update_food', )

#     def save(self, obj, commit=True):
#         return super(IngredientForm, self).save(commit=commit)

#     class Meta:
#         fields = '__all__'
#         model = Ingredient


class IngredientInline(admin.TabularInline):
    model = Ingredient
    # form = IngredientForm
    extra = 0

    fields = (
        'food',
        'notes',
        # 'update_food',
        'qty_numerator',
        'qty_denominator',
        'qty_unit',
    )
    readonly_fields = (
        'food',
        'notes',
    )


# class IngredientInlineFormSet(BaseInlineFormSet):
#     # def save_new_objects(self, commit=True):
#     #     saved_instances = super(BookInlineFormSet, self).save_new_objects(commit)
#     #     if commit:
#     #         # create book for press
#     #     return saved_instances

#     def save_existing_objects(self, commit=True):
#         saved_instances = super(
#             IngredientInlineFormSet,
#             self
#         ).save_existing_objects(commit)
#         if commit:
#             for form in self.initial_forms:
#             pk_name = self._pk_field.name
#             raw_pk_value = form._raw_value(pk_name)

#             # clean() for different types of PK fields can sometimes return
#             # the model instance, and sometimes the PK. Handle either.
#             pk_value = form.fields[pk_name].clean(raw_pk_value)
#             pk_value = getattr(pk_value, 'pk', pk_value)

#             obj = self._existing_object(pk_value)
#             if self.can_delete and self._should_delete_form(form):
#                 self.deleted_objects.append(obj)
#                 obj.delete()
#                 # problem here causes `clean` 6 lines up to fail next round

#                 # patched line here for future save()
#                 # to not attempt a second delete
#                 self.forms.remove(form)

#       return saved_instances


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
    scrape_recipe_from_url = forms.BooleanField(required=False)
    fields = ('scrape_recipe_from_url', )

    def save(self, commit=True):
        return super(RecipeForm, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = Recipe


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
