# nlp/ner/username_ner.py

import re

class UsernameNER:
    """
    Lightweight username extractor designed for auth logs.
    Triggers only when user == 'unknown_user'.
    """

    COMMON_PATTERNS = [
        r"Invalid user (\S+)",
        r"Failed password for (\S+)",
        r"authentication failure.*user=(\S+)",
        r"user=(\S+)",                  # PAM style
        r"for user (\S+)",              # generic
        r"for (\S+) from",              # 'failed password for admin from ...'
    ]

    EXCLUDE = {
        "invalid", "unknown", "user", "root", "nologin",
        "system", "admin:", "from", "to", "uid", "gid"
    }

    @staticmethod
    def extract(message: str):
        if not message:
            return None
        
        # Apply regex patterns
        for pattern in UsernameNER.COMMON_PATTERNS:
            m = re.search(pattern, message, re.IGNORECASE)
            if m:
                candidate = m.group(1).strip().lower()

                # Reject junk values
                if candidate and candidate not in UsernameNER.EXCLUDE:
                    # remove trailing punctuation
                    return candidate.strip(",.:;[]()")

        return None
