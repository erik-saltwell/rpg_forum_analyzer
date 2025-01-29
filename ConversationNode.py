from datetime import datetime


class ConversationNode:
    def __init__(
        self,
        text: str,
        timestamp: datetime,
        responses: list["ConversationNode"] = [],
    ):
        self.text: str = text
        self.timestamp: datetime = timestamp
        self.responses: list[ConversationNode] = (
            responses if responses is not None else []
        )

    def add_response(self, comment: "ConversationNode") -> None:
        self.responses.append(comment)
