from abc import ABCMeta, abstractmethod
from typing import Optional
from random import shuffle


class Lesson(object):
    def __init__(self, text: str, lesson_id: str, lesson_name: str) -> None:
        self.text = text
        self.lesson_id = lesson_id
        self.lesson_name = lesson_name


class LessonGenerator(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __next__(self) -> Optional[Lesson]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    def __iter__(self):
        return self

    @staticmethod
    @abstractmethod
    def get_generator_name() -> str:
        return ""


class TextLessonGenerator(LessonGenerator):
    def __init__(
        self,
        lesson_name: str,
        text: str,
        num_lessons: int = 0,
        len_lessons: int = 100,
        _shuffle: bool = True,
    ):
        super().__init__()
        self.lesson_name = lesson_name
        self.text = [
            line.strip()[:len_lessons] for line in text.split("\n") if line.strip()
        ]
        if _shuffle:
            shuffle(self.text)
        if not num_lessons:
            self.n = len(self.text)
        else:
            self.n = min(len(self.text), num_lessons)
        self.c = 0

    def __next__(self) -> Optional[Lesson]:
        if self.n and self.c >= self.n:
            return None
        self.c += 1
        return Lesson(
            text=self.text[self.c],
            lesson_id=self.lesson_name + "_" + str(self.c),
            lesson_name=self.lesson_name,
        )

    def __len__(self):
        return self.n

    @staticmethod
    def get_generator_name() -> str:
        return "text"
