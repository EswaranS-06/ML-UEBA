import os
import re
import random
from typing import List, Tuple


# --------- CONFIG ---------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
LOG_INPUT_PATH = os.path.join(PROJECT_ROOT, "nlp", "data", "raw", "auth-anomaly.txt")

TRAIN_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "nlp", "data", "raw", "train_logs.txt")
TEST_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "nlp", "data", "raw", "test_logs.txt")

# Approx target size
AUG_PER_REAL = 30          # each real log -> ~30 synthetic variants
TRAIN_SPLIT = 0.8          # 80% train, 20% test

# Synthetic pools
SYNTH_USERS = [
    "admin", "root", "guest", "support", "oracle",
    "tomcat", "jenkins", "postgres", "deploy", "backup"
]

SYNTH_HOSTS = [
    "ip-172-31-27-153",
    "ip-172-31-55-100",
    "ip-172-31-42-210",
    "ip-172-31-11-200",
    "ip-172-31-88-050",
]

SYNTH_IPS = [
    "187.12.249.74", "124.205.250.51", "218.75.153.170",
    "111.74.238.104", "196.200.90.236", "1.93.26.70",
    "58.211.216.43", "72.46.157.64", "120.198.156.138",
    "218.2.0.129", "218.2.0.121"
]

SYNTH_ACTION_PATTERNS = [
    "Invalid user {user} from {ip}",
    "Failed password for {user} from {ip} port 22 ssh2",
    "Connection closed by {ip} [preauth]",
    "Did not receive identification string from {ip}",
    "fatal: Read from socket failed: Connection reset by peer [preauth]"
]


# --------- UTILS ---------
def is_ipv4(token: str) -> bool:
    try:
        parts = token.split(".")
        if len(parts) != 4:
            return False
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False


def tokenize(line: str) -> List[str]:
    # simple whitespace split is enough for syslog-style logs
    return line.strip().split()


# --------- REAL LOG LOADING ---------
def load_real_logs(path: str) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input log file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        logs = [line.strip() for line in f if line.strip()]

    # de-duplicate
    logs = list(dict.fromkeys(logs))
    print(f"[+] Loaded {len(logs)} unique real logs from {path}")
    return logs


# --------- ENTITY TAGGING FOR ONE LINE ---------
def tag_line(line: str) -> List[Tuple[str, str]]:
    """
    Take a single raw log line and return list of (token, BIO_tag)
    """
    tokens = tokenize(line)
    labels = ["O"] * len(tokens)

    # HOST: first token starting with ip-
    for i, tok in enumerate(tokens):
        if tok.startswith("ip-"):
            labels[i] = "B-HOST"
            break

    # PROCESS: token containing '[' and ']' after hostname (sshd[pid], CRON[pid])
    for i, tok in enumerate(tokens):
        if "[" in tok and "]" in tok and ( "sshd" in tok or "CRON" in tok or "systemd" in tok ):
            labels[i] = "B-PROCESS"
            break

    # USER by pattern "user <name>"
    for i, tok in enumerate(tokens):
        if tok.lower() == "user" and i + 1 < len(tokens):
            uname = tokens[i+1]
            labels[i+1] = "B-USER"

    # USER by "Invalid user <name>"
    m = re.search(r"Invalid user (\S+)", line)
    if m:
        uname = m.group(1)
        for i, tok in enumerate(tokens):
            if tok == uname:
                labels[i] = "B-USER"

    # Special case: "Invalid user 54.173.58.33 from 120.198.156.138"
    m = re.search(r"Invalid user (\S+) from (\d+\.\d+\.\d+\.\d+)", line)
    if m:
        user_token = m.group(1)
        src_ip = m.group(2)
        for i, tok in enumerate(tokens):
            if tok == user_token:
                labels[i] = "B-USER"
            if tok == src_ip:
                labels[i] = "B-SRC_IP"

    # SRC_IP: last IPv4 in line if not already labeled
    ipv4_positions = [i for i, tok in enumerate(tokens) if is_ipv4(tok)]
    if ipv4_positions:
        last_pos = ipv4_positions[-1]
        if labels[last_pos] == "O":
            labels[last_pos] = "B-SRC_IP"

    # ACTION: simple pattern heuristics
    action_phrases = [
        "Invalid user",
        "Connection closed",
        "Did not receive identification string",
        "fatal",
        "POSSIBLE BREAK-IN ATTEMPT",
        "Could not write ident string"
    ]

    joined = " ".join(tokens)
    for phrase in action_phrases:
        if phrase in joined:
            # Mark the phrase tokens as ACTION
            phrase_tokens = phrase.split()
            for i in range(len(tokens) - len(phrase_tokens) + 1):
                if tokens[i:i+len(phrase_tokens)] == phrase_tokens:
                    labels[i] = "B-ACTION"
                    for j in range(1, len(phrase_tokens)):
                        labels[i+j] = "I-ACTION"
                    break

    return list(zip(tokens, labels))


# --------- SYNTHETIC VARIATION ---------
def random_host() -> str:
    return random.choice(SYNTH_HOSTS)


def random_user() -> str:
    return random.choice(SYNTH_USERS)


def random_ip() -> str:
    return random.choice(SYNTH_IPS)


def augment_line(base_line: str) -> str:
    """
    Generate a synthetic variant of a real log line.
    Keep structure similar, but randomize host, user, ip, maybe action.
    """
    line = base_line

    # Replace hostname
    line = re.sub(r"ip-\d+(?:-\d+){3}", random_host(), line)

    # Randomize IPv4s
    def repl_ip(match):
        return random_ip()
    line = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", repl_ip, line)

    # Randomize 'Invalid user X' usernames
    def repl_user(match):
        return f"Invalid user {random_user()}"
    line = re.sub(r"Invalid user \S+", repl_user, line)

    # Sometimes overwrite entire message with a synthetic pattern
    if "sshd[" in line:
        # Parse syslog prefix
        m = re.match(r"^(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+):\s+(.*)$", line)
        if m:
            ts, host, proc, msg = m.groups()
            # 50% chance to replace with synthetic ssh action
            if random.random() < 0.5:
                u = random_user()
                ip = random_ip()
                pattern = random.choice(SYNTH_ACTION_PATTERNS)
                new_msg = pattern.format(user=u, ip=ip)
                line = f"{ts} {host} {proc}: {new_msg}"

    return line


# --------- MAIN PIPELINE ---------
def build_dataset():
    random.seed(42)

    real_logs = load_real_logs(LOG_INPUT_PATH)
    bio_sequences: List[List[Tuple[str,str]]] = []

    # REAL LOGS (always included at least once)
    for log in real_logs:
        tagged = tag_line(log)
        bio_sequences.append(tagged)

    # SYNTHETIC AUGMENTATION
    print(f"[+] Generating synthetic variants (target ~{AUG_PER_REAL} per real log)...")
    for log in real_logs:
        for _ in range(AUG_PER_REAL):
            syn_line = augment_line(log)
            tagged = tag_line(syn_line)
            bio_sequences.append(tagged)

    print(f"[+] Total sequences (real + synthetic): {len(bio_sequences)}")

    # Shuffle
    random.shuffle(bio_sequences)

    # Train/test split
    split_idx = int(len(bio_sequences) * TRAIN_SPLIT)
    train_seqs = bio_sequences[:split_idx]
    test_seqs = bio_sequences[split_idx:]

    # Write BIO files
    os.makedirs(os.path.dirname(TRAIN_OUTPUT_PATH), exist_ok=True)

    def write_bio(path, sequences):
        with open(path, "w", encoding="utf-8") as f:
            for seq in sequences:
                for token, label in seq:
                    f.write(f"{token} {label}\n")
                f.write("\n")  # sentence boundary

    write_bio(TRAIN_OUTPUT_PATH, train_seqs)
    write_bio(TEST_OUTPUT_PATH, test_seqs)

    print(f"[+] Train BIO written to: {TRAIN_OUTPUT_PATH}")
    print(f"[+] Test BIO written to : {TEST_OUTPUT_PATH}")
    print(f"[+] Train sequences: {len(train_seqs)}, Test sequences: {len(test_seqs)}")


if __name__ == "__main__":
    build_dataset()
