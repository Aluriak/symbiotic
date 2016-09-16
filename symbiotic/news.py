
from itertools import islice
import feedparser
from symbiotic.data import Data


BIOINFOFR_RSS = 'http://bioinfo-fr.net/feed'


def fetch(max_article=None):
    if not max_article:
        payload = Data.from_file()
        max_article = int(payload.news_options['max_article'])
    assert max_article >= 1
    print("fetching the {} last articles from bioinfo-fr.net…".format(max_article))
    parser = feedparser.parse(BIOINFOFR_RSS)
    for entry in islice(parser.entries, 0, max_article):
        print('#', entry.title)
        print(entry.link)
        print()
