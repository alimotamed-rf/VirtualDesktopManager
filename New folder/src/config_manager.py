"""
WorkLogger
Configuration Manager
"""

import json
import os


class ConfigManager:

    def __init__(self):

        settings_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "settings.json"
        )

        settings_path = os.path.abspath(settings_path)

        with open(settings_path, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

    def get_tracked_roots(self):

        return self.settings.get("tracked_roots", [])