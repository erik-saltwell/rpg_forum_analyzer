from typing import Iterable
from core.PostData import PostData
import logging
from scrapers.RedditScraper import RedditScraper
from processing import content_classifier
from langchain_ollama import ChatOllama
from processing.LLMData import LLMData
from ConsoleUI import ConsoleUI
from rich.progress import Progress
from rich.theme import Theme
from rich.console import Console


class ForumProcessor:
    def Process(self, subreddit_name: str, max_post_limit: int) -> None:
        logging.basicConfig(
            filename="applog.txt",
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,  # Log file name  # Append to the log file ('w' to overwrite)  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        )
        with Console(theme=Theme({"bar.complete": "magenta", "bar.finished": "gray30", "bar.pulse": "magenta"})) as console:
            with Progress(console=console) as progress:
                ui: ConsoleUI = ConsoleUI(progress)
                ui.start_reddit()
                scraper: RedditScraper = RedditScraper(subreddit_name)
                posts: list[PostData] = list(scraper.Scrape(max_post_limit, ui))
                ui.stop_reddit()
                llm_generators: Iterable[LLMData] = self._create_llm_generators()
                content_classifier.update_post_types(posts, llm_generators, ui)
                for post in posts:
                    print(f" {post.FinalType}: {post.Title}")
                pass

    def _create_llm_generators(self) -> Iterable[LLMData]:
        return_values: list[LLMData] = []
        return_values.append(LLMData("llama3.2", lambda: ChatOllama(model="llama3.2")))
        return_values.append(LLMData("mistral-nemo", lambda: ChatOllama(model="mistral-nemo")))
        return_values.append(LLMData("falcon", lambda: ChatOllama(model="falcon")))
        return_values.append(LLMData("vicuna", lambda: ChatOllama(model="vicuna")))

        return return_values
