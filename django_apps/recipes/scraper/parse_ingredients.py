import re
from fuzzywuzzy import fuzz

from django_apps.foods.models import Food

from django_apps.recipes.models import Ingredient


def parse_numerator(ingredient_str, units_by_name_and_abbr):
    # 3oz. Parmesan, grated (about ¾ cup)
    # 1 cup shelled fresh peas (from about 1 pound pods) or frozen peas, thawed
    # 1 1/2cup beans"
    numerator = None
    for unit_name in units_by_name_and_abbr:
        matches = re.match(
            f'^(\d+)( *)(\d*)(/*)(\d*)( *){unit_name}(.*)', ingredient_str)
        if not matches:
            continue
        whole_number = matches[1]
        numerator = matches[3]
        denominator = matches[5]
        if numerator != '' and denominator != '':
            numerator = int(whole_number) * int(denominator) + int(numerator)
        else:
            numerator = int(whole_number)
        return numerator
    return numerator


def parse_denominator(ingredient_str, units_by_name_and_abbr):
    denominator = None
    for unit_name in units_by_name_and_abbr:
        matches = re.match(
            f'^(\d+)( *)(\d*)(/*)(\d*)( *){unit_name}(.*)', ingredient_str)
        if not matches:
            continue
        denominator = (
            1
            if matches[5] == ''
            else int(matches[5])
        )
        return denominator
    return denominator


def parse_unit(ingredient_str, units_by_name_and_abbr):
    for unit_name in units_by_name_and_abbr:
        matches = re.match(
            f'^(\d+)( *)(\d*)(/*)(\d*)( *){unit_name}(.*)', ingredient_str)
        if matches:
            return units_by_name_and_abbr[unit_name]
    return None


def parse_food_str(ingredient_str, units_by_name_and_abbr):
    for unit_name in units_by_name_and_abbr:
        matches = re.match(
            f'^(\d+)( *)(\d*)(/*)(\d*)( *){unit_name}([ +]|[,+]|[\.+])(.+)[(*]',
            ingredient_str
        )
        if matches:
            food_str = matches[8]
            # remove any modifiers:
            food_str = food_str.split(',')[0].replace('.', '').strip().lower()
            # find paren
            match = re.match(f'^(.*)[(+](.*)[)+](.*)', food_str)
            # if paren, remove
            if match:
                paren = f'({match[2]})'
                food_str = food_str.replace(paren, '').strip()
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
    print(food_str)
    if not food_str:
        return None
    food = get_closest_matching_food(food_str) or None
    return food


def parse_ingredient(ingredient_str, units_by_name_and_abbr):
    # Create ingredient but DO NOT SAVE.
    ingredient = Ingredient()
    ingredient.numerator = parse_numerator(
        ingredient_str, units_by_name_and_abbr)
    ingredient.denominator = parse_denominator(
        ingredient_str, units_by_name_and_abbr)
    ingredient.unit = parse_unit(ingredient_str, units_by_name_and_abbr)
    food = parse_food(ingredient_str, units_by_name_and_abbr)
    if food is None:
        return None
    ingredient.food = food
    return ingredient
