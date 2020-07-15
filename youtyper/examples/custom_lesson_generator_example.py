from argparse import ArgumentParser
from typing import Tuple

from youtyper.lessons.lessons import LessonGenerator, Lesson


class ExampleGenerator(LessonGenerator):
    def __init__(self, custom_args: Tuple[str]):
        # Arguments are passed through custom_args variable as list of string
        # Example:
        # $ youtype --unknown-arg1 a b c --lesson_type python --unknown_arg2 --custom_lesson_generator...
        # custom_args =  ('--unknown-arg1', 'a', 'b', 'c', '--unknown_arg2')
        # You may want to use argparse to parse these arguments
        super().__init__()
        parser = ArgumentParser()
        parser.add_argument("--text")
        parsed_args, unknown_args = parser.parse_known_args(custom_args)
        print(parsed_args, unknown_args)
        self.text = parsed_args.text
        if self.text is None:
            raise ValueError(
                "You must add --text option: --text [the text you want to type]"
            )
        self.c = 0

    def __len__(self):
        return 1

    def __next__(self):
        if self.c == 0:
            self.c += 1
            # This lesson echoes the input of --text option
            return Lesson(self.text, str(self.c), self.get_generator_name())
        else:
            return None

    @staticmethod
    def get_generator_name() -> str:
        return "example_generator"
