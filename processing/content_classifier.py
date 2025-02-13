from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Iterable
from processing.LLMData import LLMData
from numpy import double
from core.ConversationNode import ConversationNode
from core.PostData import PostData
from core.ContentType import ContentType
import logging
from langsmith import traceable
from ConsoleUI import ConsoleUI


def generate_post_type_assessments(posts: Iterable[ConversationNode], llm_generators: Iterable[LLMData], ui: ConsoleUI) -> list[PostData]:
    return_value: list[PostData] = [PostData(post, [], ContentType.OTHER) for post in posts]
    for generator in llm_generators:
        ui.start_new_classifier(generator.name, len(return_value))
        logging.info(f"Processing with: {generator.name}")

        llm: BaseChatModel = generator.generator()
        for post in return_value:
            ui.update_classifier()
            assessment: ContentType = _analyze_content_type_single(post.Conversation.text, llm)
            post.ContentTypeAssessments.append(assessment)
        ui.stop_classifier()
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
    results.append(1 if "adventure" in text else 0)

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
    if results[ContentType.ADVENTURE_QUESTION]:
        return ContentType.ADVENTURE_QUESTION

    return ContentType.OTHER


@traceable
def _analyze_content_type_single(content: str, llm: BaseChatModel) -> ContentType:
    template = """Acting as a professional rpg designer and redditor, please review the following tabletop-rpg related reddit post and classify it into one of the following post types:
    * Rules Question: This post is a question about the rules of a TTPRPG (tabletop roleplaying game).
    * Scenario Design Discussion: This post is a question or discussion about how to design scenarios or adventures for a TTRPG.
    * Product Review: This post is a review of tabletop roleplaying game or a tabletop roleplaying game supplement.
    * Show and Tell: This post is someone describing something cool they did in their game
    * Adventure Question: This post is asking questions about how to run a specific adventure or scenario published for the TTRPG.
    * Other: This post does not fall into any of hte above categories.

    Output Format: Your response should only be one of the following strings: 'Rules Question', 'Scenario Design Discussion', 'Product Review', 'Show and Tell', 'Adventure Question', 'Other'.
    It should not include any explanation or preamble.  It should only be one of these terms with no additional text.

    Example posts:
    * Rules Question: Hi, all. I'm reading through the books with the hopes of running some games soon -- if you are local to Nagoya city in Japan, hit me up! One thing that I am a bit puzzled is reduced the player's saves, and recovering losses to those saves. On my first reading, I did not notice anything about how or when a player's save scores would be reduced. I did see how minimum stress could be raised. When I looked at the recovery options, though, I noticed that several of them had effects related to restoring save scores. This left me a bit puzzled. I hope this is a simple question with a simple answer.
    * Scenario Design: Advice for more Carcanid themed scenarios Hi! So my players crit failed very badly at stopping the carcs in Anither Bug Hunt and the invasion of the milky way is due... What are some modules out there that may help or inspire this particular story arc?
    * Product Review: My table just played Another Bug Hunt and we loved it!  The tone was totally spooky.
    * Show and Tell: I wrote a thing about the set up and beginning play of a Mothership Play By Post Game on Discord using Desert Moon of Karth. Mothership Play By Post.
    * Adventure Question: Tips on running Gradient Descent. I've been readingGradient Descent, and it looks fantastic. However, I’m struggling to organize my thoughts into a cohesive overarching plot for a 2-4 session run and structure the module’s content effectively. I’d love any advice on running it , and I have a few specific questions that might help with prep: What’s the best way to track time-based events, like Troubleshooter raids? How should I handle encounters, whether they’re peaceful or hostile? Which table should I use for an encounter if there's none in the current floor?
    * Other: Wow THE PLEA has reached COPPER BEST SELLER status on Drivethru! Thank you guys so much! We didn't think our first Mothership module would do that well! If you're missing out, here's some links for you to check out!     Begin!

    Reddit post content: {input}
    """
    prompt: PromptTemplate = PromptTemplate.from_template(template=template)

    agent: Runnable = {"input": lambda x: x["input"]} | prompt | llm
    logging.info(f"llm input: {input}")
    response: BaseMessage = agent.invoke({"input": content})
    response_text: str = str(response.content)
    logging.info(f"llm output: {response_text}")
    return _convert_to_content_type(response_text)
