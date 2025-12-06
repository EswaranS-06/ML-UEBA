class UsernameClassifier:

    @staticmethod
    def choose(user_candidates: list):
        if not user_candidates:
            return None

        # Filter out false positives like "session" or "closed"
        bad_tokens = {"session", "closed", "invalid", "for", "user", "login"}

        cleaned = [
            u for u in user_candidates
            if u.lower() not in bad_tokens
        ]

        if cleaned:
            return cleaned[0]

        return None
