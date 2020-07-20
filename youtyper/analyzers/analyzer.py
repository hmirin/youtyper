from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from youtyper.logs import LessonLog


class Analytics(object):
    def __init__(
        self, analyzer_name: str, json_result: Dict[str, Any], printable_result: str,
    ):
        self.analyzer_name = analyzer_name
        self.json_result = json_result
        self.printable_result = printable_result


class Analyzer(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def analyze_lesson(self, lesson_log: LessonLog) -> Analytics:
        pass

    @abstractmethod
    def analyze_multiple_lessons(
        self, lesson_logs: List[LessonLog]
    ) -> Optional[Analytics]:
        pass

    @staticmethod
    @abstractmethod
    def get_analytics_name() -> str:
        return ""


def calculate_all_analytics(
    lesson_log: LessonLog, other_lesson_logs: List[LessonLog], analyzers: List[Analyzer]
) -> Tuple[List[Analytics], List[Analytics]]:
    single_lesson_analytics = []
    multiple_lesson_analytics = []
    for analyzer in analyzers:
        single_lesson_analytics.append(analyzer.analyze_lesson(lesson_log=lesson_log))
        if a := analyzer.analyze_multiple_lessons(
            lesson_logs=other_lesson_logs + [lesson_log]
        ):
            multiple_lesson_analytics.append(a)
    return single_lesson_analytics, multiple_lesson_analytics
