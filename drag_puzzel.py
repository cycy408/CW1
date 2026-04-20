import tkinter as tk
from tkinter import messagebox
import random

PALETTE = {
    "bg":           "#1e1e2e",
    "surface":      "#313244",
    "overlay":      "#45475a",
    "text":         "#cdd6f4",
    "subtext":      "#a6adc8",
    "blue":         "#89b4fa",
    "green":        "#a6e3a1",
    "red":          "#f38ba8",
    "yellow":       "#f9e2af",
    "mauve":        "#cba6f7",
    "teal":         "#94e2d5",
    "peach":        "#fab387",
    "slot_bg":      "#585b70",
    "slot_border":  "#6c7086",
    "block_border": "#7f849c",
}

BLOCK_COLORS = [PALETTE["blue"], PALETTE["mauve"], PALETTE["teal"],
                PALETTE["peach"], PALETTE["yellow"], PALETTE["green"]]

PUZZLES = [
    {
        "title": "Level 1 — Hello World",
        "desc":  "Arrange the code to print 'Hello World'",
        "lines": [
            "message = 'Hello World'",
            "print(message)",
        ],
    },
    {
        "title": "Level 2 — Sum of List",
        "desc":  "Calculate the sum of a list",
        "lines": [
            "numbers = [1, 2, 3, 4, 5]",
            "total = sum(numbers)",
            "print(total)",
        ],
    },
    {
        "title": "Level 3 — Loop",
        "desc":  "Print numbers 0 through 4",
        "lines": [
            "for i in range(5):",
            "    print(i)",
        ],
    },
    {
        "title": "Level 4 — Function",
        "desc":  "Define and call a greeting function",
        "lines": [
            "def greet(name):",
            "    return 'Hello, ' + name",
            "result = greet('Alice')",
            "print(result)",
        ],
    },
    {
        "title": "Level 5 — Conditional",
        "desc":  "Check if a number is even or odd",
        "lines": [
            "x = 7",
            "if x % 2 == 0:",
            "    print('even')",
            "else:",
            "    print('odd')",
        ],
    },
]

SLOT_W    = 340
SLOT_H    = 38
SLOT_PAD  = 6
LEFT_X    = 40
RIGHT_X   = 430
TOP_Y     = 130
BLOCK_FONT = ("Consolas", 11)
TITLE_FONT = ("Segoe UI", 20, "bold")
DESC_FONT  = ("Segoe UI", 11)
SLOT_FONT  = ("Consolas", 10)
BTN_FONT   = ("Segoe UI", 10, "bold")


class CodeDragPuzzle:

    def __init__(self, root):
        self.root = root
        self.root.title("Code Puzzle | INT101")
        self.root.geometry("820x560")
        self.root.resizable(False, False)
        self.root.config(bg=PALETTE["bg"])

        self.level = 0
        self.blocks = []
        self.slots = []
        self.drag_data = {}
        self.locked = False
        self._after_id = None

        self._build_chrome()
        self._load_level(self.level)

    def _build_chrome(self):
        header = tk.Frame(self.root, bg=PALETTE["surface"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.title_lbl = tk.Label(header, text="", font=TITLE_FONT,
                                  fg=PALETTE["blue"], bg=PALETTE["surface"])
        self.title_lbl.pack(side="left", padx=20, pady=10)

        btn_frame = tk.Frame(header, bg=PALETTE["surface"])
        btn_frame.pack(side="right", padx=16)

        self.reset_btn = self._make_button(btn_frame, "Reset", PALETTE["red"],
                                           self._on_reset)
        self.reset_btn.pack(side="left", padx=4)

        self.check_btn = self._make_button(btn_frame, "Check", PALETTE["green"],
                                           self._on_check)
        self.check_btn.pack(side="left", padx=4)

        self.next_btn = self._make_button(btn_frame, "Next >>", PALETTE["blue"],
                                          self._on_next)

        sep = tk.Frame(self.root, bg=PALETTE["overlay"], height=1)
        sep.pack(fill="x")

        self.desc_lbl = tk.Label(self.root, text="", font=DESC_FONT,
                                 fg=PALETTE["subtext"], bg=PALETTE["bg"],
                                 anchor="w")
        self.desc_lbl.pack(fill="x", padx=24, pady=(12, 0))

        col_label_frame = tk.Frame(self.root, bg=PALETTE["bg"])
        col_label_frame.pack(fill="x", padx=24, pady=(10, 0))
        tk.Label(col_label_frame, text="DRAG FROM HERE",
                 font=("Segoe UI", 9, "bold"), fg=PALETTE["overlay"],
                 bg=PALETTE["bg"]).place(x=LEFT_X - 24, y=0)
        tk.Label(col_label_frame, text="DROP IN ORDER",
                 font=("Segoe UI", 9, "bold"), fg=PALETTE["overlay"],
                 bg=PALETTE["bg"]).place(x=RIGHT_X - 24, y=0)

        self.canvas = tk.Canvas(self.root, bg=PALETTE["bg"],
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.status_bar = tk.Frame(self.root, bg=PALETTE["surface"], height=32)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)

        self.status_lbl = tk.Label(self.status_bar, text="", font=("Segoe UI", 9),
                                   fg=PALETTE["subtext"], bg=PALETTE["surface"])
        self.status_lbl.pack(side="left", padx=16)

        self.level_lbl = tk.Label(self.status_bar, text="", font=("Segoe UI", 9),
                                  fg=PALETTE["subtext"], bg=PALETTE["surface"])
        self.level_lbl.pack(side="right", padx=16)

    def _make_button(self, parent, text, color, cmd):
        btn = tk.Label(parent, text=f"  {text}  ", font=BTN_FONT,
                       fg=PALETTE["bg"], bg=color, cursor="hand2")
        btn.bind("<Button-1>", lambda e: cmd())
        btn.bind("<Enter>", lambda e: btn.config(bg=PALETTE["text"], fg=PALETTE["bg"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=color, fg=PALETTE["bg"]))
        return btn

    def _load_level(self, idx):
        for b in self.blocks:
            b.destroy()
        for s in self.slots:
            s.destroy()
        self.blocks.clear()
        self.slots.clear()

        puzzle = PUZZLES[idx]
        self.correct_order = list(puzzle["lines"])
        self.title_lbl.config(text=puzzle["title"])
        self.desc_lbl.config(text=puzzle["desc"])
        self.level_lbl.config(text=f"Level {idx + 1} / {len(PUZZLES)}")
        self.status_lbl.config(text="Drag each block into a slot on the right.",
                               fg=PALETTE["subtext"])

        n = len(puzzle["lines"])

        for i in range(n):
            sy = TOP_Y + i * (SLOT_H + SLOT_PAD)
            slot = tk.Label(self.canvas, text=f"  {i + 1}",
                            font=SLOT_FONT, anchor="w",
                            width=36, height=1,
                            bg=PALETTE["slot_bg"], fg=PALETTE["slot_border"],
                            relief="groove", bd=1)
            slot.place(x=RIGHT_X, y=sy)
            slot.code = None
            self.slots.append(slot)

        shuffled = list(puzzle["lines"])
        random.shuffle(shuffled)
        while shuffled == self.correct_order and n > 1:
            random.shuffle(shuffled)

        for i, line in enumerate(shuffled):
            by = TOP_Y + i * (SLOT_H + SLOT_PAD)
            color = BLOCK_COLORS[i % len(BLOCK_COLORS)]
            block = tk.Label(self.canvas, text=f"  {line}",
                             font=BLOCK_FONT, anchor="w",
                             width=36, height=1,
                             bg=color, fg=PALETTE["bg"],
                             relief="raised", bd=1, cursor="hand2")
            block.place(x=LEFT_X, y=by)
            block.code = line
            block.home_x = LEFT_X
            block.home_y = by
            block.color = color
            block.snapped_slot = None

            block.bind("<Button-1>", self._on_press)
            block.bind("<B1-Motion>", self._on_drag)
            block.bind("<ButtonRelease-1>", self._on_release)
            self.blocks.append(block)

    def _on_press(self, event):
        w = event.widget
        w.lift()
        self.drag_data = {"widget": w, "sx": event.x_root, "sy": event.y_root}
        w.config(relief="flat", bd=2)
        if w.snapped_slot is not None:
            w.snapped_slot.config(bg=PALETTE["slot_bg"],
                                  fg=PALETTE["slot_border"])
            w.snapped_slot.code = None
            w.snapped_slot = None

    def _on_drag(self, event):
        d = self.drag_data
        w = d["widget"]
        dx = event.x_root - d["sx"]
        dy = event.y_root - d["sy"]
        w.place(x=w.winfo_x() + dx, y=w.winfo_y() + dy)
        d["sx"] = event.x_root
        d["sy"] = event.y_root

        for slot in self.slots:
            if slot.code is None and self._overlap(w, slot):
                slot.config(bg=PALETTE["overlay"])
            elif slot.code is None:
                slot.config(bg=PALETTE["slot_bg"])

    def _on_release(self, event):
        w = self.drag_data.get("widget")
        if w is None:
            return
        w.config(relief="raised", bd=1)

        placed = False
        for slot in self.slots:
            if slot.code is not None:
                continue
            if self._overlap(w, slot):
                sx, sy = slot.winfo_x(), slot.winfo_y()
                w.place(x=sx, y=sy)
                slot.code = w.code
                slot.config(bg=PALETTE["surface"], fg=PALETTE["subtext"])
                w.snapped_slot = slot
                placed = True
                break

        if not placed:
            w.place(x=w.home_x, y=w.home_y)

        for slot in self.slots:
            if slot.code is None:
                slot.config(bg=PALETTE["slot_bg"], fg=PALETTE["slot_border"])

        filled = all(s.code is not None for s in self.slots)
        self.status_lbl.config(
            text="All slots filled — click Check!" if filled
            else "Drag each block into a slot on the right.")
        self.drag_data = {}

    def _overlap(self, widget, target):
        wx, wy = widget.winfo_x(), widget.winfo_y()
        tx, ty = target.winfo_x(), target.winfo_y()
        return abs(wx - tx) < SLOT_W * 0.4 and abs(wy - ty) < SLOT_H * 0.8

    def _on_check(self):
        if self.locked:
            return
        user_order = [s.code for s in self.slots]
        if None in user_order:
            self.status_lbl.config(text="Fill all slots first!", fg=PALETTE["yellow"])
            return

        if user_order == self.correct_order:
            self.locked = True
            for s in self.slots:
                s.config(bg=PALETTE["green"], fg=PALETTE["bg"])
            # Disable dragging on all blocks
            for b in self.blocks:
                b.unbind("<Button-1>")
                b.unbind("<B1-Motion>")
                b.unbind("<ButtonRelease-1>")
                b.config(cursor="")

            if self.level + 1 < len(PUZZLES):
                self.status_lbl.config(
                    text=f"✓ Correct!  Loading Level {self.level + 2} ...",
                    fg=PALETTE["green"])
                self._after_id = self.root.after(1200, self._go_next_level)
            else:
                self.status_lbl.config(
                    text="🎉 Correct! You completed all levels!",
                    fg=PALETTE["green"])
                self._after_id = self.root.after(800, lambda: messagebox.showinfo(
                    "Congratulations",
                    "You've completed all puzzle levels!\nWell done! 🎉"))
        else:
            for i, s in enumerate(self.slots):
                if s.code != self.correct_order[i]:
                    s.config(bg=PALETTE["red"], fg=PALETTE["text"])
                else:
                    s.config(bg=PALETTE["green"], fg=PALETTE["bg"])
            self.status_lbl.config(text="Some blocks are wrong — try again.",
                                   fg=PALETTE["red"])

    def _go_next_level(self):
        self._after_id = None
        self.level += 1
        self.locked = False
        self._load_level(self.level)

    def _on_next(self):
        if self.locked and self.level + 1 < len(PUZZLES):
            self._go_next_level()

    def _on_reset(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.locked = False
        self._load_level(self.level)


if __name__ == "__main__":
    root = tk.Tk()
    CodeDragPuzzle(root)
    root.mainloop()
