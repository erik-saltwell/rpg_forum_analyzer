import pytest
from scrapers.StackExchangeScraper import StackExchangeScraper
from utils.config_loader import Config

@pytest.mark.integration
def test_returns_posts_with_mothership_keyword():
    """Test that searching for 'mothership' returns at least one conversation tree."""
    config = Config().stackexchange
    
    # Skip test if no API key configured
    if not config.api_key:
        pytest.skip("StackExchange API key not configured in environment")

    scraper = StackExchangeScraper(keywords={"mothership"})
    results = list(scraper.Scrape(limit=5))

    assert len(results) >= 1, "Expected at least one post with 'mothership' keyword"
    
    first_post = results[0]
    assert first_post.text.strip() != "", "Post text should not be empty"
    assert first_post.timestamp.year >= 2010, "Timestamp should be a reasonable year"
    assert isinstance(first_post.responses, list), "Responses should be a list of nodes"
