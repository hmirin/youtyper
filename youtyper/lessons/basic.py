from abc import abstractmethod
from random import choices, sample
from typing import List, Optional

from youtyper.assets.famous_texts import (
    universal_declaration_of_human_rights_text,
    pangrams,
)
from youtyper.lessons.lessons import (
    LessonGenerator,
    Lesson,
    ListTextLessonGenerator,
    TextLessonGenerator,
    text_to_lines,
)


class PangramLessonGenerator(ListTextLessonGenerator):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_generator_name() -> str:
        return "default_lesson"

    @staticmethod
    def get_texts() -> List[str]:
        return sample(pangrams, len(pangrams))


class UniversalDeclarationOfHumanRightsLessonGenerator(ListTextLessonGenerator):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_generator_name() -> str:
        return "Universal_Declaration_Of_Human_Rights"

    @staticmethod
    def get_texts() -> List[str]:
        return text_to_lines(universal_declaration_of_human_rights_text)
