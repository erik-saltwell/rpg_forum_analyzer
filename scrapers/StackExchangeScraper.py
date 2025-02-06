from datetime import datetime
from typing import Iterator, Set
import requests
from core.ConversationNode import ConversationNode
from scrapers.ForumScraper import ForumScraper
from utils.config_loader import Config


class StackExchangeScraper(ForumScraper):
    BASE_API = "https://api.stackexchange.com/2.3"

    def __init__(self, keywords: Set[str]) -> None:
        self.keywords = {k.lower() for k in keywords}
        self.config = Config().stackexchange

    def _build_search_params(self) -> dict:
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
        params = self._build_search_params()
        response = requests.get(
            f"{self.BASE_API}/search/advanced",
            params=params
        )
        response.raise_for_status()

        for post in response.json()['items'][:limit]:
            yield self._process_post(post)
