#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from base_classes import BaseInOutStreamer


class CLIInOutStreamer(BaseInOutStreamer):
    def __init__(self):
        self.put_lines_count = 0

    def get_line(self) -> str:
        return sys.stdin.readline()

    def put_line(self, string: str) -> None:
        sys.stdout.write(string)
        sys.stdout.flush()
        self.put_lines_count += 1

    def clear_prev_output(self) -> None:
        for _ in range(self.put_lines_count):
            self.put_line("\033[2K\033[A")
        self.put_lines_count = 0

    def clear(self) -> None:
        self.clear_prev_output()
