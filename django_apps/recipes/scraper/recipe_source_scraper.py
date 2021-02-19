import re


def scrape_source_name_ogp(soup_html):
    # Open Graph Protocol Meta tag.
    # <meta property="og:site_name" content="NAME">
    source_name = soup_html.find(
        'meta',
        {'property': 'og:site_name'}
    )
    if source_name:
        source_name = source_name['content']
    return source_name


def scrape_source_url_regex(url):
    source_url = re.match('^(?:.*://)?(?:www\.)?([^:/]*).*$', str(url))
    if source_url:
        source_url = source_url[1]
    return source_url


def scrape_recipe_source_name(soup_html):
    source_name = scrape_source_name_ogp(soup_html)
    if source_name:
        source_name = source_name.strip()[:99]
    return source_name


def scrape_recipe_source_url(url):
    source_url = scrape_source_url_regex(url)
    return source_url
