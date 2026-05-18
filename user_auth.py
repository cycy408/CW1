from data_manager import DataManager


class AuthError(Exception):
    """Custom exception for authentication failures."""
    pass


class UserAuth:
    def __init__(self):
        self.data_manager = DataManager()

    def do_register(self, username, password):
        try:
            users = self.data_manager.load_users()
        except Exception as e:
            return False, f"Failed to read user data: {e}"

        if username in users:
            return False, "Username already exists"

        users[username] = password
        try:
            self.data_manager.save_users(users)
        except Exception as e:
            return False, f"Failed to save user data: {e}"

        return True, "Registration successful"

    def check_login(self, username, password):
        try:
            users = self.data_manager.load_users()
        except Exception as e:
            return False, f"Failed to read user data: {e}"

        if username in users and users[username] == password:
            return True, "Login successful"
        return False, "Incorrect username or password"