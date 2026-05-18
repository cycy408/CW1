import json
import os
from game_class import Player
# data manager handles all file operations for user data and progress
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
        try:
            with open(self.user_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self, data):
        try:
            with open(self.user_file, "w") as f:
                json.dump(data, f, indent=2)
        except (FileNotFoundError, json.JSONDecodeError):
            self.init_files()
            with open(self.user_file, "w") as f:
                json.dump(data, f, indent=2)

    def load_progress(self, username):
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"level": 1, "score": 0}
        return data.get(username, {"level": 1, "score": 0})

    def save_progress(self, username, progress):
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data[username] = progress
        try:
            with open(self.progress_file, "w") as f:
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            self.init_files()
            with open(self.progress_file, "w") as f:
                json.dump(data, f, indent=2)

    # load the player data (OOP)
    def load_player(self, username):
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return Player(username)
        if username in data:
            return Player.from_dict(data[username])
        return Player(username)

    def save_player(self, player):
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if player.username not in data:
            data[player.username] = {}
        data[player.username].update(player.to_dict())
        try:
            with open(self.progress_file, "w") as f:
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            self.init_files()
            with open(self.progress_file, "w") as f:
                json.dump(data, f, indent=2)

    def load_spaceship_progress(self, username):
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"level": 1, "total_damage": 0}
        user_data = data.get(username, {})
        return user_data.get("spaceship", {"level": 1, "total_damage": 0})

    def save_spaceship_progress(self, username, spaceship_data):
        try:
            with open(self.progress_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if username not in data:
            data[username] = {}
        data[username]["spaceship"] = spaceship_data
        try:
            with open(self.progress_file, "w") as f:
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            self.init_files()
            with open(self.progress_file, "w") as f:
                json.dump(data, f, indent=2)