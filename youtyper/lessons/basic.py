from random import choices, sample
from typing import Optional

from youtyper.lessons.lessons import LessonGenerator, Lesson

import ast

# https://ja.wikipedia.org/wiki/%E3%83%91%E3%83%B3%E3%82%B0%E3%83%A9%E3%83%A0
pangrams = [
    "Blowzy night-frumps vex'd Jack Q.",
    "Glum Schwartzkopf vex'd by NJ IQ.",
    "New job: fix Mr. Gluck's hazy TV, PDQ!",
    "Frowzy things plumb vex'd Jack Q.",
    "J. Q. Vandz struck my big fox whelp.",
    "Quartz glyph job vex'd cwm finks.",
    "Phlegms fyrd wuz qvint jackbox.",
    "Zing, vext cwm fly jabs Kurd qoph.",
    "Cwm fjord bank glyphs vext quiz.",
    "Jumbling vext frowzy hacks PDQ.",
    "Mr. Jock, TV Quiz Ph.D, bags few lynx.",
    "Junky qoph flags vext crwd zimb.",
    "Cwm fjord veg balks nth pyx quiz.",
    "Oh, wet Alex, a jar, a fag! Up, disk, curve by! Man Oz, Iraq, Arizona, my Bev? Ruck's id-pug, a far Ajax, elate? Who?",
    "How razorback-jumping frogs can level six piqued gymnasts!",
    "Cozy lummox gives smart squid who asks for job pen.",
    "Adjusting quiver and bow, Zompyc killed the fox.",
    "The quick onyx goblin jumps over the lazy dwarf.",
    "My faxed joke won a pager in the cable TV quiz show.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over a lazy dog.",
    "The jay, pig, fox, zebra and my wolves quack!",
    "Pack my box with five dozen liquor jugs.",
    "Few quips galvanized the mock jury box.",
    "Jackdaws love my big sphinx of quartz.",
    "The five boxing wizards jump quickly.",
    "How quickly daft jumping zebras vex.",
    "Bright vixens jump; dozy fowl quack.",
    "Vjump the lazy dogs,quick brown fox.",
    "Quick wafting zephyrs vex bold Jim.",
    "Quick zephyrs blow, vexing daft Jim.",
    "Sphinx of black quartz, judge my vow.",
    "Waltz, bad nymph, for quick jigs vex.",
    "Brick quiz whangs jumpy veldt fox.",
]


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
