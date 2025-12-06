import re


# -----------------------------
# USERNAME PATTERNS
# -----------------------------
USERNAME_PATTERNS = [
    re.compile(r"user(?:name)?[=\s:]+(\w[\w.-]*)", re.I),
    re.compile(r"for user (\w[\w.-]*)", re.I),
    re.compile(r"Invalid user (\w[\w.-]*)", re.I),
    re.compile(r"session opened for user (\w[\w.-]*)", re.I),
    re.compile(r"session closed for user (\w[\w.-]*)", re.I),
]


# -----------------------------
# IPv4 + IPv6 PATTERNS
# -----------------------------
IPV4_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)

IPV6_PATTERN = re.compile(
    r"\b(?:[A-Fa-f0-9]{0,4}:){2,7}[A-Fa-f0-9]{0,4}\b"
)


# -----------------------------
# PORT PATTERNS
# -----------------------------
PORT_PATTERNS = [
    re.compile(r"(?:sport|src_port|srcPort|sourcePort|SPT)[=\s:]+(\d{1,5})"),
    re.compile(r"(?:dport|dest_port|dstPort|destinationPort|DPT)[=\s:]+(\d{1,5})"),
]


# -----------------------------
# HOSTNAME PATTERNS
# -----------------------------
HOSTNAME_PATTERNS = [
    re.compile(r"\bip-\d+(?:-\d+){3}\b"),
    re.compile(r"\b[a-zA-Z0-9.-]+\.(?:local|com|net|org|io)\b"),
]


# -----------------------------
# PROCESS PATTERNS
# -----------------------------
PROCESS_PATTERNS = [
    re.compile(r"(\w[\w/_.-]+)(?=\[\d+\]|:|\s)"),
    re.compile(r"\b(sshd|cron|CRON|systemd|auditd|python|java|svchost|powershell)\b", re.I),
]

