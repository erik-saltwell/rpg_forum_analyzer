from typing import TypedDict
import os
from dotenv import load_dotenv

class RedditConfig(TypedDict):
    client_id: str
    client_secret: str
    user_agent: str

def load_reddit_config() -> RedditConfig:
    """Load Reddit API credentials from environment variables"""
    load_dotenv()  # Load environment variables from .env file
    
    return RedditConfig(
        client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
        user_agent=os.getenv("REDDIT_USER_AGENT", "")
    )
