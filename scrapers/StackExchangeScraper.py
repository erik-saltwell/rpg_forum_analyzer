from datetime import datetime
from typing import Iterator, Set
from stackapi import StackAPI, StackAPIError
from core.ConversationNode import ConversationNode
from scrapers.ForumScraper import ForumScraper
from utils.config_loader import Config
from utils.logger import logger


class StackExchangeScraper(ForumScraper):

    def __init__(self, keywords: Set[str]) -> None:
        self.keywords = {k.lower() for k in keywords}
        self.config = Config().stackexchange
        self.stackapi = StackAPI(
            site=self.config.site,
            key=self.config.api_key,
            page_size=100,
            max_pages=1
        )

    def _build_query_params(self) -> dict:
        return {
            'site': self.config.site,
            'key': self.config.api_key,
            'filter': self.config.content_filter,
            'q': ' OR '.join(self.keywords),
            'sort': 'creation'
        }

    def _process_post(self, post: dict) -> ConversationNode:
        responses = [
            self._process_post(answer)
            for answer in post.get('answers', [])
        ]
        return ConversationNode(
            text=f"{post['title']}\n{post['body']}",
            timestamp=datetime.fromtimestamp(post['creation_date']),
            responses=responses
        )

    def Scrape(self, limit: int = 50) -> Iterator[ConversationNode]:
        try:
            response = self.stackapi.fetch(
                'search/advanced',
                **self._build_query_params()
            )
            
            for post in response.get('items', [])[:limit]:
                yield self._process_post(post)

        except StackAPIError as e:
            logger.error(f"StackAPI Error: {e.message}")
            if e.code == 'throttle_violation':
                logger.warning("API quota exhausted, backing off...")
            return []
