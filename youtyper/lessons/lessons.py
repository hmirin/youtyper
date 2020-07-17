from abc import ABCMeta, abstractmethod
from random import shuffle
from typing import List, Optional


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


def text_to_lines(text: str, max_line_length: int = 100) -> List[str]:
    processed_texts = []
    for line in text.split("\n"):
        while len(line) >= max_line_length:
            l = line[:max_line_length]
            processed_texts.append(l)
            line = line[max_line_length:]
        if line:
            processed_texts.append(line)
    return processed_texts


class ListTextLessonGenerator(LessonGenerator):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.texts: List[str] = self.get_texts()
        self.idx = 0

    def __next__(self) -> Optional[Lesson]:
        if self.idx >= len(self.texts):
            return None
        self.idx += 1
        return Lesson(
            text=self.texts[self.idx - 1],
            lesson_id=self.get_generator_name() + "_" + str(self.idx),
            lesson_name=self.get_generator_name(),
        )

    def __len__(self):
        return len(self.texts)

    @staticmethod
    @abstractmethod
    def get_generator_name() -> str:
        return ""

    @staticmethod
    @abstractmethod
    def get_texts() -> List[str]:
        return [""]


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
        self.texts = text_to_lines(text, len_lessons)
        if _shuffle:
            shuffle(self.texts)
        if num_lessons:
            self.texts = self.texts[:num_lessons]
        self.idx = 0

    def __next__(self) -> Optional[Lesson]:
        if self.idx >= len(self.texts):
            return None
        self.idx += 1
        return Lesson(
            text=self.texts[self.idx - 1],
            lesson_id=self.get_generator_name() + "_" + str(self.idx),
            lesson_name=self.get_generator_name(),
        )

    def __len__(self):
        return len(self.texts)

    @staticmethod
    def get_generator_name() -> str:
        return "text"
