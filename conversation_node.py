from datetime import datetime
from typing import List

class ConversationNode:
    def __init__(self, text: str, timestamp: datetime, responses: List['ConversationNode'] = None):
        self.text: str = text
        self.timestamp: datetime = timestamp
        self.responses: List[ConversationNode] = responses if responses is not None else []
