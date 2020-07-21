import curses
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import click

from youtyper.analyzers import default_analyzers
from youtyper.analyzers.analyzer import load_custom_analyzer
from youtyper.lessons import default_lesson_generators
from youtyper.lessons.lessons import Lesson, LessonGenerator, TextLessonGenerator

from .ui import LessonWindow, show_and_calculate_analytics


def select_lesson_generator(
    lesson_type: str,
    lesson_name: str,
    text_path: str,
    num_lessons: int,
    len_lessons: int,
    disable_shuffle: bool,
    custom_lesson_generator,
    custom_args,
) -> LessonGenerator:
    # Create LessonGenerator
    if lesson_type == "built-in":
        lesson_generator = default_lesson_generators[lesson_name]()
    elif lesson_type == "text":
        if not text_path:
            raise ValueError("You must specify text_path to generate lessons.")
        if not os.path.exists(text_path):
            raise FileNotFoundError("You must specify valid text_path.")
        try:
            text = open(text_path, encoding="ascii").read()
        except UnicodeDecodeError as e:
            print(e.__traceback__)
            raise ValueError("Only accepts ascii file for text_path")
        filename = os.path.splitext(text_path)[0]
        lesson_generator = TextLessonGenerator(
            text, filename, num_lessons, len_lessons, not disable_shuffle
        )
    elif lesson_type == "python":
        f = open(custom_lesson_generator[0])
        code = f.read()
        exec(code, globals())
        custom_lesson_generator_class = globals()[custom_lesson_generator[1]]
        lesson_generator = custom_lesson_generator_class(custom_args)
    else:
        raise
    return lesson_generator


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option(
    "--lesson_type",
    "-t",
    default="built-in",
    type=click.Choice(["built-in", "text", "python"], case_sensitive=False),
    help="How the lesson is generated",
)
@click.option(
    "--lesson_name",
    "-ln",
    default="default_lesson",
    type=click.Choice(default_lesson_generators.keys(), case_sensitive=True),
    help="Choose built-in lesson to use",
)
@click.option(
    "--text_path",
    "-t",
    default="",
    type=str,
    help='Text file path to load into lessons.  Available if lesson_type="text"',
)
@click.option(
    "--disable_shuffle",
    "-ds",
    is_flag=True,
    help='Disable shuffling of lessons. Available if lesson_type="text"',
)
@click.option(
    "--num_lessons",
    "-n",
    default=0,
    type=int,
    help='Number of lessons. default: "0": never quit until all lessons are finished. Available if lesson_type="text"',
)
@click.option(
    "--len_lessons",
    "-l",
    default="100",
    type=int,
    help='Number of maximum characters of each lesson. Available if lesson_type="text"',
)
@click.option(
    "--analyzer",
    "-a",
    default=["cpm", "error_rate", "missed_key_ranking"],
    type=click.Choice(default_analyzers.keys(), case_sensitive=True),
    multiple=True,
    help="Analytics to be shown at the end of the lesson",
)
@click.option(
    "--ignore_consecutive_errors",
    "-i",
    is_flag=True,
    help="Ignore consecutive errors on calculating analytics",
)
@click.option(
    "--custom_analyzer",
    "-ca",
    type=(str, str),
    multiple=True,
    help="Custom analyzer path and class name",
)
@click.option(
    "--custom_lesson_generator",
    "-cl",
    type=(str, str),
    default=(None, None),
    help='Custom lesson generator path and class name. Available if lesson_type="python"',
)
@click.argument("custom_args", nargs=-1, type=click.UNPROCESSED)
def main(
    lesson_type: str,
    lesson_name: str,
    text_path: str,
    disable_shuffle: bool,
    num_lessons: Optional[int],
    len_lessons: int,
    analyzer: List[str],
    ignore_consecutive_errors: bool,
    custom_analyzer: List[Tuple[str, str]],
    custom_lesson_generator: Tuple[str, str],
    custom_args,
):
    if custom_lesson_generator[0] is None and custom_lesson_generator[1] is None:
        custom_lesson_generator = []

    lesson_generator = select_lesson_generator(
        lesson_type,
        lesson_name,
        text_path,
        num_lessons,
        len_lessons,
        disable_shuffle,
        custom_lesson_generator,
        custom_args,
    )

    # Create Analyzer
    analyzers = [default_analyzers[name]() for name in analyzer]
    analyzers += [
        load_custom_analyzer(analyzer_path, analyzer_classname, custom_args)
        for analyzer_path, analyzer_classname in custom_analyzer
    ]

    try:
        p = LessonWindow()
        lesson_logs = []
        logs = []
        current_lesson = 1
        win = curses.initscr()
        curses.noecho()
        win.clear()
        win.refresh()
        message = (
            f"press enter to start lesson {current_lesson} / {len(lesson_generator)}"
        )
        win.addstr(0, 0, message)
        _ = win.getkey()
        while lesson := next(lesson_generator):
            start_time = datetime.now()
            lesson_log = p.start(lesson, analyzers, lesson_logs)
            if lesson_log is None:
                print("\nAborted!")
                raise SystemExit()
            lesson_logs.append(lesson_log)
            win.clear()
            win.refresh()
            message = f"lesson {current_lesson} / {len(lesson_generator)} result:"
            win.addstr(0, 0, message)
            (current_lesson_analytics, _,) = show_and_calculate_analytics(
                win, 3, analyzers, lesson_log, lesson_logs
            )
            log = {
                "lesson_name": lesson.lesson_name,
                "lesson_id": lesson.lesson_id,
                "command-line-options": {
                    "lesson_type": lesson_type,
                    "lesson_name": lesson_name,
                    "text_path": text_path,
                    "disable_shuffle": disable_shuffle,
                    "num_lessons": num_lessons,
                    "len_lessons": len_lessons,
                    "analyzer": analyzer,
                    "ignore_consecutive_errors": ignore_consecutive_errors,
                    "custom_analyzer": custom_analyzer,
                    "custom_lesson_generator": custom_lesson_generator,
                    "custom_args": custom_args,
                },
                "text": lesson.text,
                "events": [e.to_dict() for e in lesson_log.events],
                "analytics": {
                    a.analyzer_name: a.json_result for a in current_lesson_analytics
                },
            }
            logs.append(log)
            abs_dir = str(Path.home()) + "/.youtyper/"
            os.makedirs(abs_dir, exist_ok=True)
            with open(
                f"{abs_dir}/{start_time:%Y%m%d_%H%M%S}_{lesson.lesson_name}_{lesson.lesson_id}.json",
                "w",
            ) as f:
                f.write(json.dumps(log))
            current_lesson += 1
            if current_lesson <= len(lesson_generator):
                message = f"press enter to start lesson {current_lesson} / {len(lesson_generator)}"
            else:
                message = f"press enter to finish lesson. well done!"
            curses.curs_set(1)
            win.addstr(1, 0, message)
            _ = win.getkey()
    finally:
        curses.endwin()


if __name__ == "__main__":
    main()
