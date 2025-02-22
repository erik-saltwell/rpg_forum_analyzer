from attr import dataclass
from core.ConversationNode import ConversationNode
from core.ContentType import ContentType


@dataclass
class PostData:
    Conversation: ConversationNode
    EstimatedTypes: list[ContentType]
    FinalType: ContentType
    Title: str
