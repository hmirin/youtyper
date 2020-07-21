from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from youtyper.analyzers.analyzer import Analytics
    from youtyper.cli import CLIOptions
    from youtyper.lessons.lessons import Lesson


class KeyStrokeLog(object):
    def __init__(self, timestamp: datetime, key: str, target: str):
        self.timestamp = timestamp
        self.key = key
        self.target = target

    def to_dict(self):
        return {
            "timestamp": str(self.timestamp),
            "key": self.key,
            "target": self.target,
        }


class LessonLog(object):
    def __init__(self) -> None:
        self.events: List[KeyStrokeLog] = []

    def record_key(self, key: str, target: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.events.append(KeyStrokeLog(timestamp, key, target))


def save_to_log(
    lesson: Lesson,
    lesson_log: LessonLog,
    current_lesson_analytics: List[Analytics],
    option: CLIOptions,
):
    return {
        "lesson_name": lesson.lesson_name,
        "lesson_id": lesson.lesson_id,
        "command-line-options": {
            "lesson_type": option.lesson_type,
            "lesson_name": option.lesson_name,
            "text_path": option.text_path,
            "disable_shuffle": option.disable_shuffle,
            "num_lessons": option.num_lessons,
            "len_lessons": option.len_lessons,
            "analyzer": option.analyzer,
            "ignore_consecutive_errors": option.ignore_consecutive_errors,
            "custom_analyzer": option.custom_analyzer,
            "custom_lesson_generator": option.custom_lesson_generator,
            "custom_args": option.custom_args,
        },
        "text": lesson.text,
        "events": [e.to_dict() for e in lesson_log.events],
        "analytics": {a.analyzer_name: a.json_result for a in current_lesson_analytics},
    }
