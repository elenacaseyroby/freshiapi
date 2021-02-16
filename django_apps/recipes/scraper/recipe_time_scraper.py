from datetime import timedelta
import re


def get_time(time_str):
    time_str = time_str.lower()
    # Remove number from the string
    match = re.findall('^\D*(\d*).*', time_str)
    for group in match:
        try:
            time_count = int(group)
            return time_count
        except:
            return None
    return None


def get_timedelta(time_str, time_count):
    if 'hour' in time_str:
        return timedelta(hours=time_count)
    if 'minute' in time_str:
        return timedelta(minutes=time_count)


def scrape_prep_time_wprm(soup_html):
    # <span class="wprm-recipe-details
    # wprm-recipe-details-minutes
    # wprm-recipe-prep_time wprm-recipe-prep_time-minutes">10</span>
    time = None
    # Find all elements with "wprm-recipe-name" in class
    elements = soup_html.select('span[class*="wprm-recipe-prep_time-minutes"]')
    if len(elements) > 0:
        # If elements returned, set time to text of first element.
        time = timedelta(minutes=int(elements[0].get_text()))
    return time


def scrape_cook_time_wprm(soup_html):
    # <span class="wprm-recipe-details
    # wprm-recipe-details-minutes
    # wprm-recipe-cook_time
    # wprm-recipe-cook_time-minutes">5</span>
    time = None
    # Find all elements with "wprm-recipe-name" in class
    elements = soup_html.select('span[class*="wprm-recipe-cook_time-minutes"]')
    if len(elements) > 0:
        # If elements returned, set time to text of first element.
        time = timedelta(minutes=int(elements[0].get_text()))
    return time


def scrape_total_time_wprm(soup_html):
    # <span class="wprm-recipe-details
    # wprm-recipe-details-minutes
    # wprm-recipe-total_time
    # wprm-recipe-total_time-minutes">15</span>
    time = None
    # Find all elements with "wprm-recipe-name" in class
    elements = soup_html.select(
        'span[class*="wprm-recipe-total_time-minutes"]')
    if len(elements) > 0:
        # If elements returned, set time to text of first element.
        time = timedelta(minutes=int(elements[0].get_text()))
    return time


def scrape_prep_time_tasty(soup_html):
    # <span data-tasty-recipes-customization="detail-value-color.color"
    # class="tasty-recipes-prep-time">45 minutes</span>
    time = None
    time = soup_html.find('span', {'class': 'tasty-recipes-prep-time'})
    if time:
        time_str = time.get_text()
        time_count = get_time(time_str)
        time = get_timedelta(time_str, time_count)
    return time


def scrape_cook_time_tasty(soup_html):
    # <span data-tasty-recipes-customization="detail-value-color.color"
    # class="tasty-recipes-cook-time">35 minutes</span>
    time = None
    time = soup_html.find('span', {'class': 'tasty-recipes-cook-time'})
    if time:
        time_str = time.get_text()
        time_count = get_time(time_str)
        time = get_timedelta(time_str, time_count)
    return time


def scrape_total_time_tasty(soup_html):
    # <span data-tasty-recipes-customization="detail-value-color.color"
    # class="tasty-recipes-total-time">5 hours, 5 minutes (includes chilling)
    # </span>
    time = None
    time = soup_html.find('span', {'class': 'tasty-recipes-total-time'})
    if time:
        time_str = time.get_text()
        time_count = get_time(time_str)
        time = get_timedelta(time_str, time_count)
    return time


def scrape_total_time_smitten(soup_html):
    # <span class="time">4 hours</span>
    time = soup_html.find('span', {'class': 'time'})
    if not time:
        return None
    time = time.get_text().lower()
    if 'hour' in time:
        hours = get_time(time)
        time = timedelta(hours=hours)
    elif 'minute' in time:
        minutes = get_time(time)
        time = timedelta(minutes=minutes)
    return time


def scrape_recipe_prep_time(soup_html):
    time = scrape_prep_time_wprm(soup_html)
    if not time:
        time = scrape_prep_time_tasty(soup_html)
    return time


def scrape_recipe_cook_time(soup_html):
    time = scrape_cook_time_wprm(soup_html)
    if not time:
        time = scrape_cook_time_tasty(soup_html)
    return time


def scrape_recipe_total_time(soup_html):
    time = scrape_total_time_wprm(soup_html)
    if not time:
        time = scrape_total_time_tasty(soup_html)
    if not time:
        time = scrape_total_time_smitten(soup_html)
    return time
