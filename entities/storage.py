import csv
import os
from datetime import datetime
from constants import HIGH_SCORE_FILE, MAX_SCORES, CSV_FIELDS


class Storage:

    def __init__(self, filepath: str = HIGH_SCORE_FILE):
        self.filepath = filepath
        self._ensure_file()

    # ── Private helpers ────────────────────────────────────────────────────────
    def _ensure_file(self):
        
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()

    # ── Public interface ───────────────────────────────────────────────────────
    def load(self) -> list:
      
        scores = []
        try:
            with open(self.filepath, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        scores.append({
                            "name":  row["name"].strip() or "???",
                            "score": int(row["score"]),
                            "wave":  int(row["wave"]),
                            "date":  row["date"].strip(),
                        })
                    except (ValueError, KeyError):
                        continue    # skip any malformed rows silently
        except FileNotFoundError:
            self._ensure_file()
        scores.sort(key=lambda r: r["score"], reverse=True)
        return scores

    def save(self, name: str, score: int, wave: int):
        scores = self.load()
        scores.append({
            "name":  name.strip() or "???",
            "score": score,
            "wave":  wave,
            "date":  datetime.now().strftime("%Y-%m-%d"),
        })
        scores.sort(key=lambda r: r["score"], reverse=True)
        scores = scores[:MAX_SCORES]

        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(scores)

    def is_high_score(self, score: int) -> bool:
       
        scores = self.load()
        if len(scores) < MAX_SCORES:
            return True
        return score > scores[-1]["score"]
