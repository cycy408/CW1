# OOP: Player + Level + QuestionBank + GameUI
import customtkinter as ctk
from tkinter import messagebox
import random


# ============================================================
#  Player — data class for player information and progress
# ============================================================
class Player:
    def __init__(self, username):
        self.username = username       # name
        self.score = 0                 # score
        self.level = 1                 # level
        self.mastered_topics = []      # mastered topics
        self.completed_levels = []     # completed level numbers

    # add score to current score
    def add_score(self, points):
        self.score += points

    # level up the player
    def level_up(self):
        self.level += 1
        self.score = 0  # reset score on level up

    # record mastered topics
    def add_topic(self, topic):
        if topic not in self.mastered_topics:
            self.mastered_topics.append(topic)

    # record completed level
    def complete_level(self, level_num):
        if level_num not in self.completed_levels:
            self.completed_levels.append(level_num)

    # convert to dict (for saving to file)
    def to_dict(self):
        return {
            "username": self.username,
            "score": self.score,
            "level": self.level,
            "mastered_topics": self.mastered_topics,
            "completed_levels": self.completed_levels
        }

    # create Player object from dict (for loading from file)
    @staticmethod
    def from_dict(data):
        player = Player(data["username"])
        player.score = data["score"]
        player.level = data["level"]
        player.mastered_topics = data["mastered_topics"]
        player.completed_levels = data.get("completed_levels", [])
        return player


# ============================================================
#  Level — data class for each level's information and logic
# ============================================================
class Level:
    def __init__(self, level_num):
        self.level_num = level_num    
        self.difficulty = self.get_difficulty()  
        self.pass_score = self.get_pass_score() 
        self.questions = []         
        self.topic = f"Python Basics - Level {level_num}"  

    # set difficulty based on level number
    def get_difficulty(self):
        if self.level_num <= 2:
            return "Easy"
        elif self.level_num <= 4:
            return "Medium"
        else:
            return "Hard"

    # set pass score 
    def get_pass_score(self):
        return 40

    # check if player passed the level
    def is_passed(self, player_score):
        return player_score >= self.pass_score

    def get_info(self):
        return (f"Level {self.level_num} | Difficulty: {self.difficulty} "
                f"| Pass Score: {self.pass_score}")


# ============================================================
#  QuestionBank — static class to store all questions for each level
# ============================================================
class QuestionBank:
    """store all questions for each level:
       {"question": str, "options": [A, B, C, D], "answer": int}
       answer is the index of the correct option (0-3)
    """

    @staticmethod
    def get_questions(level_num):
        """base on level number, return a list of questions for that level"""
        bank = {
            # -------- Level 1: Variables & Data Types --------
            1: [
                {
                    "question": "What is the output of: print(type(3.14))?",
                    "options": ["<class 'int'>", "<class 'float'>",
                                "<class 'str'>", "<class 'double'>"],
                    "answer": 1
                },
                {
                    "question": "Which keyword is used to define a variable\nin Python?",
                    "options": ["var", "let", "No keyword needed", "define"],
                    "answer": 2
                },
                {
                    "question": "What is the result of: 10 // 3?",
                    "options": ["3.33", "3", "4", "3.0"],
                    "answer": 1
                },
                {
                    "question": "Which of these is a valid variable name?",
                    "options": ["2name", "my-var", "_count", "class"],
                    "answer": 2
                },
                {
                    "question": "What type does input() return?",
                    "options": ["int", "float", "str", "bool"],
                    "answer": 2
                },
            ],

            # -------- Level 2: Strings & Operations --------
            2: [
                {
                    "question": "What does 'hello'[1] return?",
                    "options": ["'h'", "'e'", "'l'", "'o'"],
                    "answer": 1
                },
                {
                    "question": "How to get the length of string s?",
                    "options": ["s.length", "s.size()", "len(s)", "length(s)"],
                    "answer": 2
                },
                {
                    "question": "What does 'abc' * 2 produce?",
                    "options": ["'abc2'", "'abcabc'", "Error", "'abc abc'"],
                    "answer": 1
                },
                {
                    "question": "Which method converts a string to uppercase?",
                    "options": [".upper()", ".toUpper()", ".capitalize()",
                                ".UPPER()"],
                    "answer": 0
                },
                {
                    "question": "What is 'python'[-1]?",
                    "options": ["'p'", "'n'", "'o'", "Error"],
                    "answer": 1
                },
            ],

            # -------- Level 3: Lists & Tuples --------
            3: [
                {
                    "question": "How to add an element to the end of a list?",
                    "options": [".add()", ".append()", ".insert()", ".push()"],
                    "answer": 1
                },
                {
                    "question": "What is the output of: [1,2,3][1:3]?",
                    "options": ["[1, 2]", "[2, 3]", "[1, 2, 3]", "[2]"],
                    "answer": 1
                },
                {
                    "question": "Which is immutable?",
                    "options": ["list", "dict", "tuple", "set"],
                    "answer": 2
                },
                {
                    "question": "How to remove the last element of list a?",
                    "options": ["a.pop()", "a.remove()", "del a", "a.drop()"],
                    "answer": 0
                },
                {
                    "question": "What does len([1, [2, 3], 4]) return?",
                    "options": ["4", "3", "5", "Error"],
                    "answer": 1
                },
            ],

            # -------- Level 4: Conditionals & Loops --------
            4: [
                {
                    "question": "What keyword starts a conditional branch\nin Python?",
                    "options": ["switch", "if", "when", "case"],
                    "answer": 1
                },
                {
                    "question": "How many times does this loop run?\nfor i in range(5):",
                    "options": ["4", "5", "6", "Infinite"],
                    "answer": 1
                },
                {
                    "question": "What does 'break' do inside a loop?",
                    "options": ["Skips current iteration",
                                "Exits the loop",
                                "Restarts the loop",
                                "Raises an error"],
                    "answer": 1
                },
                {
                    "question": "What is range(2, 8, 2) equivalent to?",
                    "options": ["[2,3,4,5,6,7,8]", "[2,4,6,8]",
                                "[2,4,6]", "[2,3,4,5,6,7]"],
                    "answer": 2
                },
                {
                    "question": "What is the output of:\nprint(10 > 5 and 3 < 1)?",
                    "options": ["True", "False", "Error", "None"],
                    "answer": 1
                },
            ],

            # -------- Level 5: Functions --------
            5: [
                {
                    "question": "Which keyword is used to define a function?",
                    "options": ["func", "function", "def", "define"],
                    "answer": 2
                },
                {
                    "question": "What does a function return if there is\nno return statement?",
                    "options": ["0", "''", "None", "Error"],
                    "answer": 2
                },
                {
                    "question": "What is a lambda function?",
                    "options": ["A named function",
                                "An anonymous one-line function",
                                "A class method",
                                "A built-in function"],
                    "answer": 1
                },
                {
                    "question": "What does *args allow in a function?",
                    "options": ["Keyword arguments",
                                "Variable number of positional arguments",
                                "Default values",
                                "No arguments"],
                    "answer": 1
                },
                {
                    "question": "Which is correct to call function foo\nwith argument 5?",
                    "options": ["foo[5]", "call foo(5)", "foo(5)", "foo 5"],
                    "answer": 2
                },
            ],

            # -------- Level 6: Dictionaries & File I/O --------
            6: [
                {
                    "question": "How to access value of key 'a' in dict d?",
                    "options": ["d('a')", "d['a']", "d.a", "d{a}"],
                    "answer": 1
                },
                {
                    "question": "Which method returns all keys of a dict?",
                    "options": [".keys()", ".values()", ".items()",
                                ".getkeys()"],
                    "answer": 0
                },
                {
                    "question": "How to open a file for reading in Python?",
                    "options": ["open('f.txt', 'w')", "open('f.txt', 'r')",
                                "read('f.txt')", "file.open('f.txt')"],
                    "answer": 1
                },
                {
                    "question": "What does json.loads() do?",
                    "options": ["Writes JSON to file",
                                "Parses a JSON string to Python object",
                                "Converts Python object to JSON string",
                                "Reads a JSON file"],
                    "answer": 1
                },
                {
                    "question": "What is the advantage of using 'with'\nto open files?",
                    "options": ["Faster reading",
                                "Automatically closes the file",
                                "Allows binary mode only",
                                "No advantage"],
                    "answer": 1
                },
            ],

            # -------- Level 7: Exception Handling --------
            7: [
                {
                    "question": "Which keyword catches exceptions in Python?",
                    "options": ["catch", "except", "handle", "error"],
                    "answer": 1
                },
                {
                    "question": "What is the purpose of try/except?",
                    "options": ["Define functions",
                                "Handle runtime errors gracefully",
                                "Create loops",
                                "Import modules"],
                    "answer": 1
                },
                {
                    "question": "What does the 'finally' block do?",
                    "options": ["Catches the exception",
                                "Runs regardless of exception",
                                "Skips the try block",
                                "Raises a new error"],
                    "answer": 1
                },
                {
                    "question": "How to manually raise an error?",
                    "options": ["throw Error()",
                                "raise Exception()",
                                "error()",
                                "assert False"],
                    "answer": 1
                },
                {
                    "question": "When does ValueError occur?",
                    "options": ["File not found",
                                "Invalid type conversion",
                                "Key not found in dict",
                                "List index out of range"],
                    "answer": 1
                },
            ],
        }

        questions = bank.get(level_num, bank[1])
        random.shuffle(questions)
        return questions


LEVEL_TOPICS = {
    1: "Variables & Data Types",
    2: "Strings & Operations",
    3: "Lists & Tuples",
    4: "Conditionals & Loops",
    5: "Functions",
    6: "Dictionaries & File I/O",
    7: "Exception Handling",
}

LEVEL_COLORS = {
    "Easy": "#27ae60",
    "Medium": "#f39c12",
    "Hard": "#e74c3c",
}


# ============================================================
#  GameUI — custom tkinter
# ============================================================
class GameUI:
    MAX_LEVEL = 7  # max level number

    def __init__(self, player, data_manager):
        """
        player       : Player object (loaded from DataManager)
        data_manager : DataManager object (for saving progress)
        """
        self.player = player
        self.dm = data_manager
        self.current_level = None      
        self.questions = []           
        self.q_index = 0              

        # ---------- GUI ----------
        self.root = ctk.CTk()
        self.selected = ctk.IntVar(value=-1)  # selected option
        self.root.title(f"Python Learning Game - {player.username}")
        self.root.geometry("620x540")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#f0f4ff")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        top_bar = ctk.CTkFrame(self.root, fg_color="white",
                               corner_radius=14, height=60,
                               border_width=1, border_color="#e0e6f0")
        top_bar.pack(fill="x", padx=20, pady=(16, 0))
        top_bar.pack_propagate(False)

        self.lbl_user = ctk.CTkLabel(
            top_bar, text=f"Player: {player.username}",
            font=("Segoe UI", 13, "bold"), text_color="#1a1a2e")
        self.lbl_user.pack(side="left", padx=18)

        self.lbl_score = ctk.CTkLabel(
            top_bar, text="Score: 0",
            font=("Segoe UI", 13), text_color="#4a6cf7")
        self.lbl_score.pack(side="right", padx=18)

        self.lbl_level = ctk.CTkLabel(
            top_bar, text="",
            font=("Segoe UI", 13), text_color="#3a3f55")
        self.lbl_level.pack(side="right", padx=18)

        # ---------- area of question ----------
        self.card = ctk.CTkFrame(self.root, fg_color="white",
                                 corner_radius=18,
                                 border_width=1, border_color="#e0e6f0")
        self.card.pack(fill="both", expand=True, padx=20, pady=16)

        # ---------- bottom button bar ----------
        btn_bar = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_bar.pack(fill="x", padx=20, pady=(0, 16))

        self.btn_submit = ctk.CTkButton(
            btn_bar, text="Submit Answer", font=("Segoe UI", 14, "bold"),
            height=42, corner_radius=10,
            fg_color="#4a6cf7", hover_color="#3b5ae0",
            command=self.submit_answer)
        self.btn_submit.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_quit = ctk.CTkButton(
            btn_bar, text="Save & Quit", font=("Segoe UI", 14),
            height=42, corner_radius=10,
            fg_color="transparent", hover_color="#c34c4c",
            text_color="#e74c3c", border_width=2, border_color="#e74c3c",
            command=self.on_close)
        self.btn_quit.pack(side="right", expand=True, fill="x", padx=(6, 0))

        # ---------- show level selection ----------
        self.show_level_select()

    # -------------------- level selection --------------------
    def show_level_select(self):
        for w in self.card.winfo_children():
            w.destroy()

        self.btn_submit.configure(
            state="disabled", text="Select a Level",
            fg_color="#a0a8c0", hover_color="#a0a8c0")

        completed_count = len(self.player.completed_levels)
        self.lbl_level.configure(
            text=f"Completed: {completed_count}/{self.MAX_LEVEL}")
        self.lbl_score.configure(text="")

        ctk.CTkLabel(
            self.card, text="Select Level",
            font=("Segoe UI", 20, "bold"), text_color="#1a1a2e"
        ).pack(pady=(14, 10))

        for level_num in range(1, self.MAX_LEVEL + 1):
            completed = level_num in self.player.completed_levels
            topic = LEVEL_TOPICS.get(level_num, f"Level {level_num}")
            lvl = Level(level_num)
            diff_color = LEVEL_COLORS.get(lvl.difficulty, "#8892a6")

            row = ctk.CTkFrame(self.card, fg_color="#f8f9fc",
                               corner_radius=10, height=50,
                               border_width=1,
                               border_color="#c8e6c9" if completed
                               else "#e0e6f0")
            row.pack(fill="x", padx=16, pady=3)
            row.pack_propagate(False)

            mark = "Done" if completed else ""
            mark_color = "#27ae60" if completed else "#d0d7e6"
            ctk.CTkLabel(
                row, text=mark,
                font=("Segoe UI", 11, "bold"),
                text_color=mark_color, width=36
            ).pack(side="left", padx=(10, 2))

            ctk.CTkLabel(
                row, text=f"Level {level_num}: {topic}",
                font=("Segoe UI", 12, "bold"),
                text_color="#1a1a2e", anchor="w"
            ).pack(side="left", padx=4, fill="x", expand=True)

            ctk.CTkButton(
                row, text="Play", font=("Segoe UI", 11, "bold"),
                width=54, height=30, corner_radius=8,
                fg_color="#4a6cf7", hover_color="#3b5ae0",
                command=lambda ln=level_num: self.start_level(ln)
            ).pack(side="right", padx=(4, 8))

            ctk.CTkLabel(
                row, text=f" {lvl.difficulty} ",
                font=("Segoe UI", 10, "bold"),
                text_color="white", fg_color=diff_color,
                corner_radius=6, width=58, height=24
            ).pack(side="right", padx=4)

    def _build_question_ui(self):
        for w in self.card.winfo_children():
            w.destroy()

        self.lbl_qnum = ctk.CTkLabel(
            self.card, text="", font=("Segoe UI", 12),
            text_color="#8892a6")
        self.lbl_qnum.pack(anchor="w", padx=28, pady=(20, 4))

        self.lbl_question = ctk.CTkLabel(
            self.card, text="", font=("Segoe UI", 15, "bold"),
            text_color="#1a1a2e", wraplength=520, justify="left")
        self.lbl_question.pack(anchor="w", padx=28, pady=(0, 14))

        self.option_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.option_frame.pack(fill="x", padx=28)

        self.radio_buttons = []
        for i in range(4):
            rb = ctk.CTkRadioButton(
                self.option_frame, text="", variable=self.selected,
                value=i, font=("Segoe UI", 13), text_color="#3a3f55",
                fg_color="#4a6cf7", hover_color="#dce3fc",
                border_color="#b0b8d0")
            rb.pack(anchor="w", pady=5)
            self.radio_buttons.append(rb)

        self.lbl_feedback = ctk.CTkLabel(
            self.card, text="", font=("Segoe UI", 13, "bold"),
            text_color="#27ae60")
        self.lbl_feedback.pack(pady=(8, 4))

    # -------------------- level control --------------------
    def start_level(self, level_num):
        """load specified level"""
        if level_num > self.MAX_LEVEL:
            self.show_victory()
            return
        self._build_question_ui()
        self.btn_submit.configure(
            state="normal", text="Submit Answer",
            fg_color="#4a6cf7", hover_color="#3b5ae0",
            command=self.submit_answer)
        self.current_level = Level(level_num)
        self.questions = QuestionBank.get_questions(level_num)
        self.q_index = 0
        self.player.score = 0
        self.update_header()
        self.show_question()

    def update_header(self):
        """update header information"""
        lvl = self.current_level
        self.lbl_level.configure(
            text=f"Level {lvl.level_num} ({lvl.difficulty})"
                 f"  |  Pass: {lvl.pass_score}")
        self.lbl_score.configure(text=f"Score: {self.player.score}")

    def show_question(self):
        """show current question and options"""
        self.selected.set(-1)
        self.lbl_feedback.configure(text="")
        self.btn_submit.configure(text="Submit Answer",
                                  command=self.submit_answer,
                                  fg_color="#4a6cf7")

        q = self.questions[self.q_index]
        total = len(self.questions)
        self.lbl_qnum.configure(
            text=f"Question {self.q_index + 1} / {total}")
        self.lbl_question.configure(text=q["question"])
        for i, rb in enumerate(self.radio_buttons):
            rb.configure(text=q["options"][i], state="normal")

    # -------------------- answer logic --------------------
    def submit_answer(self):
        """submit answer"""
        sel = self.selected.get()
        if sel == -1:
            messagebox.showwarning("Notice", "Please select an answer!")
            return

        q = self.questions[self.q_index]
        correct = q["answer"]

        # disable options to prevent resubmission
        for rb in self.radio_buttons:
            rb.configure(state="disabled")

        if sel == correct:
            points = 10
            self.player.add_score(points)
            self.update_header()
            self.lbl_feedback.configure(
                text=f"Correct!  +{points} pts",
                text_color="#27ae60")
        else:
            correct_text = q["options"][correct]
            self.lbl_feedback.configure(
                text=f"Wrong! The answer is: {correct_text}",
                text_color="#e74c3c")

        # switch button to "Next"
        if self.q_index + 1 < len(self.questions):
            self.btn_submit.configure(text="Next Question",
                                      command=self.next_question,
                                      fg_color="#27ae60")
        else:
            self.btn_submit.configure(text="Finish Level",
                                      command=self.finish_level,
                                      fg_color="#f39c12")

    def next_question(self):
        """ move to next question in current level"""
        self.q_index += 1
        self.show_question()

    # -------------------- level conclusion --------------------
    def finish_level(self):
        """level conclusion, determine if passed"""
        lvl = self.current_level
        passed = lvl.is_passed(self.player.score)

        if passed:
            self.player.add_topic(lvl.topic)
            self.player.complete_level(lvl.level_num)
            if lvl.level_num >= self.player.level:
                self.player.level = lvl.level_num + 1
            self.save_progress()

            if len(self.player.completed_levels) >= self.MAX_LEVEL:
                self.show_victory()
                return

            messagebox.showinfo(
                "Level Passed!",
                f"Score: {self.player.score}  (need {lvl.pass_score})\n\n"
                f"Level {lvl.level_num} completed!")
            self.show_level_select()
        else:
            res = messagebox.askyesno(
                "Level Failed",
                f"Your score: {self.player.score}"
                f"  (need {lvl.pass_score})\n\n"
                f"Try this level again?")
            if res:
                self.start_level(lvl.level_num)
            else:
                self.show_level_select()

    def show_victory(self):
        for w in self.card.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.card, text="Congratulations!",
            font=("Segoe UI", 26, "bold"), text_color="#f39c12"
        ).pack(pady=(50, 10))

        ctk.CTkLabel(
            self.card, text="You have completed all levels!",
            font=("Segoe UI", 16), text_color="#3a3f55"
        ).pack(pady=(0, 6))

        topics = ", ".join(self.player.mastered_topics) or "None"
        ctk.CTkLabel(
            self.card, text=f"Mastered Topics:\n{topics}",
            font=("Segoe UI", 13), text_color="#8892a6",
            wraplength=460, justify="center"
        ).pack(pady=(10, 24))

        victory_btns = ctk.CTkFrame(self.card, fg_color="transparent")
        victory_btns.pack()

        ctk.CTkButton(
            victory_btns, text="Back to Levels",
            font=("Segoe UI", 14, "bold"),
            height=42, corner_radius=10,
            fg_color="#4a6cf7", hover_color="#3b5ae0",
            command=self.show_level_select
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            victory_btns, text="Quit Game",
            font=("Segoe UI", 14, "bold"),
            height=42, corner_radius=10,
            fg_color="transparent", hover_color="#c34c4c",
            text_color="#e74c3c", border_width=2, border_color="#e74c3c",
            command=self.on_close
        ).pack(side="left", padx=8)

        self.btn_submit.configure(
            state="disabled", text="All Levels Done!",
            fg_color="#a0a8c0", hover_color="#a0a8c0")

    # -------------------- save / exit --------------------
    def save_progress(self):
        """save current progress"""
        self.dm.save_player(self.player)

    def on_close(self):
        """save before exit"""
        self.save_progress()
        messagebox.showinfo("Saved", "Your progress has been saved!")
        self.root.destroy()

    def run(self):
        """start main loop"""
        self.root.mainloop()
