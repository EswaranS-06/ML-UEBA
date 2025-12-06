class BaseParser:
    """
    Every parser must inherit this class
    and implement parse(raw_log) → dict
    """

    def parse(self, raw_log: str) -> dict:
        raise NotImplementedError("Parser must implement parse()")
