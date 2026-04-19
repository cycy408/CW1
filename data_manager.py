import json
import os

class DataManager:
    def __init__(self):
        self.user_file = "users.json"
        self.progress_file = "progress.json"
        self.init_files()

    def init_files(self):
        if not os.path.exists(self.user_file):
            with open(self.user_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.progress_file):
            with open(self.progress_file, "w") as f:
                json.dump({}, f)

    def load_users(self):
        with open(self.user_file, "r") as f:
            return json.load(f)

    def save_users(self, data):
        with open(self.user_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_progress(self, username):
        with open(self.progress_file, "r") as f:
            data = json.load(f)
        return data.get(username, {"level": 1, "score": 0})

    def save_progress(self, username, progress):
        with open(self.progress_file, "r") as f:
            data = json.load(f)
        data[username] = progress
        with open(self.progress_file, "w") as f:
            json.dump(data, f, indent=2)