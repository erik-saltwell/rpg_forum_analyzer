from typing import Iterator
from abc import ABC, abstractmethod
from ConsoleUI import ConsoleUI
from core.PostData import PostData


class ForumScraper(ABC):
    @abstractmethod
    def Scrape(self, limit: int, ui: ConsoleUI) -> Iterator[PostData]:
        pass
