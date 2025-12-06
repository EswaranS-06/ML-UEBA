import re

class NetworkClassifier:

    LABELED_SRC_PATTERNS = [
        r"src(?:addr)?[=\s:]+(\b\d{1,3}(?:\.\d{1,3}){3}\b)",
        r"source(?:Address)?[=\s:]+(\b\d{1,3}(?:\.\d{1,3}){3}\b)",
        r"orig_h[=\s:]+(\b\d{1,3}(?:\.\d{1,3}){3}\b)",  # Zeek
    ]

    LABELED_DST_PATTERNS = [
        r"dst(?:addr)?[=\s:]+(\b\d{1,3}(?:\.\d{1,3}){3}\b)",
        r"dest(?:ination)?Address[=\s:]+(\b\d{1,3}(?:\.\d{1,3}){3}\b)",
        r"resp_h[=\s:]+(\b\d{1,3}(?:\.\d{1,3}){3}\b)",  # Zeek
    ]

    @staticmethod
    def labeled_extract(message: str):
        src_ip = None
        dst_ip = None

        for pat in NetworkClassifier.LABELED_SRC_PATTERNS:
            m = re.search(pat, message)
            if m:
                src_ip = m.group(1)
                break

        for pat in NetworkClassifier.LABELED_DST_PATTERNS:
            m = re.search(pat, message)
            if m:
                dst_ip = m.group(1)
                break

        return src_ip, dst_ip

    @staticmethod
    def classify_ips(ips: list, ports: list):
        """
        Fallback: use heuristics if no labeled info.
        1 IP -> unknown role
        2 IPs -> assume ips[0] = src, ips[1] = dst
        """
        if len(ips) == 1:
            return ips[0], None

        if len(ips) >= 2:
            src_ip = ips[0]
            dst_ip = ips[1]
            return src_ip, dst_ip

        return None, None

    def extract_src_dst(self, message: str, ips: list, ports: list):
        # First: try labeled patterns
        src, dst = self.labeled_extract(message)
        if src or dst:
            return src, dst

        # Fallback: use heuristics
        return self.classify_ips(ips, ports)
