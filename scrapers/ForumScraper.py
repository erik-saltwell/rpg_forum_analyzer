from core.ConversationNode import ConversationNode
from typing import Iterator
from abc import ABC, abstractmethod
from ConsoleUI import ConsoleUI


class ForumScraper(ABC):
    @abstractmethod
    def Scrape(self, limit: int, ui: ConsoleUI) -> Iterator[ConversationNode]:
        pass
