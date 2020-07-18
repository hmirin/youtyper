from typing import Callable, Dict

from youtyper.analyzers.built_in import (
    BuiltInAnalyzer,
    CharacterPerMinuteAnalyzer,
    ErrorRateAnalyzer,
)

default_analyzer_classes = [CharacterPerMinuteAnalyzer, ErrorRateAnalyzer]

default_analyzers: Dict[str, Callable] = {
    a.get_abbreviated_name(): a for a in default_analyzer_classes
}
