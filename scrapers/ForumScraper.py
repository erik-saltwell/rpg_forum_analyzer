from ConversationNode import ConversationNode
from typing import Iterator
from abc import ABC, abstractmethod


class ForumScraper(ABC):
    @abstractmethod
    def Scrape(self) -> Iterator[ConversationNode]:
        pass
