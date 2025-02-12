from attr import dataclass
from core.ConversationNode import ConversationNode
from processing.content_classifier import ContentType


@dataclass
class PostData:
    Conversation: ConversationNode
    ContentTypeAssessments: list[ContentType]
    FinalAssessment: ContentType
