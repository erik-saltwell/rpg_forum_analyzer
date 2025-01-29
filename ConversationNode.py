from typing import List
from datetime import datetime

class ConversationNode:
    def __init__(self, text: str, timestamp: datetime, responses: List['ConversationNode']) -> None:
        self.text = text
        self.timestamp = timestamp
        self.responses = responses
    
    def __repr__(self) -> str:
        return f"ConversationNode(text={self.text!r}, timestamp={self.timestamp!r}, responses={self.responses!r})"
