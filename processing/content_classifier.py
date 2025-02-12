from enum import Enum
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Callable, Iterable

from numpy import double
from core.ConversationNode import ConversationNode
from core.PostData import PostData


class ContentType(int, Enum):
    OTHER = 0
    RULES_QUESTION = 1
    SCENARIO_DESIGN = 2
    PRODUCT_REVIEW = 3
    SHOW_AND_TELL = 4


def generate_post_type_assessments(posts: Iterable[ConversationNode], llm_generators: Iterable[Callable[[], BaseChatModel]]) -> list[PostData]:
    return_value: list[PostData] = [PostData(post, [], ContentType.OTHER) for post in posts]
    for generator in llm_generators:
        llm: BaseChatModel = generator()
        for post in return_value:
            assessment: ContentType = _analyze_content_type_single(post.Conversation.text, llm)
            post.ContentTypeAssessments.append(assessment)
    for post in return_value:
        post.FinalAssessment = _coalesce_content_types(post.ContentTypeAssessments)
    return return_value


def _coalesce_content_types(content_types: list[ContentType]) -> ContentType:
    total_assessments: double = double(len(content_types))
    quorum_threshold = total_assessments / 2.0
    for type in ContentType:
        if _is_coalesced_content_type(content_types, type, total_assessments, quorum_threshold):
            return type
    return ContentType.OTHER


def _is_coalesced_content_type(content_types: list[ContentType], type_to_check: ContentType, total_assessments: double, quorum_threshold: double) -> bool:
    total_count_of_type = sum([1.0 if content == type_to_check else 0.0 for content in content_types])
    if total_count_of_type >= quorum_threshold:
        return True
    return False


def _convert_to_content_type(text: str) -> ContentType:
    text = text.lower().strip(" \t\r\n'\"")
    results: list[int] = []

    results.append(0)
    results.append(1 if "rules" in text else 0)
    results.append(1 if "scenario" in text else 0)
    results.append(1 if "review" in text else 0)
    results.append(1 if ("show" in text and "tell" in text) else 0)

    total_results: int = sum(results)
    if total_results != 1:
        return ContentType.OTHER
    if results[ContentType.RULES_QUESTION]:
        return ContentType.RULES_QUESTION
    if results[ContentType.SCENARIO_DESIGN]:
        return ContentType.SCENARIO_DESIGN
    if results[ContentType.PRODUCT_REVIEW]:
        return ContentType.PRODUCT_REVIEW
    if results[ContentType.SHOW_AND_TELL]:
        return ContentType.SHOW_AND_TELL

    return ContentType.OTHER


def _analyze_content_type_single(content: str, llm: BaseChatModel) -> ContentType:
    template = """Acting as a professional rpg designer and redditor, please review the following tabletop-rpg related reddit post and classify it into one of the following post types:
    * Rules Question: This post is a question about the rules of a TTPRPG (tabletop roleplaying game).
    * Scenario Design Discussion: This post is a question or discussion about how to design scenarios or adventures for a TTRPG.
    * Product Review: This post is a review of tabletop roleplaying game or a tabletop roleplaying game supplement.
    * Show and Tell: This post is someone describing something cool they did in their game
    * Other: This post does not fall into any of hte above categories.

    Output Format: Your response should only be one of the following strings: 'Rules Question', 'Scenario Design Discussion', 'Product Review', 'Show and Tell', 'Other'.
    It should not include any explanation or preamble.  It should only be one of these terms with no additional text.

    Example posts:
    * Rules Question: Hi, all. I'm reading through the books with the hopes of running some games soon -- if you are local to Nagoya city in Japan, hit me up! One thing that I am a bit puzzled is reduced the player's saves, and recovering losses to those saves. On my first reading, I did not notice anything about how or when a player's save scores would be reduced. I did see how minimum stress could be raised. When I looked at the recovery options, though, I noticed that several of them had effects related to restoring save scores. This left me a bit puzzled. I hope this is a simple question with a simple answer.
    * Scenario Design: My players just crash-landed on an unknown planet, and I want to give them a tight survival horror experience. Ultimately, I plan to give them access to their first ship. Finding a fully-fledged module would be the best, but I also consider cool planet traits/secrets. My best idea so far is to make occasional glass rains. The planet is orbiting a black hole if that matters. Thanks!
    * Product Review: My table just played Another Bug Hunt and we loved it!  The tone was totally spooky.
    * Show and Tell: I wrote a thing about the set up and beginning play of a Mothership Play By Post Game on Discord using Desert Moon of Karth. Mothership Play By Post.
    * Other: Wow THE PLEA has reached COPPER BEST SELLER status on Drivethru! Thank you guys so much! We didn't think our first Mothership module would do that well! If you're missing out, here's some links for you to check out!     Begin!

    Reddit post content: {input}
    """
    prompt: PromptTemplate = PromptTemplate.from_template(template=template)

    agent: Runnable = {"input": lambda x: x["input"]} | prompt | llm
    response: BaseMessage = agent.invoke({"input": content})
    response_text: str = str(response.content)
    return _convert_to_content_type(response_text)
