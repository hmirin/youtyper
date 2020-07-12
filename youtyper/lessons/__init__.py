from youtyper.lessons.basic import PangramLessonGenerator

default_lesson_generator_classes = [PangramLessonGenerator]

default_lesson_generators = {
    lg.get_generator_name(): lg for lg in default_lesson_generator_classes
}
