from typing import TypedDict, Optional
import os
from dotenv import load_dotenv


class RedditConfig(TypedDict):
    client_id: str
    client_secret: str
    user_agent: str


class Config:
    _instance: Optional['Config'] = None

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self) -> None:
        load_dotenv()  # Load environment variables from .env file
        
        # Load Reddit configuration
        self.reddit = RedditConfig(
            client_id=os.getenv("REDDIT_CLIENT_ID", ""),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
            user_agent=os.getenv("REDDIT_USER_AGENT", "")
        )
