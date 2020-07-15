from youtyper.lessons.basic import (
    PangramLessonGenerator,
    UniversalDeclarationOfHumanRightsLessonGenerator,
)

default_lesson_generator_classes = [
    PangramLessonGenerator,
    UniversalDeclarationOfHumanRightsLessonGenerator,
]

default_lesson_generators = {
    lg.get_generator_name(): lg for lg in default_lesson_generator_classes
}
