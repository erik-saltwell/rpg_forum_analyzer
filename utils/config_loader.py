from typing import Optional
import os
from dotenv import load_dotenv


class Config:
    _instance: Optional["Config"] = None
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    openapi_key: str

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self) -> None:
        load_dotenv()  # Load environment variables from .env file

        # Load Reddit configuration
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
        self.reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "")
        self.openapi_key = os.getenv("OPENAI_API_KEY", "")
