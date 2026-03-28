#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse

from base_classes import Note, NoteNames
from cli.cli_interactor import CLIInteractor
from session_stats import SessionStats
from task import Task


class GuitarNoteTrainer:
    EXIT_COMMANDS = ("exit", "выход")
    EXCLUDE_NOTES_FOR_TASKS = (Note.get_note_by_name("C3"), Note.get_note_by_name("D3"))

    def __init__(
        self,
        task_type: str,
        interface: str = "CLI",
        notes_lang: str = "RU",
        notes_num: int = 1,
        min_octave: int = 3,
        max_octave: int = 6,
    ) -> None:
        self.notes_num = notes_num
        self.min_octave = min_octave
        self.max_octave = max_octave
        self.task_type = task_type
        self.notes_lang = notes_lang
        self.stats = SessionStats()
        if interface == "CLI":
            self.interactor = CLIInteractor(notes_lang=notes_lang, exit_commands=self.EXIT_COMMANDS)
        else:
            raise ValueError(f"Unsupported mode {interface}")

    def print_stats(self) -> None:
        self.interactor.print_string(self.stats.get_stats())

    def get_valid_answer(self, task: Task) -> list[NoteNames]:
        while True:
            answer = self.interactor.get_user_input()
            try:
                return task.normilize_answer(answer)
            except ValueError:
                self.interactor.print_string("Ошибка ввода, повторите: ")
            except Exception as e:
                self.interactor.print_string(f"Неизвестная ошибка обработки ввода {answer}\n{e}")

    def run(self) -> None:
        while True:
            task = Task.make_task(
                task_type=self.task_type,
                notes_num=self.notes_num,
                notes_excludes=self.EXCLUDE_NOTES_FOR_TASKS,
                min_octave=self.min_octave,
                max_octave=self.max_octave,
            )
            self.interactor.render_task(task)
            self.interactor.print_string(task.get_init_prompt(self.notes_lang))
            answer = self.get_valid_answer(task)
            task_results = task.check_answer(answer=answer)
            task_results_str = task.get_result_str(
                task_results=task_results, notes_lang=self.notes_lang
            )
            self.interactor.print_string(task_results_str)
            for res in task_results:
                self.stats.record(is_correct=res)
            self.interactor.wait_continue()

    def finish(self) -> None:
        self.stats.finish()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="GuitarNoteTrainer")
    parser.add_argument("--notes_num", type=int, default=1, help="How much notes to guess at once")
    parser.add_argument(
        "--task_type",
        type=str,
        default="guess_notes_on_staff",
        choices=Task.TASK_TYPES.keys(),
        help="Which tasks will be run",
    )
    parser.add_argument(
        "--interface",
        type=str,
        default="CLI",
        choices=("CLI",),
        help="Which interface will be used",
    )
    parser.add_argument(
        "--min_octave",
        type=int,
        default=3,
        choices=(3, 4, 5, 6),
        help="Minimum octave in the training",
    )
    parser.add_argument(
        "--max_octave",
        type=int,
        default=6,
        choices=(3, 4, 5, 6),
        help="Maximum octave in the training",
    )
    parser.add_argument(
        "--notes_lang",
        type=str,
        default="RU",
        choices=("RU", "EN"),
        help="Which language use for notes print",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    trainer = GuitarNoteTrainer(
        task_type=args.task_type,
        interface=args.interface,
        notes_lang=args.notes_lang,
        notes_num=args.notes_num,
        min_octave=args.min_octave,
        max_octave=args.max_octave,
    )
    try:
        trainer.run()
    except KeyboardInterrupt:
        pass
    trainer.finish()
    trainer.print_stats()


if __name__ == "__main__":
    main()
