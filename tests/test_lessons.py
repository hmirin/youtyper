from importlib.resources import read_text
from unittest import TestCase

from nose.tools import eq_, ok_

from youtyper.lessons.lessons import TextLessonGenerator, text_to_lines


class LessonUtilityTestCase(TestCase):
    @staticmethod
    def test_text_to_lines():
        text = "a" * 200
        eq_(len(text_to_lines(text)), 2)
        text = "a" * 10
        eq_(len(text_to_lines(text)), 1)
        text = ""
        eq_(len(text_to_lines(text)), 0)


class TextLessonTestCase(TestCase):
    @staticmethod
    def text_lesson_test_case():
        text = read_text("youtyper.assets", "universal_declaration_of_human_rights.txt")
        num_lessons = 10
        len_lessons = 30
        g = TextLessonGenerator(
            "test",
            text,
            num_lessons=num_lessons,
            len_lessons=len_lessons,
            _shuffle=True,
        )
        n = 0
        while next(g):
            n += 1
        eq_(n, num_lessons, "TextLessonGenerator should respect num_lessons")
        g = TextLessonGenerator(
            "test",
            text,
            num_lessons=num_lessons,
            len_lessons=len_lessons,
            _shuffle=True,
        )
        l = next(g)
        while l:
            print(l.text)
            ok_(
                0 < len(l.text) <= len_lessons,
                "TextLessonGenerator should respect len_lessons",
            )
            l = next(g)
        g1 = TextLessonGenerator(
            "test",
            text,
            num_lessons=num_lessons,
            len_lessons=len_lessons,
            _shuffle=True,
        )
        g2 = TextLessonGenerator(
            "test",
            text,
            num_lessons=num_lessons,
            len_lessons=len_lessons,
            _shuffle=True,
        )
        l1 = next(g1)
        l2 = next(g2)
        all_same = True
        while l1 or l2:
            if l1.text != l2.text:
                all_same = False
            l1 = next(g1)
            l2 = next(g2)
        ok_(not all_same, "TextLessonGenerator should respect _shuffle")
        g1 = TextLessonGenerator(
            "test",
            text,
            num_lessons=num_lessons,
            len_lessons=len_lessons,
            _shuffle=False,
        )
        g2 = TextLessonGenerator(
            "test",
            text,
            num_lessons=num_lessons,
            len_lessons=len_lessons,
            _shuffle=False,
        )
        l1 = next(g1)
        l2 = next(g2)
        while l1 or l2:
            ok_(l1.text == l2.text, "TextLessonGenerator should respect _shuffle")
            l1 = next(g1)
            l2 = next(g2)
