import pytest
from scrapers.RedditScraper import _RedditScraper
from core.ConversationNode import ConversationNode

def test_reddit_scraper_scrape_returns_nodes() -> None:
    scraper = _RedditScraper('mothershiprpg')
    nodes: list[ConversationNode] = list(scraper.Scrape(limit=10))
    assert len(nodes) >= 1, "Scrape should return at least one ConversationNode"
