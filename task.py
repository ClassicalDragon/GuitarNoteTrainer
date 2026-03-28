#!/usr/bin/python3
# -*- coding: utf-8 -*-


from abc import abstractmethod
from typing import Collection, Sequence

from base_classes import STAFF_NOTES, Note, NoteNames, get_lowest_note
from note_translator import NoteTranslator
from itertools import zip_longest


class Task:
    task_type: str | None = None
    TASK_TYPES: dict[str, type] = {}
    are_notes_hidden: bool = False

    def __init__(
        self, notes_num: int, notes_excludes: Collection[Note], min_octave: int, max_octave: int
    ):
        self.condition: list[Note] = []
        while len(self.condition) < notes_num:
            note = Note.get_random_note(min_octave, max_octave)
            if note not in notes_excludes and note not in self.condition:
                self.condition.append(note)

    def __init_subclass__(cls):
        cls.TASK_TYPES[cls.task_type] = cls

    @abstractmethod
    def check_answer(self, answer: Sequence[NoteNames]) -> list[bool]:
        pass

    @abstractmethod
    def get_expected_answer(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def get_init_prompt(self, *args, **kwargs) -> str:
        pass

    def get_notes_to_render(self) -> tuple[Note, ...]:
        return tuple(self.condition)

    def get_condition_str(self, notes_lang: str) -> str:
        return " ".join(
            (NoteTranslator.note_to_str(note.name, notes_lang) for note in self.condition)
        )

    @abstractmethod
    def normilize_answer(self, answer_str: str) -> list[NoteNames]:
        pass

    @classmethod
    def make_task(cls, task_type: str, *args, **kwargs) -> "Task":
        if task_type not in cls.TASK_TYPES:
            raise ValueError(f"There is no such task type as {task_type}")
        return cls.TASK_TYPES[task_type](*args, **kwargs)

    def get_result_str(self, task_results: list[bool], notes_lang: str) -> str:
        if all(task_results):
            return "Верно!\n"
        else:
            expected_answer = self.get_expected_answer(note_lang=notes_lang)
            return f"Ошибка! Это {expected_answer}\n"


class GuessNoteOnStaffTask(Task):
    task_type = "guess_notes_on_staff"

    def __init__(
        self, notes_num: int, notes_excludes: Collection[Note], min_octave: int, max_octave: int
    ):
        self.condition: list[Note] = []
        while len(self.condition) < notes_num:
            note = Note.get_random_note(min_octave, max_octave)
            if note not in notes_excludes and note not in self.condition:
                self.condition.append(note)

    def check_answer(self, answer: Sequence[NoteNames]) -> list[bool]:
        task_results = []
        trunkated_answer = answer
        if len(answer) > len(self.condition):
            trunkated_answer = answer[: len(self.condition)]
        for expected, note_name in zip_longest(self.condition, trunkated_answer):
            res = expected.name == note_name
            task_results.append(res)
        return task_results

    def get_expected_answer(self, note_lang: str) -> str:
        return " ".join(
            [
                NoteTranslator.note_to_str(note_name=note.name, lang=note_lang)
                for note in self.condition
            ]
        )

    def get_init_prompt(self, *args, **kwargs) -> str:
        plural_notes_str = "ноту" if len(self.condition) == 1 else "ноты"
        return f"Введите {plural_notes_str} cо стана или выход: "

    def normilize_answer(self, answer_str: str) -> list[NoteNames]:
        normalized_answer = []
        for word in answer_str.split():
            note_name = NoteTranslator.str_to_note(word)
            normalized_answer.append(note_name)
        return normalized_answer


class FindPlaceForNoteTask(Task):
    task_type = "find_place_for_note"
    are_notes_hidden = True

    def get_lowest_note(self) -> Note:
        lowest_staff_note = STAFF_NOTES[0]
        lowest_note = min(self.condition)
        if lowest_note > lowest_staff_note:
            lowest_note = lowest_staff_note
        return lowest_note

    def check_answer(self, answer: Collection[NoteNames]) -> list[bool]:
        task_results = []
        for expected, note_name in zip_longest(self.condition, answer):
            res = expected.name == note_name
            task_results.append(res)
        return task_results

    def get_expected_answer(self, *args, **kwargs) -> str:
        lowest_note = get_lowest_note(notes=self.condition)
        return " ".join(str(int(note) - int(lowest_note) + 1) for note in self.condition)

    def get_init_prompt(self, notes_lang: str, *args, **kwargs) -> str:
        plural_notes_str = "расположена нота" if len(self.condition) == 1 else "расположены ноты"
        return f"Введите номера строк где {plural_notes_str} {self.get_condition_str(notes_lang=notes_lang)} или выход: "

    def normilize_answer(self, answer_str: str, *args, **kwargs) -> list[NoteNames]:
        normalized_answer = []
        for word in answer_str.split():
            lowest_note = get_lowest_note(self.condition)
            note_name = Note.get_note_by_idx(int(word) + int(lowest_note) - 1).name
            normalized_answer.append(note_name)
        return normalized_answer
