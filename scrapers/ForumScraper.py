from core.ConversationNode import ConversationNode
from typing import Iterator
from abc import ABC, abstractmethod


class ForumScraper(ABC):
    @abstractmethod
    def Scrape(self, limit: int) -> Iterator[ConversationNode]:
        pass
