
from itertools import islice
from symbiotic.data import Data


def fetch(max_article=None, rss_feed_url=None):
    import feedparser
    payload = Data.from_file()
    if not max_article:
        max_article = int(payload.news_options['max_article'])
    if not rss_feed_url:
        rss_feed_url = str(payload.news_options['rss_feed_url'])
    assert max_article >= 1
    print("fetching the {} last articles from {}…".format(max_article, rss_feed_url))
    parser = feedparser.parse(rss_feed_url)
    for entry in islice(parser.entries, 0, max_article):
        print('#', entry.title)
        print(entry.link)
        print()
