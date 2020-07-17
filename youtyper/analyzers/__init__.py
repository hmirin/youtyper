from typing import Dict

from youtyper.analyzers.built_in import (
    CharacterPerMinuteAnalyzer,
    BuiltInAnalyzer,
    ErrorRateAnalyzer,
)

default_analyzer_classes = [CharacterPerMinuteAnalyzer, ErrorRateAnalyzer]

default_analyzers: Dict[str, BuiltInAnalyzer] = {
    a.get_abbreviated_name(): a for a in default_analyzer_classes
}
