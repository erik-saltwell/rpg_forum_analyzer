from scrapers.RedditScraper import _RedditScraper, ForumScraper
from core.ConversationNode import ConversationNode


def test_single_reddit_scrape() -> None:
    _run_reddit_Scrape("mothershiprpg", 1)


def test_double_reddit_scrape() -> None:
    _run_reddit_Scrape("mothershiprpg", 2)


def _run_reddit_Scrape(subreddit_name: str, expected_post_count: int) -> None:
    scraper: ForumScraper = _RedditScraper(subreddit_name)
    nodes: list[ConversationNode] = list(scraper.Scrape(limit=expected_post_count)) 
    assert len(nodes) == expected_post_count, "Scrape should return at least 1 ConversationNode"
