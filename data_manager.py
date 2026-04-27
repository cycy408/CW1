import json
import os
from game_class import Player

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

    # 加载玩家（OOP）
    def load_player(self, username):
        with open(self.progress_file, "r") as f:
            data = json.load(f)
        if username in data:
            return Player.from_dict(data[username])
        return Player(username)

    def save_player(self, player):
        with open(self.progress_file, "r") as f:
            data = json.load(f)
        if player.username not in data:
            data[player.username] = {}
        data[player.username].update(player.to_dict())
        with open(self.progress_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_spaceship_progress(self, username):
        with open(self.progress_file, "r") as f:
            data = json.load(f)
        user_data = data.get(username, {})
        return user_data.get("spaceship", {"level": 1, "total_damage": 0})

    def save_spaceship_progress(self, username, spaceship_data):
        with open(self.progress_file, "r") as f:
            data = json.load(f)
        if username not in data:
            data[username] = {}
        data[username]["spaceship"] = spaceship_data
        with open(self.progress_file, "w") as f:
            json.dump(data, f, indent=2)