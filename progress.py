# Simple ProgressManager to persist progress to JSON.
# Keeps unlocked list, high_score, and selected character.

import json
import os

DEFAULT_PATH = "progress.json"

class ProgressManager:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.data = {
            "unlocked": ["bird"],
            "high_score": 0,
            "selected": "bird"
        }
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            self._save()
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                # ensure required keys exist
                if "unlocked" not in self.data:
                    self.data["unlocked"] = ["bird"]
                if "high_score" not in self.data:
                    self.data["high_score"] = 0
                if "selected" not in self.data:
                    self.data["selected"] = "bird"
        except Exception:
            # if file is corrupted, reset to defaults
            self.data = {
                "unlocked": ["bird"],
                "high_score": 0,
                "selected": "bird"
            }
            self._save()

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get_unlocked(self):
        return list(self.data.get("unlocked", []))

    def is_unlocked(self, name):
        return name in self.data.get("unlocked", [])

    def unlock(self, name):
        if name not in self.data.get("unlocked", []):
            self.data.setdefault("unlocked", []).append(name)
            self._save()

    def get_selected(self):
        return self.data.get("selected", "bird")

    def set_selected(self, name):
        self.data["selected"] = name
        self._save()

    def get_high_score(self):
        return int(self.data.get("high_score", 0))

    def set_high_score(self, score):
        if score > self.get_high_score():
            self.data["high_score"] = int(score)
            self._save()