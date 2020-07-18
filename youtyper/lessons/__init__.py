from youtyper.lessons.built_in import (
    Common6GramLessonGenerator,
    PangramLessonGenerator,
    UniversalDeclarationOfHumanRightsLessonGenerator,
)

default_lesson_generator_classes = [
    PangramLessonGenerator,
    UniversalDeclarationOfHumanRightsLessonGenerator,
    Common6GramLessonGenerator,
]

default_lesson_generators = {
    lg.get_generator_name(): lg for lg in default_lesson_generator_classes
}
