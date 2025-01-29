from scrapers.ForumScraper import ForumScraper
from typing import Iterator, cast
from ConversationNode import ConversationNode
import praw
from praw.models import Comment, Submission
from datetime import datetime


class _RedditScraper(ForumScraper):
    def __init__(self, subreddit_name: str, client_id: str, client_secret: str, user_agent: str) -> None:
        self.SubredditName = subreddit_name
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def _comment_to_node(self, comment: Comment) -> ConversationNode:
        """Convert a PRAW comment to a ConversationNode"""
        responses = [self._comment_to_node(reply) for reply in comment.replies]
        return ConversationNode(
            text=comment.body,
            timestamp=datetime.fromtimestamp(comment.created_utc),
            responses=responses
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
                responses=[self._comment_to_node(comment) for comment in submission.comments]
            )
            yield root
