class HostnameClassifier:

    @staticmethod
    def choose(host_candidates: list):
        if not host_candidates:
            return None

        # Prefer AWS-style or FQDN-style hosts
        for h in host_candidates:
            if h.startswith("ip-"):
                return h
            if "." in h:
                return h

        return host_candidates[0]
