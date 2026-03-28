from typing import Iterable

from cli.cli_inout_streamer import CLIInOutStreamer
from cli.cli_renderer import CLIStaffRenderer
from task import Task


class CLIInteractor:
    def __init__(self, notes_lang: str, exit_commands: Iterable[str]) -> None:
        self.exit_commands = exit_commands
        self.notes_lang = notes_lang
        self.inout_streamer = CLIInOutStreamer()
        self.renderer = CLIStaffRenderer()

    def render_task(self, task: Task) -> None:
        self.inout_streamer.clear()
        for line in self.renderer.render(task=task):
            self.inout_streamer.put_line(f"{line}\n")

    def get_user_input(self) -> str:
        user_input = self.inout_streamer.get_line().strip()
        if user_input.lower() in self.exit_commands:
            raise KeyboardInterrupt
        return user_input

    def print_string(self, string: str) -> None:
        self.inout_streamer.put_line(string)

    def wait_continue(self) -> None:
        self.inout_streamer.put_line("Нажмите для продолжения...")
        self.inout_streamer.get_line()
