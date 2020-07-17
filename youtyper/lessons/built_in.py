from random import sample
from typing import List

from youtyper.assets.famous_texts import (
    universal_declaration_of_human_rights_text,
    pangrams_text,
    common_english_6_grams,
)
from youtyper.lessons.lessons import (
    ListTextLessonGenerator,
    text_to_lines,
)


class PangramLessonGenerator(ListTextLessonGenerator):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_generator_name() -> str:
        return "pangram"

    @staticmethod
    def get_texts() -> List[str]:
        pangrams = pangrams_text.strip().split("\n")
        return sample(pangrams, len(pangrams))


class UniversalDeclarationOfHumanRightsLessonGenerator(ListTextLessonGenerator):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_generator_name() -> str:
        return "universal_declaration_of_human_rights"

    @staticmethod
    def get_texts() -> List[str]:
        return text_to_lines(universal_declaration_of_human_rights_text)


class Common6GramLessonGenarator(ListTextLessonGenerator):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_generator_name() -> str:
        return "default_lesson"

    @staticmethod
    def get_texts() -> List[str]:
        texts = text_to_lines(common_english_6_grams)
        return sample(texts, len(texts))
