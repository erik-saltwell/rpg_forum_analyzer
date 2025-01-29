from scrapers.RedditScraper import _RedditScraper, ForumScraper
from core.ConversationNode import ConversationNode


def test_reddit_scraper_scrape_returns_nodes() -> None:
    scraper: ForumScraper = _RedditScraper("mothershiprpg")
    nodes: list[ConversationNode] = list(scraper.Scrape(limit=1))
    assert len(nodes) == 1, "Scrape should return at least one ConversationNode"
