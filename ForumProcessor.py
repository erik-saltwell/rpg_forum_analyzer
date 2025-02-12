from typing import Iterable
from core.ConversationNode import ConversationNode
from core.PostData import PostData
import logging
from scrapers.RedditScraper import RedditScraper
from processing import content_classifier
from langchain_ollama import ChatOllama
from processing.LLMData import LLMData


class ForumProcessor:
    def Process(self, subreddit_name: str) -> None:
        logging.basicConfig(
            filename="applog.txt",
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,  # Log file name  # Append to the log file ('w' to overwrite)  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        )

        max_post_limit = 10  # change_this!!
        scraper: RedditScraper = RedditScraper(subreddit_name)
        conversations: list[ConversationNode] = list(scraper.Scrape(max_post_limit))
        llm_generators: Iterable[LLMData] = self._create_llm_generators()
        posts_data: list[PostData] = content_classifier.generate_post_type_assessments(conversations, llm_generators)
        for post in posts_data:
            print(post.FinalAssessment)
        pass

    def _create_llm_generators(self) -> Iterable[LLMData]:
        return_values: list[LLMData] = []
        return_values.append(LLMData("llama3.2", lambda: ChatOllama(model="llama3.2")))
        return_values.append(LLMData("mistral-nemo", lambda: ChatOllama(model="mistral-nemo")))
        # return_values.append(LLMData("falcon", lambda: ChatOllama(model="falcon")))
        return_values.append(LLMData("vicuna", lambda: ChatOllama(model="vicuna")))

        return return_values
