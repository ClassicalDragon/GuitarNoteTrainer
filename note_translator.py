#!/usr/bin/python3
# -*- coding: utf-8 -*-


from base_classes import NoteNames


class NoteTranslator:
    # translations = {
    #     "RU": ("ДО", "РЕ", "МИ", "ФА", "СОЛЬ", "ЛЯ", "СИ"),
    #     "EN": ("C", "D", "E", "F", "G", "A", "H"),
    # }

    langs_available = ("RU", "EN")

    note_table = {
        "ДО": (NoteNames.C, "RU"),
        "C": (NoteNames.C, "EN"),
        "РЕ": (NoteNames.D, "RU"),
        "D": (NoteNames.D, "EN"),
        "МИ": (NoteNames.E, "RU"),
        "E": (NoteNames.E, "EN"),
        "ФА": (NoteNames.F, "RU"),
        "F": (NoteNames.F, "EN"),
        "СОЛЬ": (NoteNames.G, "RU"),
        "G": (NoteNames.G, "EN"),
        "ЛЯ": (NoteNames.A, "RU"),
        "A": (NoteNames.A, "EN"),
        "СИ": (NoteNames.H, "RU"),
        "H": (NoteNames.H, "EN"),
    }

    @staticmethod
    def str_to_note(note_str: str) -> NoteNames:
        note_str = note_str.upper()
        if note_str not in NoteTranslator.note_table:
            raise ValueError(f"There is no such note as {note_str}")
        return NoteTranslator.note_table[note_str][0]

    @staticmethod
    def note_to_str(note_name: NoteNames, lang="RU") -> str:
        lang = lang.upper()
        if lang not in NoteTranslator.langs_available:
            raise ValueError(f"There is no such language as {lang}")
        for note_str in NoteTranslator.note_table:
            if (note_name, lang) == NoteTranslator.note_table[note_str]:
                return note_str
        raise ValueError(f"There is no such note as {note_name}")
