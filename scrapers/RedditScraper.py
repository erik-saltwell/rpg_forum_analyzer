from scrapers.ForumScraper import ForumScraper


class _RedditScraper(ForumScraper):
    def __init__(self, subreddit_name: str) -> None:
        self.SubredditName = subreddit_name
