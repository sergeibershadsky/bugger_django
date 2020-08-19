from typing import List

import dramatiq
import requests
from lxml import html
from .models import Article
import logging

logger = logging.getLogger(__name__)


def get_articles() -> List[dict]:
    html_str = fetch_page()
    root = html.fromstring(html_str)
    articles = root.xpath("//a[@class='storylink']")
    return [
        dict(title=article.text, url=article.attrib['href'])
        for article in articles
    ]


def fetch_page() -> str:
    url = "https://news.ycombinator.com/"
    request = requests.get(url)
    request.raise_for_status()
    return request.text


def refresh_articles():
    articles = get_articles()
    assert len(articles) == 30, "Hackernews goes wrong"
    Article.objects.all().delete()
    Article.objects.bulk_create(
        [Article(**article) for article in articles]
    )


@dramatiq.actor
def refresh_articles_job():
    logger.info("Refresh job started")
    refresh_articles()
    logger.info("Job finished")
