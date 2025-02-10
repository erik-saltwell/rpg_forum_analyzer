"""
StackExchange Scraper Implementation using StackAPI

Implements ForumScraper interface to retrieve RPG-related conversations from StackExchange sites.
"""

from datetime import datetime
from typing import Iterator, Set, List
from stackapi import StackAPI, StackAPIError
from core.ConversationNode import ConversationNode
from scrapers.ForumScraper import ForumScraper
from utils.config_loader import Config
from utils.logger import logger


class StackExchangeScraper(ForumScraper):
    """
    Scrapes RPG-related content from Stack Exchange sites using the official API.

    Utilizes StackAPI wrapper for API interaction with automatic retries and backoff.

    Requires configuration in .env:
    - STACKEXCHANGE_API_KEY: Valid API key from Stack Apps
    - STACKEX_SITE: Site ID (default: 'rpg')
    - SE_CONTENT_FILTER: Content filter ID (default: 'withbody')

    Args:
        keywords: Set of search terms to filter discussions
    """
    
    def __init__(self, *keywords: str) -> None:
        """
        Initialize scraper with validated configuration and API client.

        Raises:
            ValueError: If missing required config or empty keywords
        """
        if not keywords:
            raise ValueError("At least one search keyword required")

        self.keywords = {k.lower() for k in keywords}
        self.config = Config().stackexchange

        # Validate configuration
        required_config = ['api_key', 'site', 'content_filter']
        missing = [field for field in required_config
                   if not getattr(self.config, field)]
        if missing:
            raise ValueError(f"Missing StackExchange config: {', '.join(missing)}")

        self.stackapi = StackAPI(
            site=self.config.site,
            key=self.config.api_key,
            page_size=100
        )

    def Scrape(self, limit: int = 50) -> Iterator[ConversationNode]:
        """
        Retrieve conversation trees matching keywords.

        Args:
            limit: Maximum number of conversations to return

        Yields:
            ConversationNode objects representing discussion threads

        Raises:
            StackAPIError: For API-related failures after retries
        """
        self.stackapi.max_pages = limit/100
        if limit % 100 ==0:
            self.stackapi.max_pages = self.stackapi.max_pages+1

        posts = self.stackapi.fetch('questions')
        yield