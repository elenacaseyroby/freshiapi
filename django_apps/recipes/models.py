from django.db import models
from django.utils.functional import cached_property


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

    @cached_property
    def is_original(self):
        return self.owner is not None

    def update_nutrition_facts(self):
        return 'placeholder'

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
    qty_denominator = models.PositiveSmallIntegerField(null=True, blank=True)
    # Leave blank for something like 1 banana
    qty_unit = models.ForeignKey(
        'foods.Unit', on_delete=models.CASCADE, null=True, blank=True)

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

################################################
# Recipe Scraper
################################################

    ################################################
    # Recipe Nutrition Facts Functions
    ################################################
    # def CalculateNutritionFacts(ingredients_list):
    # output nutrition_facts_list
    # def GetNutritionFactsToUpdate(
    #   old_nutrition_facts_list, new_nutrition_facts_list)
    # output old_nfs_to_update
    # def GetNutritionFactsToDelete(
    #   old_nutrition_facts_list, new_nutrition_facts_list)
    # output old_nfs_to_delete

    ################################################

    #     # object label in admin
    #     def __str__(self):
    #         return str(self.usdanutrient_id)

    #     class Meta:
    #         db_table = '"foods_recipes"'

    # class Image(models.Model):
    #     url =
    #     owner = models.ForeignKey(
    #         User, on_delete=models.CASCADE, null=True)

    # ingredient.convert_unit(to_unit_id):
    # if the unit_ids are equal, return self
    # converted_ingredient = self OR db.Ingredient() # proxy model #don't save or
    #   it will update the ingredient record in db
    # qty_conversion_coefficient = self.unit.conversions.findOne(where to_unit_id =
    #   to_unit_id).qty_conversion_coefficient
    # converted_ingredient.food_qty = self.food_qty * qty_conversion_coefficient
    # converted_ingredient.unit_id = to_unit_id
    # returns proxy ingredient object and doesn't save the conversion.
    # run the save method on the returned object to save the conversion in the db.
    # return converted_ingredient

    # ingredient.food_servings (cached custom property):
    # ingredient_food = self.food # if this would ever be in loop and it truly
    #   queries each time, we will need to optimize.
    # converted_ingredient = self.convert_unit(to_unit_id =
    #   ingredient_food.unit_id)
    # return converted_ingredient.food_qty / ingredient_food.serving_size_qty

    # food_nutrient.convert_unit(to_unit_id):
    # if (self.nutrient_unit_id === to_unit_id) return self
    # converted_food_nutrient = self OR db.FoodNutrient() # proxy model #don't
    #   save or it will update the food_nutrient record in db
    # qty_conversion_coefficient = self.nutrient_unit.conversions.findOne(where
    #   to_unit_id = to_unit_id).qty_conversion_coefficient
    # converted_food_nutrient.nutrient_qty =
    #   self.nutrient_qty * qty_conversion_coefficient
    # converted_food_nutrient.unit_id = to_unit_id
    # returns proxy food_nutrient object and doesn't save the conversion.
    # run the save method on the returned object to save the conversion in the db.
    # return converted_food_nutrient

    # food_nutrient.percent_dv (cached custom property):
    # nutrient = food_nutrient.nutrient
    # converted_food_nutrient = food_nutrient.convert_unit(to_unit_id =
    #   nutrient.dv_unit_id)
    # return converted_food_nutrient.nutrient_qty / nutrient.dv_qty

    # ingredient.nutritional_breakdown (cached):
    # ingredient_food = self.food
    # ingredient_cals = ingredient_food.cals * self.food_servings
    # ingredient_nutrients = []
    # for food_nutrient in ingredient_food.food_nutrients:
    #   food = food_nutrient.food
    #   ingredient_nutrient = db.IngredientNutrient() use object, don't save
    #   ingredient_nutrient.name = food.name
    #   ingredient_nutrient.percent_dv =
    #       food_nutrient.percent_dv * self.food_servings
    #   ingredient.nutrients.append(ingredient_nutrient)

    # recipe.nutrient_breakdown (cached property-- yeah.. cached in the db lol):
    # will be more efficient without using ingredient.nutritional_breakdown in a
    #   loop...
    # try to bulk calculate
    # maybe use proxy models to make all the food_nutrients and ingredients
    #   normalized before calculating everything? idk yikes
