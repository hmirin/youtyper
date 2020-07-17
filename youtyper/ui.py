import curses
import time
from typing import Optional

from .lessons.lessons import Lesson
from .logs import LessonLog


class UI(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def start(lesson: Lesson) -> Optional[LessonLog]:
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
            curses.noecho()
            missed = False
            key = ""
            target = ""
            while True:
                win.clear()
                if missed:
                    win.addstr(0, 0, "miss! " + key + "->" + target)
                win.addstr(1, 0, "Lesson: ")
                win.addstr(2, 0, "You:    ")
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
                win.attron(curses.color_pair(1))
                win.addstr(1, 8 + len(current_str), text[len(current_str)])
                win.attroff(curses.color_pair(1))
                win.attroff(curses.A_BOLD)
                win.addstr(2, 8, current_str)
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
