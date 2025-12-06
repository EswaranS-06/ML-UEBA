from .regex_patterns import (
    USERNAME_PATTERNS,
    IPV4_PATTERN,
    IPV6_PATTERN,
    PORT_PATTERNS,
    HOSTNAME_PATTERNS,
    PROCESS_PATTERNS
)


class RegexExtractor:

    def extract(self, message: str) -> dict:
        if not message:
            return {
                "user_candidates": [],
                "ips": [],
                "ports": [],
                "host_candidates": [],
                "process_candidates": []
            }

        # Users
        users = []
        for pat in USERNAME_PATTERNS:
            users.extend(pat.findall(message))

        # IPs
        ips = IPV4_PATTERN.findall(message)
        ips += IPV6_PATTERN.findall(message)

        # Ports
        ports = []
        for pat in PORT_PATTERNS:
            ports.extend(pat.findall(message))

        # Hosts
        hosts = []
        for pat in HOSTNAME_PATTERNS:
            hosts.extend(pat.findall(message))

        # Processes
        processes = []
        for pat in PROCESS_PATTERNS:
            processes.extend(pat.findall(message))

        return {
            "user_candidates": list(set(users)),
            "ips": list(set(ips)),
            "ports": ports,
            "host_candidates": hosts,
            "process_candidates": processes
        }
