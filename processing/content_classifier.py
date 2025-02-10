from enum import Enum
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class ContentType(int, Enum):
    OTHER = 0
    RULES_QUESTION = 1
    SCENARIO_DESIGN = 2
    PRODUCT_REVIEW = 3
    SHOW_AND_TELL = 4


def _analyze_content_type_single(content: str, llm) -> ContentType:
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
    prompt = PromptTemplate.from_template(template=template)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent = {"input": lambda x: x["input"]} | prompt | llm
    response = agent.invoke({"input": "What is the length of the text 'DOG' in characters?'"})
    return ContentType.OTHER
