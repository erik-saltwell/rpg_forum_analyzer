from typing import NamedTuple
from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel


class LLMData(NamedTuple):
    name: str
    generator: Callable[[], BaseChatModel]
