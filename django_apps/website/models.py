from django.db import models

# Create your models here.
# foods

# nutrients

# food_nutrients (through table)

# categories

# food_categories (this can be implied instead of through for now)

# diets

# food_diets (implied)

# units

# unit_conversions (through table unit on unit)

# ingredient.convert_unit(to_unit_id):
# if the unit_ids are equal, return self
# converted_ingredient = self OR db.Ingredient() # proxy model #don't save or it will update the ingredient record in db
# qty_conversion_coefficient = self.unit.conversions.findOne(where to_unit_id = to_unit_id).qty_conversion_coefficient
# converted_ingredient.food_qty = self.food_qty * qty_conversion_coefficient
# converted_ingredient.unit_id = to_unit_id
# returns proxy ingredient object and doesn't save the conversion.
# run the save method on the returned object to save the conversion in the db.
# return converted_ingredient

# ingredient.food_servings (cached custom property):
# ingredient_food = self.food # if this would ever be in loop and it truly queries each time, we will need to optimize.
# converted_ingredient = self.convert_unit(to_unit_id = ingredient_food.unit_id)
# return converted_ingredient.food_qty / ingredient_food.serving_size_qty

# food_nutrient.convert_unit(to_unit_id):
# if (self.nutrient_unit_id === to_unit_id) return self
# converted_food_nutrient = self OR db.FoodNutrient() # proxy model #don't save or it will update the food_nutrient record in db
# qty_conversion_coefficient = self.nutrient_unit.conversions.findOne(where to_unit_id = to_unit_id).qty_conversion_coefficient
# converted_food_nutrient.nutrient_qty = self.nutrient_qty * qty_conversion_coefficient
# converted_food_nutrient.unit_id = to_unit_id
# returns proxy food_nutrient object and doesn't save the conversion.
# run the save method on the returned object to save the conversion in the db.
# return converted_food_nutrient

# food_nutrient.percent_dv (cached custom property):
# nutrient = food_nutrient.nutrient
# converted_food_nutrient = food_nutrient.convert_unit(to_unit_id = nutrient.dv_unit_id)
# return converted_food_nutrient.nutrient_qty / nutrient.dv_qty

# ingredient.nutritional_breakdown (cached):
# ingredient_food = self.food
# ingredient_cals = ingredient_food.cals * self.food_servings
# ingredient_nutrients = []
# for food_nutrient in ingredient_food.food_nutrients:
#   food = food_nutrient.food
#   ingredient_nutrient = db.IngredientNutrient() use object, don't save
#   ingredient_nutrient.name = food.name
#   ingredient_nutrient.percent_dv = food_nutrient.percent_dv * self.food_servings
#   ingredient.nutrients.append(ingredient_nutrient)


# recipe.nutrient_breakdown (cached property-- yeah.. cached in the db lol):
# will be more efficient without using ingredient.nutritional_breakdown in a loop...
# try to bulk calculate
# maybe use proxy models to make all the food_nutrients and ingredients normalized before calculating everything? idk yikes
