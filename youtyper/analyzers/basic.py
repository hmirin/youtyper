from abc import abstractmethod
from collections import defaultdict
from datetime import timedelta
from typing import List, Dict, Optional

from youtyper.analyzers.analyzer import Analyzer

from youtyper.logs import KeyStrokeLog, LessonLog


class BuiltInAnalyzer(Analyzer):
    @staticmethod
    @abstractmethod
    def get_abbreviated_name() -> str:
        return ""


def time_to_push_correct_key(events: List[KeyStrokeLog]):
    last_time = None
    accumulated_time = timedelta()
    elasped_time_dict: Dict[str, List[timedelta]] = defaultdict(list)
    for key_stroke_log in events:
        if last_time is None:
            last_time = key_stroke_log.timestamp
        else:
            current_time = key_stroke_log.timestamp
            elasped_time = current_time - last_time
            if key_stroke_log.target == key_stroke_log.key:
                elasped_time_dict[key_stroke_log.target].append(
                    elasped_time + accumulated_time
                )
                accumulated_time = timedelta()
            else:
                accumulated_time += elasped_time
    return elasped_time_dict


def elasped_seconds_and_num_keys(
    lesson_log: LessonLog, key: str = None, tail: Optional[int] = None
) -> (int, timedelta):
    if tail is not None:
        events = lesson_log.events[-tail:]
    else:
        events = lesson_log.events
    if key is None:
        first_stroke_time = events[0].timestamp
        last_stroke_time = events[-1].timestamp
        return (len(events) - 1), last_stroke_time - first_stroke_time
    else:
        seconds = [t.total_seconds() for t in time_to_push_correct_key(events)[key]]
        return len(seconds), timedelta(seconds=sum(seconds))


class CharacterPerMinuteAnalyzer(BuiltInAnalyzer):
    def __init__(self):
        super().__init__()

    def analyze(self, lesson_log: LessonLog) -> (Dict, str):
        num_keys, elasped_time = elasped_seconds_and_num_keys(lesson_log)
        seconds = elasped_time.total_seconds()
        cpm = num_keys / (seconds / 60)
        return (
            {"cpm": cpm, "len_lesson": num_keys, "total_time_in_seconds": seconds},
            f"cpm: {cpm:.1f} (elasped seconds: {elasped_time}, len_lesson: {num_keys})",
        )

    @staticmethod
    def get_analytics_name() -> str:
        return "Character Per Minute (CPM)"

    @staticmethod
    def get_abbreviated_name() -> str:
        return "cpm"


class ErrorRateAnalyzer(BuiltInAnalyzer):
    def __init__(self):
        super().__init__()

    def analyze(self, lesson_log: LessonLog) -> (Dict, str):
        events = lesson_log.events
        wrong_events = [e for e in events if e.target != e.key]
        error_rate = len(wrong_events) / len(events)
        return (
            {
                "error_rate": error_rate,
                "total_push": len(events),
                "wrong_push": len(wrong_events),
            },
            f"error_rate: {error_rate*100:.1f}% (wrong push: {len(wrong_events)}, total push: {len(events)})",
        )

    @staticmethod
    def get_analytics_name() -> str:
        return "Error Rate"

    @staticmethod
    def get_abbreviated_name() -> str:
        return "error_rate"
