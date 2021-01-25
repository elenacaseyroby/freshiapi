from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=100)


class Nutrient(models.Model):
    name = models.CharField(max_length=40)
    # Defines a single serving of the food
    # Example: 1 cup
    dv_qty = models.DecimalField(max_digits=5, decimal_places=2)
    dv_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=40)


class Food(models.Model):
    name = models.CharField(max_length=100)
    # Defines a single serving of the food
    # Example: 1 cup
    # Use these for conversions & writing recipes
    one_serving_qty = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    one_serving_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, blank=True)
    # If one serving is 100 grams.
    # We might want one serving to be displayed as 1 slice or 5 crackers.
    # Use these for tracking foods.
    # Ex. I ate 2 cups of banana is not appropriate for food tracker,
    # but 1 banana is.
    one_serving_display_qty = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    one_serving_display_unit = models.CharField(max_length=30)
    nutrients = models.ManyToManyField(Nutrient, through='Nutrition')
    categories = models.ManyToManyField(Category)


class NutritionFact(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    # nutrient qty in one serving of food. unit is defined in nutrient table):
    nutrient_qty = models.DecimalField(
        max_digits=5, decimal_places=2)


class UnitConversion(models.Model):
    from_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    to_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    qty_conversion_coefficient = models.DecimalField(
        max_digits=5, decimal_places=5)
