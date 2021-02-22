import re
from fuzzywuzzy import fuzz

from django_apps.foods.models import Food

from django_apps.recipes.models import Ingredient


def parse_numerator(ingredient_str, units_by_name, units_by_abbr):
    # 3oz. Parmesan, grated (about ¾ cup)
    # 1 cup shelled fresh peas (from about 1 pound pods) or frozen peas, thawed
    # 1 1/2cup beans"
    ingredient_str = ingredient_str.lower()
    unit_dicts_list = [units_by_name, units_by_abbr]
    numerator = None
    for unit_dict in unit_dicts_list:
        for unit_name in unit_dict:
            matches = re.match(
                f'^(\d+)(\s|-|)(\d*)(/*)(\d*)( *){unit_name}(.*)',
                ingredient_str
            )
            if not matches:
                continue
            whole_number = matches[1]
            numerator = matches[3]
            denominator = matches[5]
            if numerator != '' and denominator != '':
                numerator = int(whole_number) * \
                    int(denominator) + int(numerator)
            else:
                numerator = int(whole_number)
            return numerator
    return numerator


def parse_denominator(ingredient_str, units_by_name, units_by_abbr):
    ingredient_str = ingredient_str.lower()
    unit_dicts_list = [units_by_name, units_by_abbr]
    denominator = None
    for unit_dict in unit_dicts_list:
        for unit_name in unit_dict:
            matches = re.match(
                f'^(\d+)(\s|-|)(\d*)(/*)(\d*)( *){unit_name}(.*)',
                ingredient_str
            )
            if not matches:
                continue
            denominator = (
                1
                if matches[5] == ''
                else int(matches[5])
            )
            return denominator
    return denominator


def parse_unit(ingredient_str, units_by_name, units_by_abbr):
    ingredient_str = ingredient_str.lower()
    for unit_name in units_by_name:
        matches = re.match(
            f'^(\d+)(\s|-|)(\d*)(/*)(\d*)( *){unit_name}(.*)', ingredient_str)
        if matches:
            return units_by_name[unit_name]
    for unit_name in units_by_abbr:
        matches = re.match(
            f'^(\d+)(\s|-|)(\d*)(/*)(\d*)( *){unit_name}(\s|,|[.])',
            ingredient_str
        )
        if matches:
            return units_by_abbr[unit_name]
    return None


def remove_modifiers(food_str):
    common_modifiers = [
        'shelled', 'fresh', 'skinned', 'chopped', 'grated',
        'finely', 'coursely', 'pinch', 'low-fat', 'lowfat',
        'low fat', 'fat free', 'fat-free']
    cleaned_str = ''
    skip_char = False
    for char in food_str:
        if char == '(':
            skip_char = True
        elif char == ')':
            skip_char = False
        elif skip_char is False:
            cleaned_str = cleaned_str + char
    food_str = cleaned_str
    for mod in common_modifiers:
        food_str = food_str.replace(mod, '')
    # remove "plus more for bon appetit"
    food_str = food_str.split('plus more')[0]
    # remove anything after "or"
    food_str = food_str.split('or')[0]
    # remove anything after ","
    food_str = food_str.split(',')[0]
    # remove "."
    food_str = food_str.replace('.', '')
    # make lowercase
    food_str = food_str.lower()
    # remove all parens
    return food_str.strip()


def parse_food_str(ingredient_str, units_by_name, units_by_abbr):
    # units_by_name.update(units_by_abbr)
    # units_by_name_and_abbr = units_by_name
    # Try complicated match for instances where we don't want
    # 'g' to catch 'grated' or
    # 'oz' to catch 'frozen'
    ingredient_str = ingredient_str.lower()
    for unit_name in units_by_abbr:
        matches = re.match(
            f'^(\d+)( *)(\d*)(/*)(\d*)( *){unit_name}(\s|,|[.])(.+)',
            ingredient_str
        )
        if matches:
            food_str = matches[8]
            return remove_modifiers(food_str)
    # Then try simplier match
    for unit_name in units_by_name:
        matches = re.match(
            f'^(\d+)( *)(\d*)(/*)(\d*)( *){unit_name}(.*)', ingredient_str)
        if matches:
            food_str = matches[7]
            # Remove 's' from front if unit was plural.
            matches = re.match(f'^s (.*)', food_str)
            if matches:
                food_str = matches[1]
            return remove_modifiers(food_str)
    # Try matching without unit
    matches = re.match(f'^(\d*)(.*)', ingredient_str)
    if matches:
        food_str = matches[2]
        return remove_modifiers(food_str)
    # Otherwise just return string assuming there are no unit
    # or qty specifications
    return remove_modifiers(ingredient_str)


def get_closest_matching_food(food_str):
    foods_with_ingredient_name = Food.objects.filter(
        name__contains=food_str,
        usdacategory__search_order__lte=15).all()
    if len(foods_with_ingredient_name) == 0:
        foods_with_ingredient_name = Food.objects.filter(
            name__contains=food_str,
            usdacategory__search_order__gt=15).all()
    if len(foods_with_ingredient_name) == 0:
        foods_with_ingredient_name = Food.objects.filter(
            name__contains=food_str,
            usdacategory__search_order__isnull=True).all()
    print(
        f'there are {len(foods_with_ingredient_name)} foods w ingredient name')
    highest_match_score = 0
    food_with_highest_match_score = None
    for food in foods_with_ingredient_name:
        match_score = fuzz.ratio(food.name.lower(), food_str.lower())
        if match_score > highest_match_score:
            highest_match_score = match_score
            food_with_highest_match_score = food
    return food_with_highest_match_score


def parse_food(ingredient_str, units_by_name, units_by_abbr):
    print("parse food:")
    print(ingredient_str)
    food_str = parse_food_str(ingredient_str, units_by_name, units_by_abbr)
    print(food_str)
    if not food_str:
        return None
    food = get_closest_matching_food(food_str)
    print(food)
    return food


def parse_ingredient(ingredient_str, units_by_name, units_by_abbr):
    ingredient = Ingredient()
    # If food matched, add parse all attributes.
    food = parse_food(ingredient_str, units_by_name, units_by_abbr)
    if food:
        ingredient.food = food
        ingredient.qty_numerator = parse_numerator(
            ingredient_str, units_by_name, units_by_abbr)
        ingredient.qty_denominator = parse_denominator(
            ingredient_str, units_by_name, units_by_abbr)
        # If numerator exists and denominator dne,
        # set denominator to 1.
        if (
            ingredient.qty_numerator is not None and
            ingredient.qty_denominator is None
        ):
            ingredient.qty_denominator = 1
        ingredient.qty_unit = parse_unit(
            ingredient_str, units_by_name, units_by_abbr)
    # If food not matched, make note
    else:
        food_str = parse_food_str(ingredient_str, units_by_name, units_by_abbr)
        ingredient.notes = food_str or ingredient_str
    return ingredient
