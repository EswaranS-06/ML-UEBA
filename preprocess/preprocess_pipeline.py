import pandas as pd
from preprocess.parser.parser_registry import ParserRegistry
from preprocess.normalizer.normalizer import Normalizer

class PreprocessPipeline:

    def __init__(self):
        self.registry = ParserRegistry()
        self.normalizer = Normalizer()

    def run(self, raw_logs: list) -> pd.DataFrame:
        records = []

        for raw in raw_logs:
            parser_type = self.registry.detect_type(raw)
            parser = self.registry.get_parser(parser_type)

            parsed = parser.parse(raw)
            normalized = self.normalizer.normalize(parsed)

            records.append(normalized)

        return pd.DataFrame(records)
