from scrapers.ForumScraper import ForumScraper
from typing import Iterator
from core.ConversationNode import ConversationNode
import praw  # type: ignore
from praw.models import Comment  # type: ignore
from datetime import datetime
from utils.config_loader import Config


class RedditScraper(ForumScraper):
    def _normalize_subreddit_name(self, subreddit_name: str) -> str:
        """Ensure the subreddit name does not start with 'r/' or 'r\\'."""
        subreddit_name_lower = subreddit_name.lower()
        if subreddit_name_lower.startswith("r/") or subreddit_name_lower.startswith("r\\"):
            return subreddit_name[2:]
        return subreddit_name

    def __init__(self, subreddit_name: str) -> None:
        config = Config()
        self.SubredditName = self._normalize_subreddit_name(subreddit_name)
        self.reddit = praw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent,
        )

    def _comment_to_node(self, comment: Comment) -> ConversationNode:
        """Convert a PRAW comment to a ConversationNode"""
        responses = [self._comment_to_node(reply) for reply in comment.replies]
        return ConversationNode(
            text=comment.body,
            timestamp=datetime.fromtimestamp(comment.created_utc),
            responses=responses,
        )

    def Scrape(self, limit: int) -> Iterator[ConversationNode]:
        subreddit = self.reddit.subreddit(self.SubredditName)

        for submission in subreddit.new(limit=limit):
            # Ensure all comments are loaded
            submission.comments.replace_more(limit=None)

            # Create root node from submission
            root = ConversationNode(
                text=submission.title + "\n" + submission.selftext,
                timestamp=datetime.fromtimestamp(submission.created_utc),
                responses=[self._comment_to_node(comment) for comment in submission.comments],
            )
            yield root
