from scrapers.ForumScraper import ForumScraper
from typing import Iterator
from core.ConversationNode import ConversationNode
import praw  # type: ignore
from praw.models import Comment  # type: ignore
from datetime import datetime
from utils.config_loader import Config


class _RedditScraper(ForumScraper):
    def __init__(self, subreddit_name: str) -> None:
        config = Config()
        reddit_config = config.reddit
        self.SubredditName = subreddit_name
        self.reddit = praw.Reddit(
            client_id=reddit_config["client_id"],
            client_secret=reddit_config["client_secret"],
            user_agent=reddit_config["user_agent"],
        )

    def _comment_to_node(self, comment: Comment) -> ConversationNode:
        """Convert a PRAW comment to a ConversationNode"""
        responses = [self._comment_to_node(reply) for reply in comment.replies]
        return ConversationNode(
            text=comment.body,
            timestamp=datetime.fromtimestamp(comment.created_utc),
            responses=responses,
        )

    def Scrape(self) -> Iterator[ConversationNode]:
        subreddit = self.reddit.subreddit(self.SubredditName)

        for submission in subreddit.hot(limit=10):
            # Ensure all comments are loaded
            submission.comments.replace_more(limit=None)

            # Create root node from submission
            root = ConversationNode(
                text=submission.selftext,
                timestamp=datetime.fromtimestamp(submission.created_utc),
                responses=[
                    self._comment_to_node(comment) for comment in submission.comments
                ],
            )
            yield root
