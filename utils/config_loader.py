from typing import TypedDict, cast
import json
from pathlib import Path

class RedditConfig(TypedDict):
    client_id: str
    client_secret: str
    user_agent: str

def load_reddit_config(config_path: Path) -> RedditConfig:
    """Load Reddit API credentials from a config file"""
    with open(config_path) as f:
        config = json.load(f)
    return cast(RedditConfig, config)
