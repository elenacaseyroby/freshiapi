from django.db import models
from django.utils.functional import cached_property

from django_apps.foods.models import (
    get_unit_conversions_dict,
    USDACategory,
    Nutrient,
    NutritionFact as FoodNutritionFact
)

from math import floor


class Source(models.Model):
    # Many Recipes to one Source
    name = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=False, blank=False)

    class Meta:
        db_table = 'recipes_sources'

    def __str__(self):
        return self.name or self.website


class Allergen(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'recipes_allergens'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'recipes_categories'

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'recipes_cuisines'

    def __str__(self):
        return self.name


class Diet(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'recipes_diets'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    # If on scrape it finds no info, email the url and recipe id to casey
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=75, null=True, blank=True)
    servings_count = models.PositiveSmallIntegerField(null=True, blank=True)
    prep_time = models.DurationField(null=True, blank=True)
    cook_time = models.DurationField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(
        'users.User', on_delete=models.RESTRICT, null=True, blank=True)
    source = models.ForeignKey(
        Source, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    ingredients = models.ManyToManyField(
        'foods.Food', through='Ingredient', blank=True)

    # This field tracks how many ingredients were included in the 
    # calculation of the recipe's nutrition facts. For example
    # if none of the ingredients are matched to foods in the foods table, then 
    # 0% of the ingredients were included in the calculation of the nutrition
    # facts.
    ingredients_in_nutrition_facts = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True)

    # Uploaded by users to Freshi.
    user_photos = models.ManyToManyField(
        'media.Photo', through='RecipePhoto', blank=True)

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

    @cached_property
    def internet_image_url(self):
        image = RecipeInternetImage.objects.filter(recipe_id=self.id).first()
        if image:
            return image.url
        return None

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
        # This is lazy.  Clean up later.
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

    def save_nutrition_facts(self, ingredients=None, recipe_ingredient_count=None):
        if not ingredients:
            ingredients = Ingredient.objects.filter(recipe_id=self.id).all()
        # If no ingredients, then no nutrition facts to document.
        
        # Track the percentage of the ingredients that were used to 
        # calculate the nutrition facts for the recipe.
        # Start by setting ingredients_in_nutrition_facts to 0% and
        # update as you go.
        self.ingredients_in_nutrition_facts = 0
        if len(ingredients) == 0:
            self.save()
            return
        # Track ingredients parsed to later update
        # ingredients_in_nutrition_facts %.
        ingredients_w_nutrition_facts = 0

        nutrition_facts = {}
        conversions = get_unit_conversions_dict()
        for ingredient in ingredients:
            qty_numerator = ingredient.qty_numerator
            qty_denominator = ingredient.qty_denominator
            unit = ingredient.qty_unit

            # If numerator exists but denominator is None
            # set denominator = 1.
            if qty_numerator and not qty_denominator:
                qty_denominator = 1

            # Skip and mark nutrition facts incomplete i
            # if no numerator
            if not qty_numerator:
                continue

            ingredients_w_nutrition_facts += 1
            # Get food's nutrition facts from database.
            food_nutrition_facts = FoodNutritionFact.objects.filter(
                food_id=ingredient.food_id).all()

            # Add them to the recipe nutrition facts
            for fact in food_nutrition_facts:
                food_nutrient_qty = float(fact.nutrient_qty)
                # If nutrient hasn't been added to recipe_nutrition_facts
                # initialize with 0.
                if fact.nutrient_id not in nutrition_facts:
                    nutrition_facts[fact.nutrient_id] = float(0)
                # If no unit, then we will take
                # the qty to be the number of servings of the food
                # in the recipe (ex. '3 onions' would be 3 servings of onion).
                # Multiply nutrient qty in one serving of food
                # by number of food servings.
                if not unit:
                    food_servings = float(qty_numerator)/float(qty_denominator)
                    ingredient_nutrient_qty = float(
                        food_nutrient_qty * food_servings
                    )
                # Commenting this out because it leads to issues like
                # counting the recipe as having 100g of salt per serving
                # because the serving size of salt in our db is 100g 
                # (a relic of the usda food db):
                # If no ingredient qty and no unit, calculate ingredient
                # nutrient qty by takinging the food nutrient_qty for
                # one serving and multiplying it by the number of servings in
                # the recipe.
                # elif not qty_numerator and not unit:
                #     recipe_servings = float(
                #         1
                #         if self.servings_count is None else
                #         self.servings_count
                #     )
                #     ingredient_nutrient_qty = float(
                #         food_nutrient_qty * recipe_servings
                #     )
                # Else nutrient qty per one serving food to
                # nutrient qty per qty of food in ingredient.
                else:
                    ingredient_qty = round(
                        qty_numerator/qty_denominator, 2)
                    food = ingredient.food
                    # Get food qty in food serving units.
                    ingredient_qty_in_food_unit = ingredient_qty
                    # convert ingredient to same unit as food if necessary.
                    if ingredient.qty_unit.id is not food.one_serving_unit_id:
                        ingredient_qty_in_food_unit = (
                            ingredient_qty * conversions[
                                ingredient.qty_unit.id
                            ][
                                food.one_serving_unit_id
                            ]
                        )
                        
                    # Find food servings in ingredient.
                    ingredient_food_servings = round(
                        float(
                            ingredient_qty_in_food_unit /
                            float(food.one_serving_qty)
                        ),
                        2
                    )
                    # Find nutrient qty for ingredient.
                    ingredient_nutrient_qty = float(
                        float(fact.nutrient_qty) * ingredient_food_servings
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

        # Create new nutrition facts for recipe.
        # 1. Get servings count
        # Set servings count 1, if no calories or servings count for recipe:
        calories = Nutrient.objects.get(name='calories')
        if calories.id not in nutrition_facts and self.servings_count is None:
            self.servings_count = 1
        # Set servings count to break recipe very roughly into
        # ~400 cal serving sizes.
        elif self.servings_count is None:
            self.servings_count = floor(
                int(nutrition_facts[calories.id]) / 400)
            if self.servings_count == 0:
                self.servings_count = 1
        # Else servings_count is already set.

        NutritionFact.objects.bulk_create([
            NutritionFact(
                recipe_id=self.id,
                nutrient_id=nutrient_id,
                nutrient_qty=round(
                    float(nutrition_facts[nutrient_id]/self.servings_count), 2),
            ) for nutrient_id in nutrition_facts
        ])
        # Save note about nutrition facts
        if recipe_ingredient_count:
            self.ingredients_in_nutrition_facts = round(
                ingredients_w_nutrition_facts / recipe_ingredient_count, 
                2)
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
    unique_together = [['recipe', 'photo']]

    class Meta:
        db_table = 'recipes_recipes_photos'


class RecipeInternetImage(models.Model):
    # For images from the internet that we don't legally own.
    # urlfield too short to be useful.
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    url = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    unique_together = [['recipe', 'url']]

    # Django admin display name
    def __str__(self):
        return str(self.url)

    class Meta:
        db_table = 'recipes_internet_images'


class Direction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.PositiveSmallIntegerField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'recipes_directions'
        ordering = ('step',)


class Ingredient(models.Model):
    food = models.ForeignKey(
        'foods.Food', on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # qty_numerator / qty_denominator in qty_unit
    qty_numerator = models.PositiveSmallIntegerField(null=True, blank=True)
    qty_denominator = models.PositiveSmallIntegerField(null=True, blank=True)
    # Leave blank for something like 1 banana
    qty_unit = models.ForeignKey(
        'foods.Unit', on_delete=models.CASCADE, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)

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
    unique_together = [['recipe', 'category']]

    class Meta:
        db_table = 'recipes_recipes_categories'
