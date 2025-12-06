import re
import yaml
import os

from .syslog_parser import SyslogParser
from .windows_parser import WindowsParser
from .cloudtrail_parser import CloudTrailParser
from .network_parser import NetworkParser


class ParserRegistry:

    def __init__(self, config_path=None):
        # Default config path
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                "../../config/parser_config.yml"
            )

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Registry of available parser classes
        self.available_parsers = {
            "syslog": SyslogParser(),
            "windows": WindowsParser(),
            "cloudtrail": CloudTrailParser(),
            "network": NetworkParser(),
        }

    def detect_type(self, raw_log):
        """
        Dynamic & configurable log-type detection.
        Supports:
          - text triggers
          - regex triggers
          - dict key triggers
        """

        for parser_name, parser_info in self.config["parsers"].items():
            triggers = parser_info.get("triggers", [])

            for rule in triggers:
                rtype = rule.get("type")

                # Case 1: Rule works only when log is text/string
                if rtype == "text" and isinstance(raw_log, str):
                    substrings = rule.get("contains", [])
                    if any(s in raw_log for s in substrings):
                        return parser_name

                # Case 2: Regex rule on string logs
                if rtype == "regex" and isinstance(raw_log, str):
                    pattern = rule.get("pattern")
                    if re.search(pattern, raw_log):
                        return parser_name

                # Case 3: Dict key presence rule
                if rtype == "dict_keys" and isinstance(raw_log, dict):
                    keys = rule.get("keys", [])
                    if all(k in raw_log for k in keys):
                        return parser_name

        # Fallback parser from config
        return self.config.get("default_parser", "syslog")

    def get_parser(self, parser_type):
        return self.available_parsers.get(parser_type)
