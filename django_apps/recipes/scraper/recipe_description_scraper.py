def scrape_description_ogp(soup_html):
    # Open Graph Protocol Meta tag.
    # <meta property="og:description" content="Description" />
    description = soup_html.find(
        'meta',
        {'property': 'og:description'}
    )
    if description:
        description = description.get_text()
    return description


def scrape_description_meta(soup_html):
    # <meta name="description"
    # content="Topping these fresh blini-like pancakes
    # with smoked salmon would make an ideal appetizer for a party.">
    description = soup_html.find(
        'meta',
        {'name': 'description'}
    )
    if description:
        description = description['content']
    return description


def scrape_recipe_description(soup_html):
    description = scrape_description_ogp(soup_html)
    if not description:
        description = scrape_description_meta(soup_html)
    return description
