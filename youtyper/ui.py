import curses, time
from typing import Optional

from .lessons.lessons import Lesson
from .logs import LessonLog


class UI(object):
    def __init__(self) -> None:
        pass

    def start(self, lesson: Lesson) -> Optional[LessonLog]:
        text = lesson.text
        lesson_log = LessonLog()
        current_str = ""
        aborted = False
        try:
            win = curses.initscr()
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
