import re
from .base_parser import BaseParser

class SyslogParser(BaseParser):
    # Nov 30 08:17:01 ip-172-31-27-153 CRON[22172]: pam_unix(cron:session): session closed for user root
    SYSLOG_REGEX = re.compile(
        r"(?P<timestamp>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\S+)\s+(?P<process>\S+):\s+(?P<message>.*)"
    )

    def parse(self, raw_log: str) -> dict:
        match = self.SYSLOG_REGEX.match(raw_log)
        if not match:
            return {}

        data = match.groupdict()
        return {
            "timestamp": data.get("timestamp"),
            "user": None,  # syslog usually lacks user info
            "src_ip": None,
            "dest_ip": None,
            "host": data.get("host"),
            "process": data.get("process"),
            "event_type": "syslog",
            "message": data.get("message"),
            "raw": raw_log
        }
