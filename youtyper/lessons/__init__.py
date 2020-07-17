from youtyper.lessons.built_in import (
    PangramLessonGenerator,
    UniversalDeclarationOfHumanRightsLessonGenerator,
    Common6GramLessonGenarator,
)

default_lesson_generator_classes = [
    PangramLessonGenerator,
    UniversalDeclarationOfHumanRightsLessonGenerator,
    Common6GramLessonGenarator,
]

default_lesson_generators = {
    lg.get_generator_name(): lg for lg in default_lesson_generator_classes
}
