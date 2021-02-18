from django.db import models
from django.utils.functional import cached_property

from django_apps.foods.models import (
    get_unit_conversions_dict,
    USDACategory,
    NutritionFact as FoodNutritionFact
)


class Source(models.Model):
    # Many Recipes to one Source
    name = models.CharField(max_length=100, null=False, blank=False)
    website = models.URLField(null=False, blank=False)

    class Meta:
        db_table = 'recipes_recipe_sources'


class Allergen(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'recipes_allergens'


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'recipes_categories'


class Cuisine(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'recipes_cuisines'


class Diet(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'recipes_diets'


class Recipe(models.Model):
    # If on scrape it finds no info, email the url and recipe id to casey
    title = models.CharField(max_length=75, null=False, blank=False)
    author = models.CharField(max_length=50, null=True)
    servings_count = models.PositiveSmallIntegerField(null=True)
    prep_time = models.DurationField(null=True)
    cook_time = models.DurationField(null=True)
    total_time = models.DurationField(null=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True)
    owner = models.ForeignKey(
        'users.User', on_delete=models.RESTRICT, null=True)
    source = models.ForeignKey(
        Source, on_delete=models.RESTRICT, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    ingredients = models.ManyToManyField(
        'foods.Food', through='Ingredient', blank=True)
    nutrition_facts_complete = models.BooleanField(default=False)

    # Uploaded by users to Freshi.
    user_photos = models.ManyToManyField(
        'media.Photo', through='RecipePhoto', blank=True)
    # Urls of images for scraped recipes.
    internet_images = models.ManyToManyField(
        'media.InternetImage', through='RecipeInternetImage', blank=True)

    contains_allergens = models.ManyToManyField(
        Allergen,
        through='RecipeAllergen',
        blank=True
    )

    cuisines = models.ManyToManyField(
        Cuisine,
        through='RecipeCuisine',
        blank=True
    )

    diets = models.ManyToManyField(
        Diet,
        through='RecipeDiet',
        blank=True
    )

    categories = models.ManyToManyField(
        Category,
        through='RecipeCategory',
        blank=True
    )

    def save_allergens(self, ingredients=None):
        if not ingredients:
            ingredients = Ingredient.objects.filter(recipe_id=self.id).all()
        allergens_by_name = {
            allergen.name: allergen for allergen in Allergen.objects.all()}
        recipe_allergens = {
            'gluten': False,
            'dairy': False,
            'peanut': False,
            'egg': False,
            'soy': False,
            'fish': False,
            'shellfish': False,
            'tree nuts': False,
        }
        for ingredient in ingredients:
            if not ingredient:
                continue
            food = ingredient.food
            # skip if no food
            if not food:
                continue
            if (
                food.usdacategory_id == 18 or (
                    ' pasta ' in food.name and
                    ' gluten-free ' not in food.name
                )
            ):
                recipe_allergens['gluten'] = True
            # 1: Dairy and Egg Products
            if (
                food.usdacategory_id == 1 and
                ' egg ' not in food.name
            ):
                recipe_allergens['dairy'] = True
            if (
                ' peanut ' in food.name
            ):
                recipe_allergens['peanut'] = True
            # 1: Dairy and Egg Products
            if (
                food.usdacategory_id == 1 and
                ' egg ' in food.name
            ):
                recipe_allergens['egg'] = True
            if (
                ' soy ' in food.name or
                ' tofu ' in food.name
            ):
                recipe_allergens['soy'] = True
            # 15: Finfish and Shellfish Products
            if (
                food.usdacategory_id == 15 and
                ' fish ' in food.name
            ):
                recipe_allergens['fish'] = True
            if(
                ' shrimp ' in food.name or
                ' crab ' in food.name or
                ' lobster ' in food.name or
                ' clams ' in food.name or
                ' mussels ' in food.name or
                ' oysters ' in food.name or
                ' scallops ' in food.name or
                ' octopus ' in food.name
            ):
                recipe_allergens['shellfish'] = True
            # 12: Nut and Seed Products
            if food.usdacategory_id == 12:
                recipe_allergens['tree nuts'] = True
        # Delete all allergens
        allergens = RecipeAllergen.objects.filter(recipe_id=self.id).all()
        allergens.delete()
        # Create new allergens
        RecipeAllergen.objects.bulk_create(
            [
                RecipeAllergen(
                    contains_allergen=allergens_by_name[allergen],
                    recipe_id=self.id
                ) for allergen in recipe_allergens
                if recipe_allergens[allergen] is True
            ]
        )

    def save_nutrition_facts(self, ingredients=None):
        if not ingredients:
            ingredients = Ingredient.objects.filter(recipe_id=self.id).all()
        nutrition_facts_complete = True
        nutrition_facts = {}
        conversions = get_unit_conversions_dict()
        for ingredient in ingredients:
            # Skip and mark nutrition facts incomplete
            # if food dne.
            if not ingredient:
                continue
            food_nutrition_facts = FoodNutritionFact.objects.filter(
                food_id=ingredient.food_id).all()
            for fact in food_nutrition_facts:
                if fact.nutrient_id not in nutrition_facts:
                    nutrition_facts[fact.nutrient_id] = 0
                # If unit is None, add nutrient_qty for one serving of food.
                if ingredient.unit is None:
                    ingredient_nutrient_qty = fact.nutrient_qty
                # Else nutrient qty per one serving food to
                # nutrient qty per qty of food in ingredient.
                else:
                    numerator = float(ingredient.numerator or 1)
                    denominator = float(ingredient.denominator or 1)
                    ingredient_qty = round(float(numerator/denominator), 3)
                    food = ingredient.food
                    # Get food qty in food serving units.
                    ingredient_qty_in_food_unit = (
                        ingredient_qty * conversions[
                            ingredient.unit.id
                        ][
                            food.one_serving_display_unit_id
                        ]
                    )
                    # Find food servings for ingredient.
                    ingredient_food_servings = round(
                        float(
                            ingredient_qty_in_food_unit/food.one_serving_qty
                        ),
                        2
                    )
                    # Find nutrient qty for ingredient.
                    ingredient_nutrient_qty = (
                        fact.nutrient_qty * ingredient_food_servings
                    )
                # Store ingredient nutrient qty in nutrition facts dict.
                nutrition_facts[
                    fact.nutrient_id
                ] += ingredient_nutrient_qty
        # Delete all nutrition facts for recipe
        recipe_nutrition_facts = NutritionFact.objects.filter(
            recipe_id=self.id
        ).all()
        recipe_nutrition_facts.delete()
        # Create new nutrition facts for recipe
        NutritionFact.objects.bulk_create([
            NutritionFact(
                recipe_id=self.id,
                nutrient_id=nutrient_id,
                nutrient_qty=nutrition_facts[nutrient_id],
            ) for nutrient_id in nutrition_facts
        ])
        # Save note about nutrition facts
        self.nutrition_facts_complete = nutrition_facts_complete
        self.save()

    @cached_property
    def is_original(self):
        return self.owner is not None

    def update_nutrition_facts(self):
        return 'placeholder'

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'recipes_recipes'


class RecipePhoto(models.Model):
    # Many Recipes to Many Photos
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    photo = models.ForeignKey('media.Photo', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipes_recipes_photos'


class RecipeInternetImage(models.Model):
    # Many Recipes to Many Images
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    internet_image = models.ForeignKey(
        'media.InternetImage', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipes_recipes_internet_images'


class Direction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.PositiveSmallIntegerField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'recipes_directions'


class Ingredient(models.Model):
    food = models.ForeignKey('foods.Food', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # qty_numerator / qty_denominator in qty_unit
    qty_numerator = models.PositiveSmallIntegerField(null=False, blank=False)
    qty_denominator = models.PositiveSmallIntegerField(default=1)
    # Leave blank for something like 1 banana
    qty_unit = models.ForeignKey(
        'foods.Unit', on_delete=models.CASCADE, null=True, blank=True)

    # ON SAVE REGENERATE RECIPE NUTRITION FACTS

    class Meta:
        db_table = 'recipes_ingredients'


class NutritionFact(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(
        'foods.Nutrient',
        on_delete=models.CASCADE,
        related_name='recipe_nutrition_facts')
    unique_together = [['recipe', 'nutrient']]
    # nutrient qty in one serving of recipe. unit is defined in nutrient table:
    nutrient_qty = models.DecimalField(
        max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'recipes_nutrition_facts'


class RecipeAllergen(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    contains_allergen = models.ForeignKey(Allergen, on_delete=models.CASCADE)
    unique_together = [['recipe', 'contains_allergen']]

    class Meta:
        db_table = 'recipes_recipes_allergens'


class RecipeCuisine(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    unique_together = [['recipe', 'cuisine']]

    class Meta:
        db_table = 'recipes_recipes_cuisines'


class RecipeDiet(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    unique_together = [['recipe', 'diet']]

    class Meta:
        db_table = 'recipes_recipes_diets'


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unique_together = [['recipe', 'diet']]

    class Meta:
        db_table = 'recipes_recipes_categories'
