from django.db import models
from django.utils.functional import cached_property

from django_apps.users.models import User

# Note: in postgress unique_together is functionally the same
# as index_togeter

# Django standard practice is to use "blank=True"
# but for this app we are using "null=True"
# to easier input data without weird errors.
# Exception: many to many tables.


class Unit(models.Model):
    name = models.CharField(unique=True, max_length=50)
    abbr = models.CharField(max_length=10)

    # object label in admin
    def __str__(self):
        return self.name


class USDANutrient(models.Model):
    # usda_nutrient_id stores the nutrient ids from the USDA FoodData Central
    # Database.  Each usda_nutrient_id is tied to one or more nutrient
    # in the foods_nutrient table.
    usda_nutrient_id = models.IntegerField()


class Nutrient(models.Model):
    name = models.CharField(unique=True, max_length=40)
    dv_qty = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)
    dv_unit = models.ForeignKey(
        Unit, on_delete=models.RESTRICT, null=True)
    usda_nutrient_ids = models.ManyToManyField(USDANutrient, blank=True)
    article_url = models.URLField(null=True)
    description = models.TextField(null=True)
    description_citations = models.TextField(null=True)
    description_src_note = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @cached_property
    def is_spotlight_nutrient(self):
        if self.description:
            return True
        return False

    @cached_property
    def is_trackable_nutrient(self):
        trackable_nutrients_without_dv = [
            'calories',
            'carbohydrates',
            'protein',
            'fat'
            'sugars',
            'sodium',
            'trans fat',
            'fiber',
        ]
        if (
            (self.dv_qty and self.dv_unit)
            or self.name in trackable_nutrients_without_dv
        ):
            return True
        return False

    # object label in admin
    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            models.F('dv_qty').asc(nulls_last=True),
            models.F('dv_unit').asc(nulls_last=True)
        ]


class USDACategory(models.Model):
    name = models.CharField(unique=True, max_length=40)
    # usda_category_id stores the category id from the USDA FoodData Central
    # Database.
    usda_category_id = models.PositiveSmallIntegerField()


class Food(models.Model):
    name = models.CharField(unique=True, max_length=100)
    # Defines a single serving of the food
    # Example: 1 cup
    # Use these for conversions & writing recipes
    one_serving_qty = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # If unit is deleted we do not want food record to be deleted.
    one_serving_unit = models.ForeignKey(
        Unit, on_delete=models.RESTRICT, null=True)
    # If one serving is 100 grams.
    # We might want one serving to be displayed as 1 slice or 5 crackers.
    # Use these for tracking foods.
    # Ex. I ate 2 cups of banana is not appropriate for food tracker,
    # but 1 banana is.
    one_serving_display_qty = models.DecimalField(
        max_digits=7, decimal_places=2, null=True)
    one_serving_display_unit = models.CharField(max_length=30, null=True)
    nutrients = models.ManyToManyField(
        Nutrient, through='NutritionFact', blank=True)
    # If usda category is deleted, we do not want food to be deleted.
    usda_category = models.ForeignKey(
        USDACategory, on_delete=models.RESTRICT, null=True)
    # usda_fdc_id will only exist for foods added from the USDA FoodData
    # Central Database.
    usda_fdc_id = models.IntegerField(null=True)
    # upc_code is bar code.
    upc_code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @cached_property
    def citation(self):
        if self.usda_fdc_id:
            return 'U.S. Department of Agriculture, Agricultural Research \
                Service. 2018. USDA Food and Nutrient Database for Dietary \
                Studies 2017-2018. Food Surveys Research Group Home \
                Page, www.ars.usda.gov/nea/bhnrc/fsrg '
        return ''

    @cached_property
    def source_note(self):
        if self.usda_fdc_id:
            return 'USDA’s Food and Nutrient Database for Dietary Studies \
                2017-2018 was used to code dietary intake data and calculate \
                nutrient intakes.'
        return ''


class NutritionFact(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    unique_together = [['food', 'nutrient']]
    # nutrient qty in one serving of food. unit is defined in nutrient table):
    nutrient_qty = models.DecimalField(
        max_digits=7, decimal_places=2)


class UnitConversion(models.Model):
    from_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='from_unit')
    to_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='to_unit')
    unique_together = [['from_unit', 'to_unit']]
    qty_conversion_coefficient = models.DecimalField(
        max_digits=45, decimal_places=15)


# Mostly for internal record.
class FoodAddedByUser(models.Model):
    # Record will not be deleted if user is deleted, but it will be deleted if
    # food is deleted.
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
