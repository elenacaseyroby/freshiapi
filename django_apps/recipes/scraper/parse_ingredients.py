import re
from fuzzywuzzy import fuzz

from django_apps.foods.models import Food

from models import Ingredient


def parse_numerator(ingredient_str, units_by_name_and_abbr):
    for unit_name in units_by_name_and_abbr:
        fraction = re.match(f'^(\d+)(/*)(\d*){unit_name}', ingredient_str)
        if fraction:
            numerator = int(fraction[1])
            return numerator
    return None


def parse_denominator(ingredient_str, units_by_name_and_abbr):
    for unit_name in units_by_name_and_abbr:
        fraction = re.match(f'^(\d+)(/*)(\d*){unit_name}', ingredient_str)
        if fraction:
            denominator = fraction[3]
            if denominator == '':
                return 1
            else:
                return denominator
    return None


def parse_unit(ingredient_str, units_by_name_and_abbr):
    for unit_name in units_by_name_and_abbr:
        fraction = re.match(f'^(\d+)(/*)(\d*){unit_name}', ingredient_str)
        if fraction:
            return units_by_name_and_abbr[unit_name]
    return None


def parse_food_str(ingredient_str, units_by_name_and_abbr):
    for unit_name in units_by_name_and_abbr:
        ingredient_str_matches = re.match(
            f'^(\d+)(/*)(\d*){unit_name}(.*)', ingredient_str)
        if ingredient_str_matches:
            food_str = ingredient_str_matches[4]
            # remove any modifiers:
            food_str = food_str.split(',')[0].replace('.', '').strip().lower()
            return food_str
    return None


def get_closest_matching_food(food_str):
    foods_with_ingredient_name = Food.objects.filter(
        name__contains=food_str,
        usdacategory__search_order__lte=15).all()
    highest_match_score = 0
    food_with_highest_match_score = None
    for food in foods_with_ingredient_name:
        match_score = fuzz.ratio(food.name.lower(), food_str.lower())
        if match_score > highest_match_score:
            highest_match_score = match_score
            food_with_highest_match_score = food
    return food_with_highest_match_score


def parse_food(ingredient_str, units_by_name_and_abbr):
    food_str = parse_food_str(ingredient_str, units_by_name_and_abbr)
    if not food_str:
        return None
    food = get_closest_matching_food(food_str)
    return food


def parse_ingredient(ingredient_str, units_by_name_and_abbr):
    # Create ingredient but DO NOT SAVE.
    ingredient = Ingredient()
    ingredient.numerator = parse_numerator(
        ingredient_str, units_by_name_and_abbr)
    ingredient.denominator = parse_denominator(
        ingredient_str, units_by_name_and_abbr)
    ingredient.unit = parse_unit(ingredient_str, units_by_name_and_abbr)
    ingredient.food = parse_food(ingredient_str, units_by_name_and_abbr)
    return ingredient
