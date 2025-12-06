from datetime import datetime, timezone
from .schema import TARGET_SCHEMA
from .missing_handler import MissingHandler


class Normalizer:

    def normalize_timestamp(self, ts: str):
        """
        Normalize timestamp to ISO 8601 UTC and epoch seconds.
        Accepts many formats: syslog, Windows, CloudTrail.
        """
        if ts is None:
            return None, None

        parsed = None

        # Try CloudTrail-like timestamp
        try:
            parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            pass

        # Try syslog formats: "Jan 12 12:33:00"
        if parsed is None:
            try:
                parsed = datetime.strptime(ts, "%b %d %H:%M:%S")
                # syslog does not contain year → add current year
                parsed = parsed.replace(year=datetime.utcnow().year)
            except Exception:
                pass

        # If still None → return empty fields
        if parsed is None:
            return None, None

        # Force UTC
        parsed = parsed.astimezone(timezone.utc)

        iso_ts = parsed.isoformat()
        epoch_ts = int(parsed.timestamp())

        return iso_ts, epoch_ts

    def normalize(self, parsed: dict) -> dict:

        record = {field: parsed.get(field) for field in TARGET_SCHEMA}

        # Normalize the timestamp
        iso_ts, epoch_ts = self.normalize_timestamp(record["timestamp"])
        record["timestamp"] = iso_ts
        record["epoch_timestamp"] = epoch_ts

        # Standard missing value handling
        record = MissingHandler.fill_missing(record)

        # Add indicator features
        record = MissingHandler.add_missing_indicators(record)

        return record
