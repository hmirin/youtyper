from abc import abstractmethod
from collections import defaultdict
from datetime import timedelta
from typing import Dict, List, Optional

import numpy as np

from youtyper.analyzers.analyzer import Analytics, Analyzer
from youtyper.logs import KeyStrokeLog, LessonLog


class BuiltInAnalyzer(Analyzer):
    @staticmethod
    @abstractmethod
    def get_abbreviated_name() -> str:
        return ""


def time_to_push_correct_key(events: List[KeyStrokeLog]):
    last_time = None
    accumulated_time = timedelta()
    elapsed_time_dict: Dict[str, List[timedelta]] = defaultdict(list)
    for key_stroke_log in events:
        if last_time is None:
            last_time = key_stroke_log.timestamp
        else:
            current_time = key_stroke_log.timestamp
            elapsed_time = current_time - last_time
            if key_stroke_log.target == key_stroke_log.key:
                elapsed_time_dict[key_stroke_log.target].append(
                    elapsed_time + accumulated_time
                )
                accumulated_time = timedelta()
            else:
                accumulated_time += elapsed_time
    return elapsed_time_dict


def elapsed_seconds_and_num_keys(
    lesson_log: LessonLog, key: str = None, tail: Optional[int] = None
) -> (int, timedelta):
    if tail is not None:
        events = lesson_log.events[-tail:]
    else:
        events = lesson_log.events
    if len(events) == 0:
        return 0, timedelta()
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

    def analyze_lesson(self, lesson_log: LessonLog) -> Analytics:
        num_keys, elapsed_time = elapsed_seconds_and_num_keys(lesson_log)
        seconds = elapsed_time.total_seconds()
        if seconds > 0:
            cpm = num_keys / (seconds / 60)
        else:
            cpm = 0
        return Analytics(
            self.get_analytics_name(),
            {"cpm": cpm, "len_lesson": num_keys, "total_time_in_seconds": seconds},
            f"cpm:\t\t{cpm:.1f}\t(elapsed seconds: {seconds:.1f}, len_lesson: {num_keys})",
        )

    def analyze_multiple_lessons(self, lesson_logs: List[LessonLog]) -> Analytics:
        num_keys = 0
        seconds = 0
        for lesson_log in lesson_logs:
            single_lesson_analytics = self.analyze_lesson(lesson_log)
            num_keys += single_lesson_analytics.json_result["len_lesson"]
            seconds += single_lesson_analytics.json_result["total_time_in_seconds"]
        if seconds > 0:
            cpm = num_keys / (seconds / 60)
        else:
            cpm = 0
        return Analytics(
            self.get_analytics_name(),
            {"cpm": cpm, "len_lesson": num_keys, "total_time_in_seconds": seconds},
            f"cpm:\t\t{cpm:.1f}\t(elapsed seconds: {seconds:.1f}, len_lesson: {num_keys})",
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

    def analyze_lesson(self, lesson_log: LessonLog) -> Analytics:
        events = lesson_log.events
        wrong_events = [e for e in events if e.target != e.key]
        if events:
            error_rate = len(wrong_events) / len(events)
        else:
            error_rate = 0.0
        return Analytics(
            self.get_analytics_name(),
            {
                "error_rate": error_rate,
                "total_push": len(events),
                "wrong_push": len(wrong_events),
            },
            f"error_rate:\t{error_rate*100:.1f}%\t(wrong push: {len(wrong_events)}, total push: {len(events)})",
        )

    def analyze_multiple_lessons(self, lesson_logs: List[LessonLog]) -> Analytics:
        len_events = 0
        len_wrong_events = 0
        for lesson_log in lesson_logs:
            single_lesson_analytics = self.analyze_lesson(lesson_log)
            len_events += single_lesson_analytics.json_result["total_push"]
            len_wrong_events += single_lesson_analytics.json_result["wrong_push"]
        if len_events > 0:
            error_rate = len_wrong_events / len_events
        else:
            error_rate = 0
        return Analytics(
            self.get_analytics_name(),
            {
                "error_rate": error_rate,
                "total_push": len_events,
                "wrong_push": len_wrong_events,
            },
            f"error_rate:\t{error_rate*100:.1f}%\t(wrong push: {len_wrong_events}, total push: {len_events})",
        )

    @staticmethod
    def get_analytics_name() -> str:
        return "Error Rate"

    @staticmethod
    def get_abbreviated_name() -> str:
        return "error_rate"


class MissedKeyRanking(BuiltInAnalyzer):
    def __init__(self):
        super().__init__()

    def analyze_lesson(self, lesson_log: LessonLog) -> Analytics:
        events = lesson_log.events
        keys = sorted(list(set([e.target for e in events] + [e.key for e in events])))
        key2idx = {key: idx for idx, key in enumerate(keys)}
        matrix = np.zeros([len(keys), len(keys)])
        for e in events:
            if e.target == e.key:
                continue
            matrix[key2idx[e.target], key2idx[e.key]] += 1
        prob_matrix = matrix / np.sum(matrix)
        flatten_matrix = np.ravel(prob_matrix)
        n = 5
        top_n = -np.sort(-flatten_matrix)[:n]
        keys_to_show = []
        for prob in top_n:
            xs, ys = np.where(prob_matrix == prob)
            for x, y in zip(xs, ys):
                keys_to_show.append((keys[x], keys[y], prob_matrix[x, y]))
        text = "confused key:\t"
        for key, target, prob in keys_to_show[:n]:
            if prob == 0:
                continue
            text += f"{key}->{target} {prob*100:.0f}% "

        return Analytics(self.get_analytics_name(), {"top_errors": keys_to_show}, text,)

    def analyze_multiple_lessons(self, lesson_logs: List[LessonLog]) -> Analytics:
        events = []
        for l in lesson_logs:
            events = events + l.events
        keys = sorted(list(set([e.target for e in events] + [e.key for e in events])))
        key2idx = {key: idx for idx, key in enumerate(keys)}
        matrix = np.zeros([len(keys), len(keys)])
        for e in events:
            if e.target == e.key:
                continue
            matrix[key2idx[e.target], key2idx[e.key]] += 1
        prob_matrix = matrix / np.sum(matrix)
        flatten_matrix = np.ravel(prob_matrix)
        n = 5
        top_n = -np.sort(-flatten_matrix)[:n]
        keys_to_show = []
        for prob in top_n:
            xs, ys = np.where(prob_matrix == prob)
            for x, y in zip(xs, ys):
                keys_to_show.append((keys[x], keys[y], prob_matrix[x, y]))
        text = "confused key:\t"
        for key, target, prob in keys_to_show[:n]:
            if prob == 0:
                continue
            text += f"{key}->{target} {prob*100:.0f}% "

        return Analytics(self.get_analytics_name(), {"top_errors": keys_to_show}, text,)

    @staticmethod
    def get_analytics_name() -> str:
        return "Missed Key Ranking"

    @staticmethod
    def get_abbreviated_name() -> str:
        return "missed_key_ranking"
