#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from typing import Optional


class SessionStats:
    def __init__(self) -> None:
        self.total: int = 0
        self.correct: int = 0
        self.start_time: float = time.time()
        self.end_time: Optional[float] = None

    def record(self, is_correct: bool) -> None:
        self.total += 1
        if is_correct:
            self.correct += 1

    def finish(self) -> None:
        self.end_time = time.time()

    def accuracy(self) -> float:
        if self.total == 0:
            return 0.0
        return self.correct / self.total

    def duration(self) -> float:
        if not self.end_time:
            return 0.0
        return self.end_time - self.start_time

    def get_stats(self) -> str:
        return (
            f"\n=== Результаты ===\n"
            f"Всего: {self.total}\n"
            f"Верно: {self.correct}\n"
            f"Точность: {self.accuracy() * 100:.2f}%\n"
            f"Время: {self.duration():.2f} сек"
        )
