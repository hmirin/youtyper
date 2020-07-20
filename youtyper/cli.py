from __future__ import annotations

import os
from typing import TYPE_CHECKING, List, Optional, Tuple

from youtyper.analyzers import default_analyzers
from youtyper.lessons import default_lesson_generators

if TYPE_CHECKING:
    from youtyper.lessons.lessons import LessonGenerator, TextLessonGenerator


class CLIOptions(object):
    def __init__(
        self,
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
    ) -> None:
        self.lesson_type = lesson_type
        self.lesson_name = lesson_name
        self.text_path = text_path
        self.disable_shuffle = disable_shuffle
        self.num_lessons = num_lessons
        self.len_lessons = len_lessons
        self.analyzer = analyzer
        self.ignore_consecutive_errors = ignore_consecutive_errors
        self.custom_analyzer = custom_analyzer
        self.custom_lesson_generator = custom_lesson_generator
        self.custom_args = custom_args

        if custom_lesson_generator[0] is None and custom_lesson_generator[1] is None:
            custom_lesson_generator = []
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
            lesson_generator: LessonGenerator = custom_lesson_generator_class(
                custom_args
            )
        else:
            raise Exception("No such lesson_type available: " + str(lesson_type))

        # Create Analyzer
        analyzers = [default_analyzers[name]() for name in analyzer]

        for analyzer_path, analyzer_classname in custom_analyzer:
            f = open(analyzer_path[0])
            code = f.read()
            exec(code, globals())
            custom_analyzer_class = globals()[analyzer_classname]
            custom_analyzer = custom_analyzer_class(custom_args)
            analyzers.append(custom_analyzer)

        self.lesson_generator = lesson_generator
        self.analyzers = analyzers
