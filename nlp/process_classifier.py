class ProcessClassifier:

    @staticmethod
    def choose(process_candidates: list):
        if not process_candidates:
            return None

        # Prefer common OS processes
        COMMON = {"sshd", "CRON", "cron", "systemd", "auditd", "svchost", "powershell"}

        for p in process_candidates:
            if p.lower() in {c.lower() for c in COMMON}:
                return p

        # fallback: return first
        return process_candidates[0]
