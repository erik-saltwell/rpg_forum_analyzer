from scrapers.ForumScraper import ForumScraper
from typing import Iterator
from ConversationNode import ConversationNode


class _RedditScraper(ForumScraper):
    def __init__(self, subreddit_name: str) -> None:
        self.SubredditName = subreddit_name

    def Scrape(self) -> Iterator[ConversationNode]:
        return iter([])
