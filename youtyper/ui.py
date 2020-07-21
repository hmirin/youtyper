from __future__ import annotations

import curses
import time
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from .analyzers.analyzer import Analytics, Analyzer
    from .lessons.lessons import Lesson

from .analyzers.analyzer import calculate_all_analytics
from .logs import LessonLog


def show_and_calculate_analytics(
    win: curses.window,
    start_line: int,
    analyzers: List[Analyzer],
    current_lesson_log: LessonLog,
    former_lesson_logs: List[LessonLog],
) -> Tuple[List[Analytics], List[Analytics]]:
    lines = start_line
    single_lesson_analytics, whole_lesson_analytics = calculate_all_analytics(
        current_lesson_log, former_lesson_logs, analyzers
    )
    win.addstr(lines, 0, "Current Lesson:")
    for analytics in single_lesson_analytics:
        win.addstr(lines + 1, 0, analytics.printable_result)
        lines += len(analytics.printable_result.split("\n"))
    lines += 2
    win.addstr(lines, 0, "Whole Lesson:")
    for analytics in whole_lesson_analytics:
        win.addstr(lines + 1, 0, analytics.printable_result)
        lines += len(analytics.printable_result.split("\n"))
    return single_lesson_analytics, whole_lesson_analytics


class LessonWindow(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def start(
        lesson: Lesson,
        analyzers: List[Analyzer],
        former_lesson_logs: Optional[List[LessonLog]] = None,
    ) -> Optional[LessonLog]:
        if former_lesson_logs is None:
            former_lesson_logs = list()
        text = lesson.text
        mistakes = [""] * len(text)
        first_miss = ""
        lesson_log = LessonLog()
        current_str = ""
        aborted = False
        try:
            win = curses.initscr()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
            curses.noecho()
            while len(current_str) < len(text):
                win.clear()
                curses.curs_set(0)
                missed_str = "".join([c if c else " " for c in mistakes])
                win.addstr(0, 8, missed_str)
                win.addstr(0, 0, "Miss: ")
                win.addstr(1, 0, "Lesson: ")
                win.addstr(1, 8, text)
                win.attron(curses.A_BOLD)
                win.addstr(1, 8, current_str)
                for idx, (mistake, char) in enumerate(zip(mistakes, text)):
                    if idx > len(current_str):
                        break
                    elif mistake:
                        win.attron(curses.color_pair(1))
                        win.addstr(1, 8 + idx, char)
                        win.attroff(curses.color_pair(1))
                    else:
                        win.addstr(1, 8 + idx, char)
                win.attron(curses.color_pair(2))
                win.addstr(1, 8 + len(current_str), text[len(current_str)])
                win.attroff(curses.color_pair(2))
                win.attroff(curses.A_BOLD)
                show_and_calculate_analytics(
                    win, 3, analyzers, lesson_log, former_lesson_logs
                )
                win.addstr(2, 8 + len(current_str), "")
                time.sleep(0.05)
                key = win.getkey()
                target = text[len(current_str)]
                lesson_log.record_key(key, target)
                if key == target:
                    mistakes[
                        len(current_str)
                    ] = first_miss  # if no mistake, first_miss == ""
                    current_str = current_str + key
                    first_miss = ""
                elif key:
                    curses.flash()
                    mistakes[len(current_str)] = key
                    if not first_miss:
                        first_miss = key
        except:
            aborted = True
        finally:
            curses.endwin()
            return lesson_log if not aborted else None
