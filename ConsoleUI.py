# from rich.console import Console
from rich.progress import Progress, TaskID
from rich.traceback import install


class ConsoleUI:
    # _console: Console
    _progress: Progress
    _reddit_task_id: TaskID
    _reddit_post_count: int
    _classifier_task_id: TaskID
    _classifier_name: str
    _active_color: str = "magenta"
    _complete_color: str = "gray30"

    def __init__(self, progress: Progress):
        install(show_locals=True)
        self._progress = progress

    def start_reddit(self):
        self._reddit_task_id = self._progress.add_task(f"[{self._active_color}]Reading Reddit Posts", total=None)
        self._reddit_post_count = 0

    def update_reddit(self):
        self._reddit_post_count = self._reddit_post_count + 1
        self._progress.update(self._reddit_task_id, description=f"[{self._active_color}]Processing Reddit Post {self._reddit_post_count}", advance=1, style=self._active_color)

    def stop_reddit(self):
        self._progress.update(self._reddit_task_id, total=100, completed=100)
        self._progress.update(self._reddit_task_id, description=f"[{self._complete_color}]Reddit Processing Complete ({self._reddit_post_count})", style=self._complete_color)
        self._progress.stop_task(self._reddit_task_id)

    def start_new_classifier(self, classifier_name: str, post_count: int):
        self._classifier_task_id = self._progress.add_task(f"[{self._active_color}]" + classifier_name, total=post_count, style=self._active_color)
        self._classifier_name = classifier_name

    def update_classifier(self):
        self._progress.update(self._classifier_task_id, advance=1)

    def stop_classifier(self):
        self._progress.update(self._classifier_task_id, description=f"[{self._complete_color}]" + self._classifier_name, style=self._complete_color)
        self._progress.stop_task(self._classifier_task_id)
