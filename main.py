import os
import customtkinter as ctk
from tkinter import messagebox
from user_auth import UserAuth
from data_manager import DataManager
from game_class import GameUI

os.chdir(os.path.dirname(os.path.abspath(__file__)))


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GameMainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Learning Game - INT101")
        self.root.geometry("520x460")
        self.root.resizable(False, False)
        self.auth = UserAuth()
        self.current_user = None

        self.root.configure(fg_color="#f0f4ff")

        card = ctk.CTkFrame(
            root,
            width=400,
            height=380,
            corner_radius=20,
            fg_color="white",
            border_width=1,
            border_color="#e0e6f0",
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="Python Learning Game",
            font=("Segoe UI", 22, "bold"),
            text_color="#1a1a2e",
        ).pack(pady=(30, 2))

        ctk.CTkLabel(
            card,
            text="INT101 Coursework",
            font=("Segoe UI", 12),
            text_color="#8892a6",
        ).pack(pady=(0, 20))

        input_frame = ctk.CTkFrame(card, fg_color="transparent")
        input_frame.pack(padx=40, fill="x")

        ctk.CTkLabel(
            input_frame,
            text="Username",
            font=("Segoe UI", 12, "bold"),
            text_color="#3a3f55",
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        self.username_entry = ctk.CTkEntry(
            input_frame,
            height=38,
            corner_radius=10,
            font=("Segoe UI", 13),
            placeholder_text="Enter your username",
            border_color="#d0d7e6",
            fg_color="#f8f9fc",
        )
        self.username_entry.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            input_frame,
            text="Password",
            font=("Segoe UI", 12, "bold"),
            text_color="#3a3f55",
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        self.password_entry = ctk.CTkEntry(
            input_frame,
            height=38,
            corner_radius=10,
            font=("Segoe UI", 13),
            placeholder_text="Enter your password",
            show="*",
            border_color="#d0d7e6",
            fg_color="#f8f9fc",
        )
        self.password_entry.pack(fill="x", pady=(0, 24))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(padx=40, fill="x")

        ctk.CTkButton(
            btn_frame,
            text="Login",
            font=("Segoe UI", 14, "bold"),
            height=40,
            corner_radius=10,
            fg_color="#4a6cf7",
            hover_color="#3b5ae0",
            command=self.do_login,
        ).pack(fill="x", pady=(0, 10))

        secondary_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        secondary_frame.pack(fill="x")

        ctk.CTkButton(
            secondary_frame,
            text="Register",
            font=("Segoe UI", 13),
            height=36,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#e8ecf8",
            text_color="#4a6cf7",
            border_width=2,
            border_color="#4a6cf7",
            command=self.do_register,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ctk.CTkButton(
            secondary_frame,
            text="Quit",
            font=("Segoe UI", 13),
            height=36,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#fde8e8",
            text_color="#e74c3c",
            border_width=2,
            border_color="#e74c3c",
            command=root.quit,
        ).pack(side="right", expand=True, fill="x", padx=(5, 0))

        self.root.bind("<Return>", lambda e: self.do_login())

    def do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return

        ok, msg = self.auth.check_login(username, password)
        if ok:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.root.destroy()
        else:
            res = messagebox.askyesno("Notice", "Incorrect username or password.\nWould you like to register?")
            if res:
                self.do_register()

    def do_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return

        ok, msg = self.auth.do_register(username, password)
        if ok:
            messagebox.showinfo("Success", "Registration successful! Please login.")
        else:
            messagebox.showerror("Failed", msg)


if __name__ == "__main__":
    login_root = ctk.CTk()
    app = GameMainUI(login_root)
    login_root.mainloop()

    # 登录成功后，进入游戏
    if app.current_user:
        dm = DataManager()
        player = dm.load_player(app.current_user)
        game = GameUI(player, dm)
        game.run()
