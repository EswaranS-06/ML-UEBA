from .base_parser import BaseParser
import re


class NetworkParser(BaseParser):
    """
    A flexible parser for ANY network-style logs.
    Supports dict input (structured logs) and text logs (firewall, IDS, NetFlow, VPC flow, etc.)
    """

    FIELD_MAP = {
        # IPv4 / IPv6 related fields
        "src": "src_ip",
        "source_ip": "src_ip",
        "src_ip": "src_ip",
        "sourceipv4address": "src_ip",

        "dst": "dest_ip",
        "dest_ip": "dest_ip",
        "dst_ip": "dest_ip",
        "destinationipv4address": "dest_ip",

        # Ports
        "sport": "src_port",
        "src_port": "src_port",
        "sourceport": "src_port",

        "dport": "dst_port",
        "dest_port": "dst_port",
        "destinationport": "dst_port",

        # Protocols
        "proto": "protocol",
        "protocol": "protocol",

        # Traffic stats
        "bytes": "bytes",
        "bytes_in": "bytes_in",
        "bytes_out": "bytes_out",

        # Actions / metadata
        "action": "action",
        "acl": "action",
        "eventtype": "action",

        "interface": "interface",
        "logstatus": "log_status",
        "severity": "severity",
        "signature": "signature",
    }


    # -------------------------------------------------------------
    # PARSE DICT STRUCTURED LOGS (JSON / dict logs)
    # -------------------------------------------------------------
    def parse_dict(self, raw: dict) -> dict:
        parsed = {
            "timestamp": raw.get("timestamp") or raw.get("time") or raw.get("@timestamp"),
            "user": None,
            "src_ip": None,
            "dest_ip": None,
            "src_port": None,
            "dst_port": None,
            "protocol": raw.get("protocol"),
            "bytes_in": raw.get("bytes_in"),
            "bytes_out": raw.get("bytes_out"),
            "process": "network",
            "host": raw.get("device") or raw.get("hostname"),
            "event_type": raw.get("event_type") or "network_event",
            "message": raw.get("message"),
            "raw": raw
        }

        # Apply field mappings
        for k, v in raw.items():
            key = k.lower()
            for pattern, target in self.FIELD_MAP.items():
                if key == pattern.lower():
                    parsed[target] = v

        return parsed


    # -------------------------------------------------------------
    # PARSE TEXT LOGS (firewall syslog, zeek text, ASA, FortiGate, etc.)
    # -------------------------------------------------------------
    def parse_text(self, raw: str) -> dict:

        # Extract IPs
        ips = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", raw)
        src_ip = ips[0] if len(ips) > 0 else None
        dest_ip = ips[1] if len(ips) > 1 else None

        # Extract ports (naive fallback)
        ports = re.findall(r"\b\d{1,5}\b", raw)
        src_port = ports[0] if len(ports) > 0 else None
        dst_port = ports[1] if len(ports) > 1 else None

        # Extract protocol (simple matcher)
        protocol_match = re.search(r"\b(tcp|udp|icmp)\b", raw, re.I)
        protocol = protocol_match.group(1).lower() if protocol_match else None

        return {
            "timestamp": None,
            "user": None,
            "src_ip": src_ip,
            "dest_ip": dest_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "protocol": protocol,
            "process": "network",
            "host": None,
            "event_type": "network_event",
            "message": raw,
            "raw": raw
        }


    def parse(self, raw_log):
        if isinstance(raw_log, dict):
            return self.parse_dict(raw_log)

        return self.parse_text(raw_log)
