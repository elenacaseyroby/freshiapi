def scrape_title_ogp(soup_html):
    # Open Graph Protocol Meta tag.
    # <meta property="og:title" content="Title" />
    title = soup_html.find(
        'meta',
        {'property': 'og:title'}
    )
    if title:
        title = title.get_text()
    return title


def scrape_title_wprm(soup_html):
    # WP Recipe Maker by Wordpress
    # <h2 class=”wprm-recipe-name wprm-block-text-bold”>Title</h2>
    title = None
    # Find all elements with "wprm-recipe-name" in class
    elements = soup_html.select('h2[class*="wprm-recipe-name"]')
    if len(elements) > 0:
        # If elements returned, set title to text of first element.
        title = elements[0].get_text()
    return title


def scrape_entry_title_wp(soup_html):
    # SEO plugin wordpress
    # <h1 class=”entry-title”>title</h1>
    title = soup_html.find('h1', class_='entry-title')
    if title:
        title = title.get_text()
    return title


def scrape_title(soup_html):
    # <title>title</title>
    title = soup_html.find('title')
    if title:
        title = title.get_text()
    return title


def scrape_recipe_title(soup_html):
    title = scrape_title_ogp(soup_html)
    if not title:
        title = scrape_title_wprm(soup_html)
    if not title:
        title = scrape_entry_title_wp(soup_html)
    if not title:
        title = scrape_title(soup_html)
    if title:
        title = title[:99]
    return title
