import json
import os


class Settings:

    def __init__(self):
        self._load_settings()

    def _load_settings(self):
        if not os.path.exists("settings.json"):
            # create settings file with default values
            # get current working directory
            cwd = os.getcwd()
            self.settings = {
                "download_path": cwd,

            }
            self._save_settings()
        else:
            with open("settings.json") as f:
                self.settings = json

    def _save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def set_default_download_path(self, path:str):
        self.settings["download_path"] = path
        self._save_settings()

    def get_download_path(self):
        return self.settings["download_path"]
