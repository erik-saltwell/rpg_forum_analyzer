from abc import ABC, abstractmethod
from typing import Iterator
from conversation_node import ConversationNode


class ForumScraper(ABC):
    @abstractmethod
    def scrape(self) -> Iterator[ConversationNode]:
        pass
