def scrape_image_ogp(soup_html):
    # Open Graph Protocol Meta tag.
    # <meta property="og:image" content="url" />
    image_url = soup_html.find(
        'meta',
        {'property': 'og:image'}
    )
    if image_url:
        image_url = image_url['content']
    return image_url


def scrape_epicurious_img(soup_html):
    image_url = None
    images = soup_html.find_all('img')
    for image in images:
        if (
            'alt' in image and
            image['alt'] != 'Epicurious' and
            'Photo of ' not in image['alt']
        ):
            image_url = image['src']
    return image_url


def scrape_budget_bytes_img(soup_html):
    title = soup_html.find(
        'meta',
        {'property': 'og:title'}
    )
    if title:
        title = title.get_text()
    image_url = None
    images = soup_html.find_all('img')
    for image in images:
        if (
            'data-pin-title' in image and
            image['data-pin-title'] == title
        ):
            image_url = image['data-src']
    return image_url


def scrape_img(soup_html):
    # <img src=”IMAGE_URL”>
    image_url = soup_html.find('img')
    if image_url:
        image_url = image_url['src']
    return image_url


def scrape_recipe_image_url(soup_html):
    image_url = scrape_image_ogp(soup_html)
    if not image_url:
        image_url = scrape_epicurious_img(soup_html)
    # if not image_url:
    #     image_url = scrape_budget_bytes_img(soup_html)
    if not image_url:
        image_url = scrape_img(soup_html)
    return image_url
