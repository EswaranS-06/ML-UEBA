from .regex_extractor import RegexExtractor
from .network_classifier import NetworkClassifier
from .process_classifier import ProcessClassifier
from .hostname_classifier import HostnameClassifier
from .username_classifier import UsernameClassifier

from nlp.ner.username_ner import UsernameNER
from preprocess.normalizer.missing_handler import MissingHandler
from nlp.embeddings.message_embedder import MessageEmbedder



class NLPPipeline:

    def __init__(self):
        self.regex = RegexExtractor()
        self.net = NetworkClassifier()
        self.embedder = MessageEmbedder()

    def run(self, df):
        enriched = df.copy()

        for idx, row in enriched.iterrows():
            msg = row.get("message", "") or ""

            # ----------------------------------
            # Extract raw entities via regex
            # ----------------------------------
            extracted = self.regex.extract(msg)

            # -------------------------
            # USERNAME (RULE+NER)
            # -------------------------
            current_user = row.get("user")

            # Rule-based username
            user = UsernameClassifier.choose(extracted["user_candidates"])

            if current_user == "unknown_user":
                if user:  
                    enriched.at[idx, "user"] = user
                else:
                    # Fallback to lightweight NER
                    ner_user = UsernameNER.extract(msg)
                    if ner_user:
                        enriched.at[idx, "user"] = ner_user

            # ----------------------------------
            # HOST
            # ----------------------------------
            host = HostnameClassifier.choose(extracted["host_candidates"])
            if (not row.get("host") or "unknown" in str(row.get("host"))) and host:
                enriched.at[idx, "host"] = host

            # ----------------------------------
            # PROCESS
            # ----------------------------------
            process = ProcessClassifier.choose(extracted["process_candidates"])
            if not row.get("process") or "unknown" in str(row.get("process")):
                if process:
                    enriched.at[idx, "process"] = process

            # ----------------------------------
            # NETWORK: classify src/dest IP
            # ----------------------------------
            src_ip, dst_ip = self.net.extract_src_dst(
                msg,
                extracted["ips"],
                extracted["ports"]
            )

            if not row.get("src_ip") and src_ip:
                enriched.at[idx, "src_ip"] = src_ip

            if not row.get("dest_ip") and dst_ip:
                enriched.at[idx, "dest_ip"] = dst_ip

        # --------------------------------------
        # Recompute missing indicators AFTER NLP
        # --------------------------------------
        for idx, row in enriched.iterrows():
            record = row.to_dict()
            record = MissingHandler.add_missing_indicators(record)

            for key, val in record.items():
                enriched.at[idx, key] = val
                
        emb_matrix = self.embedder.encode_dataframe(enriched, "message")

        return enriched, emb_matrix
