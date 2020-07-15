from abc import abstractmethod
from random import choices, sample
from typing import Optional

from youtyper.assets.famous_texts import (
    universal_declaration_of_human_rights_text,
    pangrams,
)
from youtyper.lessons.lessons import LessonGenerator, Lesson, TextLessonGenerator


class PangramLessonGenerator(LessonGenerator):
    def __init__(self):
        super().__init__()
        self.n = len(pangrams)
        self.c = 0
        self.pangrams = sample(pangrams, len(pangrams))

    def __next__(self) -> Optional[Lesson]:
        if self.c >= self.n:
            return None
        self.c += 1
        return Lesson(
            text=pangrams[self.c],
            lesson_id=self.get_generator_name() + "_" + str(self.c),
            lesson_name=self.get_generator_name(),
        )

    def __len__(self):
        return self.n

    @staticmethod
    def get_generator_name() -> str:
        return "default_lesson"


class FamousTextsLessonGenerator(TextLessonGenerator):
    def __init__(self):
        super().__init__(self.get_generator_name(), self.get_text(), _shuffle=False)

    def __next__(self) -> Optional[Lesson]:
        if self.c >= self.n:
            return None
        self.c += 1
        return Lesson(
            text=self.text[self.c],
            lesson_id=self.get_generator_name() + "_" + str(self.c),
            lesson_name=self.get_generator_name(),
        )

    def __len__(self):
        return self.n

    @staticmethod
    @abstractmethod
    def get_generator_name() -> str:
        return ""

    @staticmethod
    @abstractmethod
    def get_text() -> str:
        return ""


class UniversalDeclarationOfHumanRightsLessonGenerator(FamousTextsLessonGenerator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_generator_name() -> str:
        return "Universal_Declaration_Of_Human_Rights"

    @staticmethod
    def get_text() -> str:
        return universal_declaration_of_human_rights_text
