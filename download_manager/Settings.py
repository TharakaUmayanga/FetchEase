import json
import os
from pathlib import Path


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
            self.set_default_download_path(cwd)
        else:
            with open("settings.json") as f:
                self.settings = json.load(f)

    def _save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)



    def set_default_download_path(self, path):
        # create a folder if it does not exist on download_path
        path = Path.joinpath(Path(path), "FetchEase")

        if not os.path.exists(path):
            os.makedirs(path)
        # now have to create bunch of folders for different types of downloads
        for folder in ["audio", "video", "playlists", "documents", "other"]:
            if not os.path.exists(os.path.join(path, folder)):
                os.makedirs(os.path.join(path, folder))
        self.settings["download_path"] = str(path)
        self._save_settings()

    def get_download_path(self):
        return self.settings["download_path"]
