from abc import ABC, abstractmethod
from typing import Iterator
from conversation_node import ConversationNode
from enum import Enum


class ForumScraper(ABC):
    @abstractmethod
    def scrape(self) -> Iterator[ConversationNode]:
        pass


class ForumType(Enum):
    REDDIT = "reddit"
    STACK_EXCHANGE = "stack_exchange"


class ForumScraperFactory:
    def create_scraper(
        self, forum_type: ForumType, tags: list[str]
    ) -> None:  # change the signature to use varargs AI!
        pass
