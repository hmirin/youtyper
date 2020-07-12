from datetime import datetime
from typing import List


class KeyStrokeLog(object):
    def __init__(self, timestamp: datetime, key: str, target: str):
        self.timestamp = timestamp
        self.key = key
        self.target = target

    def to_dict(self):
        return {
            "timestamp": str(self.timestamp),
            "key": self.key,
            "targert": self.target,
        }


class LessonLog(object):
    def __init__(self) -> None:
        self.events: List[KeyStrokeLog] = []

    def record_key(self, key: str, target: str, timestamp: datetime = None):
        if timestamp is None:
            timestamp = datetime.now()
        self.events.append(KeyStrokeLog(timestamp, key, target))
