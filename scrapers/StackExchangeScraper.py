"""
StackExchange Scraper Implementation using StackAPI

Implements ForumScraper interface to retrieve RPG-related conversations from StackExchange sites.
"""

from datetime import datetime
from typing import Iterator, Set, List
from stackapi import StackAPI, StackAPIError
from tenacity import retry, wait_exponential, stop_after_attempt
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
    
    def __init__(self, keywords: Set[str]) -> None:
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
            page_size=100,
            max_pages=1
        )

    def _build_query_params(self) -> dict:
        """
        Construct API query parameters for advanced search.
        
        Returns:
            Dictionary of validated API parameters
        """
        return {
            'filter': self.config.content_filter,
            'q': ' OR '.join(self.keywords),
            'sort': 'creation',
            'order': 'desc',
            'closed': False
        }

    def _process_post(self, post: dict) -> ConversationNode:
        """
        Convert API post response to ConversationNode.
        
        Args:
            post: Raw API post data
            
        Returns:
            Structured conversation node with nested responses
        """
        answers: List[dict] = post.get('answers', [])
        responses = [self._process_post(answer) for answer in answers]
        
        return ConversationNode(
            text=f"{post['title']}\n{post['body']}",
            timestamp=datetime.fromtimestamp(post['creation_date']),
            responses=responses
        )

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10),
           stop=stop_after_attempt(3))
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
        try:
            response = self.stackapi.fetch(
                'search/advanced',
                **self._build_query_params()
            )
            
            items: List[dict] = response.get('items', [])[:limit]
            
            for post in items:
                yield self._process_post(post)
                
        except StackAPIError as e:
            logger.error(f"StackAPI Error [{e.code}]: {e.message}")
            if e.code == 'throttle_violation':
                logger.warning("API quota exhausted, backing off...")
            raise
        except KeyError as e:
            logger.error(f"Unexpected API response format: {str(e)}")
            return iter([])
