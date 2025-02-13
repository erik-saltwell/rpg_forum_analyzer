from scrapers.RedditScraper import RedditScraper, ForumScraper
from core.ConversationNode import ConversationNode
from ConsoleUI import ConsoleUI
from rich.progress import Progress
from rich.theme import Theme
from rich.console import Console


def test_single_reddit_scrape() -> None:
    _run_reddit_Scrape("mothershiprpg", 1)


def test_double_reddit_scrape() -> None:
    _run_reddit_Scrape("mothershiprpg", 2)


def _run_reddit_Scrape(subreddit_name: str, expected_post_count: int) -> None:
    with Console(theme=Theme({"bar.complete": "cyan", "bar.finished": "gray30", "bar.pulse": "cyan"})) as console:
        with Progress(console=console) as progress:
            ui: ConsoleUI = ConsoleUI(progress)
            ui.start_reddit()
            scraper: ForumScraper = RedditScraper(subreddit_name)
            nodes: list[ConversationNode] = list(scraper.Scrape(limit=expected_post_count, ui=ui))
            ui.stop_reddit()
            assert len(nodes) == expected_post_count, "Scrape should return at least 1 ConversationNode"
