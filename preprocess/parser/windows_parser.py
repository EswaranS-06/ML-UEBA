from .base_parser import BaseParser

class WindowsParser(BaseParser):
    def parse(self, raw_log: dict) -> dict:
        """
        Windows logs typically come as JSON or XML.
        Assume parsed JSON input.
        """

        return {
            "timestamp": raw_log.get("TimeCreated"),
            "user": raw_log.get("User"),
            "src_ip": raw_log.get("IpAddress"),
            "dest_ip": None,
            "host": raw_log.get("ComputerName"),
            "process": raw_log.get("ProcessName"),
            "event_type": raw_log.get("EventID"),
            "message": raw_log.get("Message"),
            "raw": raw_log
        }
