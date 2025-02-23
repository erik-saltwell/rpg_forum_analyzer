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
from rich.table import Table
from core.ContentType import ContentType, to_simple_string


class ForumProcessor:
    def Process(self, subreddit_name: str, max_post_limit: int, output_classification_results: bool) -> None:
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
                results: list[list[ContentType]] = content_classifier.update_post_types(posts, llm_generators, ui)
                progress.stop()
                self.output_results_table(llm_generators, posts, results, console)

    def output_results_table(self, llm_generators: Iterable[LLMData], posts: list[PostData], results: list[list[ContentType]], console: Console) -> None:
        table = Table(title="classification results", show_lines=True)
        table.add_column("title")
        for llm in llm_generators:
            table.add_column(llm.name)
        table.add_column("Final")
        even_style = "cyan"
        odd_style = "magenta"
        for i, post in enumerate(posts):
            style = even_style if i % 2 == 0 else odd_style
            table.add_row(post.Title, *([to_simple_string(assessment) for assessment in results[i]]), to_simple_string(post.FinalType), style=style)
        console.print(table)

    def _create_llm_generators(self) -> Iterable[LLMData]:
        return_values: list[LLMData] = []
        return_values.append(LLMData("llama3.2", lambda: ChatOllama(model="llama3.2")))
        return_values.append(LLMData("mistral-nemo", lambda: ChatOllama(model="mistral-nemo")))
        # return_values.append(LLMData("falcon", lambda: ChatOllama(model="falcon")))
        return_values.append(LLMData("vicuna", lambda: ChatOllama(model="vicuna")))
        # return_values.append(LLMData("deepseek8b", lambda: ChatOllama(model="deepseek-r1:8b")))

        return return_values
