#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Collection, Iterable

from base_classes import STAFF_NOTES, Note, get_highest_note, get_lowest_note
from task import Task


class CLIStaffRenderer:
    WIDTH = 7

    CENTER = WIDTH // 2

    def _empty(self) -> str:
        return " " * self.WIDTH

    def _line(self) -> str:
        return "—" * self.WIDTH

    def _note_short_line(self) -> str:
        row = self._empty()
        return row[: self.CENTER - 1] + "—◯—" + row[self.CENTER + 2 :]

    def _note_line(self) -> str:
        row = self._line()
        return row[: self.CENTER] + "◯" + row[self.CENTER + 1 :]

    def _note_between(self) -> str:
        row = self._empty()
        return row[: self.CENTER] + "◯" + row[self.CENTER + 1 :]

    def _ledger(self) -> str:
        row = self._empty()
        return row[: self.CENTER - 1] + "———" + row[self.CENTER + 2 :]

    def _get_note_row(self, note: Note) -> str:
        if note in STAFF_NOTES:
            return self._note_line()
        elif (note < STAFF_NOTES[0] or note > STAFF_NOTES[-1]) and int(note) % 2 == 0:
            return self._note_short_line()
        else:
            return self._note_between()

    def _get_staff_row(
        self, note_to_render: Note | None, note_on_staff: Note, are_notes_hidden: bool = False
    ) -> str:
        if note_on_staff in STAFF_NOTES:
            return self._line()
        # if note is above or below main staff and current line_pos return a ledger
        # but only for existing note_pos
        elif (
            note_to_render is not None
            and int(note_on_staff) % 2 == 0
            and (
                are_notes_hidden
                or note_on_staff > STAFF_NOTES[0]
                and note_on_staff < note_to_render
                or note_on_staff < STAFF_NOTES[4]
                and note_on_staff > note_to_render
            )
        ):
            return self._ledger()
        else:
            return self._empty()

    def _prepare_part_staff(
        self,
        note_to_render: Note | None,
        staff_range: Iterable[Note],
        are_notes_hidden: bool = False,
    ) -> list[str]:
        rows: list[str] = []
        for note_on_staff in staff_range:
            if (
                not are_notes_hidden
                and note_to_render is not None
                and note_on_staff == note_to_render
            ):
                row = self._get_note_row(note=note_to_render)
            else:
                row = self._get_staff_row(
                    note_to_render=note_to_render,
                    note_on_staff=note_on_staff,
                    are_notes_hidden=are_notes_hidden,
                )
            rows.insert(0, row)
        return rows

    def _prepare_full_staff(
        self,
        notes: Iterable[Note | None],
        staff_range: Collection[Note],
        are_notes_hidden: bool = False,
    ) -> list[str]:
        staff_parts: list[Collection[str]] = [
            tuple(f"{idx:>2} " for idx in range(len(staff_range), 0, -1))
        ]
        staff_parts.append(
            self._prepare_part_staff(
                note_to_render=None, staff_range=staff_range, are_notes_hidden=True
            )
        )
        for note in notes:
            staff_parts.append(
                self._prepare_part_staff(
                    note_to_render=note, staff_range=staff_range, are_notes_hidden=are_notes_hidden
                )
            )
        staff_parts.append(
            self._prepare_part_staff(
                note_to_render=None, staff_range=staff_range, are_notes_hidden=True
            )
        )
        # sum staff_parts together
        return ["".join(line_parts) for line_parts in zip(*staff_parts)]

    def _get_staff_range(self, notes: Iterable[Note]) -> tuple[Note, ...]:
        return tuple(
            Note.get_note_by_idx(idx)
            for idx in range(get_lowest_note(notes), get_highest_note(notes) + 1)
        )

    def render(self, task: Task) -> list[str]:
        notes_to_render = task.get_notes_to_render()
        staff_range = self._get_staff_range(notes=notes_to_render)
        # just for offsets in the beginning and the end of a staff
        return self._prepare_full_staff(
            notes=notes_to_render, staff_range=staff_range, are_notes_hidden=task.are_notes_hidden
        )
