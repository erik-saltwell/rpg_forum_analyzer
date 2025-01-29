from scrapers.ForumScraper import ForumScraper
from scrapers.RedditScraper import _RedditScraper
from typing import Type

class ForumScraperFactory:
    @staticmethod
    def get_scraper(scraper_type: str, **kwargs) -> ForumScraper:
        if scraper_type.lower() == 'reddit':
            return _RedditScraper(**kwargs)
        else:
            raise ValueError(f"Unsupported scraper type: {scraper_type}")
