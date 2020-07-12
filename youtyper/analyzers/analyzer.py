from abc import ABCMeta, abstractmethod
from typing import List, Dict

from youtyper.logs import LessonLog


class Analyzer(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def analyze(self, lesson_log: LessonLog) -> (Dict, str):
        pass

    @staticmethod
    @abstractmethod
    def get_analytics_name() -> str:
        return ""
