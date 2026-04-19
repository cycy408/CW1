from data_manager import DataManager

class UserAuth:
    def __init__(self):
        self.data_manager = DataManager()

    def do_register(self, username, password):
        users = self.data_manager.load_users()
        if username in users:
            return False, "用户名已存在"
        users[username] = password
        self.data_manager.save_users(users)
        return True, "注册成功"

    def check_login(self, username, password):
        users = self.data_manager.load_users()
        if username in users and users[username] == password:
            return True, "登录成功"
        return False, "账号或密码错误"