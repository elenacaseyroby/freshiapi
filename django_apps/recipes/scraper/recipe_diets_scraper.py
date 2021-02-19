def scrape_recipe_diets_mentioned(soup_html, all_diet_names):
    description = soup_html.find(
        'meta',
        {'name': 'description'}
    )
    if not description:
        return []
    description = description['content']
    diet_names = []
    for name in all_diet_names:
        if name not in description:
            continue
        diet_names.append(name)
    return diet_names


def scrape_recipe_diets_meta(soup_html, all_diet_names):
    # <meta name="keywords" content="
    # recipes,appetizer,breakfast,brunch,
    # cocktail party,cottage cheese,pancake,
    # party,pea,green onion scallion,spring,spring pea,web">
    diets = []
    element = soup_html.find('meta', {'name': 'keywords'})
    if not element:
        return []
    keywords = str(element['content']).lower().split(',')
    for keyword in keywords:
        if keyword.strip() not in all_diet_names:
            continue
        diets.append(keyword.strip())
    return diets


def scrape_recipe_diets(soup_html, all_diet_names):
    diet_names = scrape_recipe_diets_mentioned(soup_html, all_diet_names)
    diet_names.extend(scrape_recipe_diets_meta(soup_html, all_diet_names))
    return diet_names
