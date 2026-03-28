#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class NoteNames(Enum):
    C = 0
    D = 1
    E = 2
    F = 3
    G = 4
    A = 5
    H = 6


@dataclass(frozen=True)
class Note:
    name: NoteNames
    octave: int

    MIN_OCTAVE = 0
    MAX_OCTAVE = 8

    def __str__(self) -> str:
        return f"{self.name.name}{self.octave}"

    def __lt__(self, other: Note):
        return (
            self.octave < other.octave
            or self.octave == other.octave
            and self.name.value < other.name.value
        )

    def __le__(self, other: Note):
        return (
            self.octave < other.octave
            or self.octave == other.octave
            and self.name.value <= other.name.value
        )

    def __gt__(self, other: Note):
        return (
            self.octave > other.octave
            or self.octave == other.octave
            and self.name.value > other.name.value
        )

    def __ge__(self, other: Note):
        return (
            self.octave > other.octave
            or self.octave == other.octave
            and self.name.value >= other.name.value
        )

    def __add__(self, other: int) -> Note:
        return Note.get_note_by_idx(int(self) + other)

    def __index__(self) -> int:
        return self.octave * len(NoteNames) + self.name.value

    @classmethod
    def get_note_by_name(cls, note_name: str) -> Note:
        note_name = note_name.upper()
        if (
            len(note_name) != 2
            or note_name[0] not in NoteNames._member_map_
            or not note_name[1].isdecimal()
            or int(note_name[1]) not in tuple(range(cls.MIN_OCTAVE, cls.MAX_OCTAVE + 1))
        ):
            raise ValueError(f"Wrong value for note creation used '{note_name}'")
        return Note(name=NoteNames[note_name[0]], octave=int(note_name[1]))

    @classmethod
    def get_note_by_idx(cls, note_idx: int) -> Note:
        if note_idx < 0:
            raise ValueError(f"Too small index used for a note creation: {note_idx}")
        octave = note_idx // len(NoteNames)
        note_name_val = note_idx % len(NoteNames)
        if octave > cls.MAX_OCTAVE:
            raise ValueError(f"Too big index used for a note creation: {note_idx}")
        return Note(name=NoteNames(note_name_val), octave=octave)

    @classmethod
    def get_random_note(cls, min_octave: int = 0, max_octave: int = 8) -> Note:
        return Note(
            name=NoteNames(random.randint(0, 6)), octave=random.randint(min_octave, max_octave)
        )


STAFF_NOTES = (
    Note.get_note_by_name("E4"),
    Note.get_note_by_name("G4"),
    Note.get_note_by_name("H4"),
    Note.get_note_by_name("D5"),
    Note.get_note_by_name("F5"),
)


def get_lowest_note(notes: Iterable[Note]) -> Note:
    lowest_staff_note = STAFF_NOTES[0]
    lowest_note = min(notes)
    if lowest_note > lowest_staff_note:
        lowest_note = lowest_staff_note
    return lowest_note


def get_highest_note(notes: Iterable[Note]) -> Note:
    highest_staff_note = STAFF_NOTES[-1]
    highest_note = max(notes)
    if highest_note < highest_staff_note:
        highest_note = highest_staff_note
    return highest_note


class BaseInOutStreamer:
    def put_line(self, string: str) -> None:
        raise NotImplementedError

    def get_line(self) -> str:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
