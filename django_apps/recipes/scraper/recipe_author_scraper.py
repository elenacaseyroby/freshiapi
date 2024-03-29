def scrape_author_meta(soup_html):
    # <meta name="author" content="Canal House">
    author = soup_html.find(
        'meta',
        {'name': 'author'}
    )
    if author:
        return author['content']
    return None


def scrape_epicurious_author(soup_html):
    # <a class="contributor"
    # href="/contributors/sohui-kim"
    # itemprop="author"
    # rel="author"
    # title="Sohui Kim"
    # data-reactid="2">Sohui Kim</a>
    author = soup_html.find(
        'a',
        {'class': 'contributor'}
    )
    if author:
        return author.get_text()
    return None


def scrape_recipe_author(soup_html):
    author = scrape_author_meta(soup_html)
    if not author:
        author = scrape_epicurious_author(soup_html)
    if author:
        return author.strip()[:74]
    return None
