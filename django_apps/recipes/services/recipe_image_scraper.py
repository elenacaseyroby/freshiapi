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

# def scrape_food_image(soup_html):
#     image_url = soup_html.select('img', class_="recipe-image__img")
#     if image_url:
#         image_url = image_url['src']


def scrape_img(soup_html):
    # <img src=”IMAGE_URL”>
    image_url = soup_html.find('img')
    if image_url:
        image_url = image_url['src']
    return image_url


def scrape_recipe_image_url(soup_html):
    image_url = scrape_image_ogp(soup_html)
    if not image_url:
        image_url = scrape_img(soup_html)
    return image_url
