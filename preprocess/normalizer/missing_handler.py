class MissingHandler:

    @staticmethod
    def fill_missing(record: dict) -> dict:
        record["user"] = record.get("user") or "unknown_user"
        record["src_ip"] = record.get("src_ip") or None
        record["dest_ip"] = record.get("dest_ip") or None
        record["process"] = record.get("process") or "unknown_process"
        record["host"] = record.get("host") or "unknown_host"
        record["message"] = record.get("message") or ""
        record["src_port"] = record.get("src_port") or None
        record["dst_port"] = record.get("dst_port") or None
        record["protocol"] = record.get("protocol") or None
        record["bytes_in"] = record.get("bytes_in") or None
        record["bytes_out"] = record.get("bytes_out") or None


        return record

    @staticmethod
    def add_missing_indicators(record: dict) -> dict:
        record["has_user"] = 1 if record.get("user") and record["user"] != "unknown_user" else 0
        record["has_src_ip"] = 1 if record.get("src_ip") else 0
        record["has_process"] = 1 if record.get("process") and record["process"] != "unknown_process" else 0
        record["has_host"] = 1 if record.get("host") and record["host"] != "unknown_host" else 0
        record["has_dest_ip"] = 1 if record.get("dest_ip") else 0
        record["has_message"] = 1 if record.get("message") else 0
        record["has_src_port"] = 1 if record.get("src_port") else 0
        record["has_dst_port"] = 1 if record.get("dst_port") else 0
        record["has_protocol"] = 1 if record.get("protocol") else 0


        return record
