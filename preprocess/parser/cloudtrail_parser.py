from .base_parser import BaseParser

class CloudTrailParser(BaseParser):

    def parse(self, raw_log: dict) -> dict:
        return {
            "timestamp": raw_log.get("eventTime"),
            "user": raw_log.get("userIdentity", {}).get("userName"),
            "source_ip": raw_log.get("sourceIPAddress"),
            "dest_ip": None,
            "host": raw_log.get("awsRegion"),
            "process": raw_log.get("eventSource"),
            "event_type": raw_log.get("eventName"),
            "message": raw_log.get("requestParameters"),
            "raw": raw_log
        }
