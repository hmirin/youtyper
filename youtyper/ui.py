import curses
import time
from typing import List, Optional, Tuple

from .analyzers.analyzer import Analytics, Analyzer, calculate_all_analytics
from .lessons.lessons import Lesson
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
        mistakes = [False] * len(text)
        lesson_log = LessonLog()
        current_str = ""
        aborted = False
        try:
            win = curses.initscr()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
            curses.noecho()
            missed = False
            key = ""
            target = ""
            while True:
                win.clear()
                curses.curs_set(0)
                if missed:
                    win.addstr(0, 0, "miss! " + key + "->" + target)
                win.addstr(1, 0, "Lesson: ")
                win.addstr(1, 8, text)
                win.attron(curses.A_BOLD)
                win.addstr(1, 8, current_str)
                for idx, (mistake, char) in enumerate(zip(mistakes, text)):
                    if idx > len(current_str):
                        break
                    if mistake:
                        win.attron(curses.color_pair(2))
                        win.addstr(1, 8 + idx, char)
                        win.attroff(curses.color_pair(2))
                    else:
                        win.addstr(1, 8 + idx, char)
                if text[len(current_str)] == " ":
                    win.attron(curses.color_pair(3))
                    win.addstr(1, 8 + len(current_str), text[len(current_str)])
                    win.attroff(curses.color_pair(3))
                else:
                    win.attron(curses.color_pair(3))
                    win.addstr(1, 8 + len(current_str), text[len(current_str)])
                    win.attroff(curses.color_pair(3))
                win.attroff(curses.A_BOLD)
                lines = 3
                show_and_calculate_analytics(
                    win, lines, analyzers, lesson_log, former_lesson_logs
                )
                win.addstr(2, 8 + len(current_str), "")
                time.sleep(0.05)
                key = win.getkey()
                target = text[len(current_str)]
                lesson_log.record_key(key, target)
                win.refresh()
                if key == target:
                    missed = False
                    current_str = current_str + key
                elif key:
                    curses.flash()
                    mistakes[len(current_str)] = True
                    missed = True
                else:
                    pass
                if current_str == text:
                    break
        except:
            aborted = True
        finally:
            curses.endwin()
            return lesson_log if not aborted else None
