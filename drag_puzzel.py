import pygame
import sys
import os
import json
import random

pygame.init()

WIDTH, HEIGHT = 820, 600
FPS = 60

PALETTE = {
    "bg":           "#F5F5F5",
    "surface":      "#FFFFFF",
    "overlay":      "#E0E0E0",
    "text":         "#212121",
    "subtext":      "#757575",
    "blue":         "#42A5F5",
    "green":        "#66BB6A",
    "red":          "#EF4744",
    "yellow":       "#FFA726",
    "mauve":        "#AB47BC",
    "teal":         "#26A69A",
    "peach":        "#FF7043",
    "slot_bg":      "#E8E8E8",
    "slot_border":  "#BDBDBD",
    "block_border": "#9E9E9E",
    "white":        "#FFFFFF",
    "progress_bg":  "#E0E0E0",
    "gold":         "#FFD54F",
}

BLOCK_COLORS_KEYS = ["blue", "mauve", "teal", "peach", "yellow", "green"]

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "Guest"
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.json")
# each module has 5 puzzles, each puzzle has a title, description, and 5 lines of code in correct order
MODULES = [
    {
        "key": "basic_syntax",
        "name": "Basic Syntax",
        "name_cn": "1-",
        "color": "blue",
        "puzzles": [
            {
                "title": "1 Variable & Print",
                "desc": "Create a variable and print its value",
                "lines": ["name = 'Python'", "print(name)"],
            },
            {
                "title": "2 String Concatenation",
                "desc": "Concatenate two strings and print the result",
                "lines": ["first = 'Hello'", "second = 'World'", "print(first + ' ' + second)"],
            },
            {
                "title": "3 Type Conversion",
                "desc": "Convert an integer to string for concatenation",
                "lines": ["age = 20", "text = 'Age: ' + str(age)", "print(text)"],
            },
            {
                "title": "4 Multiple Assignment",
                "desc": "Assign two variables and compute their sum",
                "lines": ["x, y = 10, 20", "z = x + y", "print(z)"],
            },
            {
                "title": "5 String Length",
                "desc": "Find and print the length of a string",
                "lines": ["msg = 'Hello World'", "length = len(msg)", "print(length)"],
            },
        ],
    },
    {
        "key": "control_structure",
        "name": "Control Structures",
        "name_cn": "2-",
        "color": "mauve",
        "puzzles": [
            {
                "title": "1 If / Else",
                "desc": "Check if a number is greater than 5",
                "lines": ["x = 10", "if x > 5:", "    print('big')", "else:", "    print('small')"],
            },
            {
                "title": "2 For Loop",
                "desc": "Print numbers 0, 1, 2 using a for loop",
                "lines": ["for i in range(3):", "    print(i)"],
            },
            {
                "title": "3 While Loop",
                "desc": "Count down from 3 to 1",
                "lines": ["n = 3", "while n > 0:", "    print(n)", "    n -= 1"],
            },
            {
                "title": "4 Loop with Condition",
                "desc": "Print only even numbers from 0 to 9",
                "lines": ["for i in range(10):", "    if i % 2 == 0:", "        print(i)"],
            },
            {
                "title": "5 Nested Loop",
                "desc": "Print all (i, j) pairs using nested loops",
                "lines": ["for i in range(3):", "    for j in range(2):", "        print(i, j)"],
            },
        ],
    },
    {
        "key": "data_structure",
        "name": "Data Structures",
        "name_cn": "3-",
        "color": "teal",
        "puzzles": [
            {
                "title": "1 List",
                "desc": "Create a list and append an item",
                "lines": ["fruits = ['apple', 'banana']", "fruits.append('cherry')", "print(fruits)"],
            },
            {
                "title": "2 Dictionary",
                "desc": "Create a dict and access a value by key",
                "lines": ["d = {'name': 'Alice', 'age': 20}", "print(d['name'])"],
            },
            {
                "title": "3 Tuple Unpacking",
                "desc": "Unpack a tuple into two variables",
                "lines": ["point = (3, 4)", "x, y = point", "print(x, y)"],
            },
            {
                "title": "4 Set Intersection",
                "desc": "Find common elements of two sets",
                "lines": ["a = {1, 2, 3}", "b = {2, 3, 4}", "print(a & b)"],
            },
            {
                "title": "5 List Comprehension",
                "desc": "Create a list of squares using comprehension",
                "lines": ["nums = [1, 2, 3, 4, 5]", "sq = [x**2 for x in nums]", "print(sq)"],
            },
        ],
    },
    {
        "key": "function",
        "name": "Functions",
        "name_cn": "4-",
        "color": "peach",
        "puzzles": [
            {
                "title": "1 Simple Function",
                "desc": "Define and call a simple function",
                "lines": ["def greet():", "    print('Hello!')", "greet()"],
            },
            {
                "title": "2 Return Value",
                "desc": "Define a function that returns the sum",
                "lines": ["def add(a, b):", "    return a + b", "result = add(3, 5)", "print(result)"],
            },
            {
                "title": "3 Default Parameter",
                "desc": "Use a default parameter value",
                "lines": ["def greet(name='World'):", "    return 'Hello, ' + name", "print(greet())", "print(greet('Alice'))"],
            },
            {
                "title": "4 Multiple Return",
                "desc": "Return multiple values from a function",
                "lines": ["def min_max(lst):", "    return min(lst), max(lst)", "lo, hi = min_max([3,1,2])", "print(lo, hi)"],
            },
            {
                "title": "5 Lambda",
                "desc": "Create and use a lambda function",
                "lines": ["double = lambda x: x * 2", "result = double(5)", "print(result)"],
            },
        ],
    },
    {
        "key": "oop",
        "name": "OOP",
        "name_cn": "5-",
        "color": "yellow",
        "puzzles": [
            {
                "title": "1 Class & Object",
                "desc": "Define a class and create an instance",
                "lines": ["class Dog:", "    def bark(self):", "        print('Woof!')", "d = Dog()", "d.bark()"],
            },
            {
                "title": "2 Constructor",
                "desc": "Use __init__ to initialize attributes",
                "lines": ["class Cat:", "    def __init__(self, name):", "        self.name = name", "c = Cat('Kitty')", "print(c.name)"],
            },
            {
                "title": "3 Method",
                "desc": "Define a class with a calculation method",
                "lines": ["class Circle:", "    def __init__(self, r):", "        self.r = r", "    def area(self):", "        return 3.14 * self.r ** 2"],
            },
            {
                "title": "4 Inheritance",
                "desc": "Create a subclass that overrides a method",
                "lines": ["class Animal:", "    def speak(self):", "        return 'sound'", "class Dog(Animal):", "    def speak(self):", "        return 'Woof'"],
            },
            {
                "title": "5 Instance Usage",
                "desc": "Build a counter class with an add method",
                "lines": ["class Counter:", "    def __init__(self):", "        self.count = 0", "    def add(self):", "        self.count += 1"],
            },
        ],
    },
    {
        "key": "file_io",
        "name": "File I/O",
        "name_cn": "6-",
        "color": "green",
        "puzzles": [
            {
                "title": "1 Write File",
                "desc": "Open a file in write mode and write content",
                "lines": ["f = open('test.txt', 'w')", "f.write('Hello')", "f.close()"],
            },
            {
                "title": "2 Read File",
                "desc": "Open a file in read mode and print content",
                "lines": ["f = open('test.txt', 'r')", "content = f.read()", "f.close()", "print(content)"],
            },
            {
                "title": "3 With Statement",
                "desc": "Use 'with' to safely write a file",
                "lines": ["with open('test.txt', 'w') as f:", "    f.write('Hello')"],
            },
            {
                "title": "4 Read Lines",
                "desc": "Read all lines and print each one",
                "lines": ["with open('data.txt', 'r') as f:", "    lines = f.readlines()", "for line in lines:", "    print(line.strip())"],
            },
            {
                "title": "5 Append Mode",
                "desc": "Append new content to an existing file",
                "lines": ["with open('log.txt', 'a') as f:", "    f.write('new line\\n')"],
            },
        ],
    },
    {
        "key": "exception",
        "name": "Exception Handling",
        "name_cn": "7-",
        "color": "red",
        "puzzles": [
            {
                "title": "1 Try / Except",
                "desc": "Handle a division by zero error",
                "lines": ["try:", "    x = 1 / 0", "except ZeroDivisionError:", "    print('Cannot divide by zero')"],
            },
            {
                "title": "2 Try / Except / Finally",
                "desc": "Use finally for cleanup after try/except",
                "lines": ["try:", "    f = open('test.txt')", "except FileNotFoundError:", "    print('File not found')", "finally:", "    print('Done')"],
            },
            {
                "title": "3 Raise Exception",
                "desc": "Raise a ValueError for invalid input",
                "lines": ["def check_age(age):", "    if age < 0:", "        raise ValueError('Invalid')", "    return age"],
            },
            {
                "title": "4 Multiple Except",
                "desc": "Handle different exception types separately",
                "lines": ["try:", "    x = int('abc')", "except ValueError:", "    print('Not a number')", "except TypeError:", "    print('Type error')"],
            },
            {
                "title": "5 Custom Exception",
                "desc": "Define and use a custom exception class",
                "lines": ["class MyError(Exception):", "    pass", "try:", "    raise MyError('oops')", "except MyError as e:", "    print(e)"],
            },
        ],
    },
]
# UI layout constants
SLOT_W = 340
SLOT_H = 36
SLOT_PAD = 5
LEFT_X = 40
RIGHT_X = 430
TOP_Y = 130
HEADER_H = 60
BTN_W = 80
BTN_H = 32


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


C = {k: hex_to_rgb(v) for k, v in PALETTE.items()}
BLOCK_COLORS = [C[k] for k in BLOCK_COLORS_KEYS]


def get_font(size, bold=False):
    for name in ["segoeui", "arial", "helvetica"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)


def load_progress():
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    user_data = data.get(USERNAME, {})
    return user_data.get("drag_puzzle", {})


def save_progress(progress):
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    if USERNAME not in data:
        data[USERNAME] = {}
    data[USERNAME]["drag_puzzle"] = progress
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class Button:
    def __init__(self, x, y, w, h, text, color, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = font
        self.hovered = False
        self.visible = True

    def draw(self, surface):
        if not self.visible:
            return
        bg = C["text"] if self.hovered else self.color
        pygame.draw.rect(surface, bg, self.rect, border_radius=4)
        txt_surf = self.font.render(self.text, True, C["white"])
        tx = self.rect.x + (self.rect.w - txt_surf.get_width()) // 2
        ty = self.rect.y + (self.rect.h - txt_surf.get_height()) // 2
        surface.blit(txt_surf, (tx, ty))

    def handle_event(self, event):
        if not self.visible:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Block:
    def __init__(self, x, y, code, color, font):
        self.rect = pygame.Rect(x, y, SLOT_W, SLOT_H)
        self.code = code
        self.color = color
        self.font = pygame.font.SysFont("consolas", 14)
        self.home_x = x
        self.home_y = y
        self.snapped_slot = None
        self.dragging = False
        self.enabled = True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, C["block_border"], self.rect, 2, border_radius=4)
        txt = self.font.render("  " + self.code, True, C["white"])
        surface.blit(txt, (self.rect.x + 6, self.rect.y + (SLOT_H - txt.get_height()) // 2))

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def go_home(self):
        self.rect.x = self.home_x
        self.rect.y = self.home_y


class Slot:
    def __init__(self, x, y, index, font):
        self.rect = pygame.Rect(x, y, SLOT_W, SLOT_H)
        self.index = index
        self.font = font
        self.code = None
        self.bg_color = C["slot_bg"]
        self.border_color = C["slot_border"]

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, self.border_color, self.rect, 1, border_radius=4)
        txt = self.font.render(f"  {self.index + 1}", True, C["slot_border"])
        surface.blit(txt, (self.rect.x + 4, self.rect.y + (SLOT_H - txt.get_height()) // 2))

    def reset_color(self):
        self.bg_color = C["slot_bg"]
        self.border_color = C["slot_border"]


class CodeDragPuzzle:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Code Puzzle | INT101")
        self.clock = pygame.time.Clock()

        self.code_font = get_font(14)
        self.slot_font = get_font(13)
        self.title_font = get_font(22, bold=True)
        self.desc_font = get_font(13)
        self.label_font = get_font(11, bold=True)
        self.btn_font = get_font(12, bold=True)
        self.status_font = get_font(12)
        self.menu_title_font = get_font(20, bold=True)
        self.menu_item_font = get_font(14, bold=True)
        self.menu_sub_font = get_font(12)
        self.menu_small_font = get_font(11)

        self.progress = load_progress()
        self.state = "menu"
        self.current_module = 0
        self.current_level = 0

        self.blocks = []
        self.slots = []
        self.dragging_block = None
        self.drag_offset = (0, 0)
        self.locked = False
        self.auto_next_timer = 0
        self.status_text = ""
        self.status_color = C["subtext"]
        self.module_done = False

        self.menu_hovered = -1

        self.back_btn = Button(10, 14, 70, BTN_H, "< Back", C["subtext"], self.btn_font)
        self.reset_btn = Button(WIDTH - 200, 14, BTN_W, BTN_H, "Reset", C["red"], self.btn_font)
        self.check_btn = Button(WIDTH - 110, 14, BTN_W, BTN_H, "Check", C["green"], self.btn_font)
        self.next_btn = Button(WIDTH - 110, 14, BTN_W, BTN_H, "Next >>", C["blue"], self.btn_font)
        self.next_btn.visible = False

    def _get_module_progress(self, module_key):
        return self.progress.get(module_key, 0)

    def _save_level_progress(self):
        mod_key = MODULES[self.current_module]["key"]
        current = self.progress.get(mod_key, 0)
        new_level = self.current_level + 1
        if new_level > current:
            self.progress[mod_key] = new_level
            save_progress(self.progress)

    def _enter_module(self, module_idx):
        self.state = "puzzle"
        self.current_module = module_idx
        mod_key = MODULES[module_idx]["key"]
        done = self.progress.get(mod_key, 0)
        self.current_level = 0 if done >= 5 else done
        self.module_done = False
        self._load_level()

    def _back_to_menu(self):
        self.state = "menu"
        self.locked = False
        self.auto_next_timer = 0
        self.module_done = False

    def _load_level(self):
        self.blocks.clear()
        self.slots.clear()
        self.locked = False
        self.module_done = False

        module = MODULES[self.current_module]
        puzzle = module["puzzles"][self.current_level]

        self.correct_order = list(puzzle["lines"])
        self.title_text = f"{module['name_cn']} — {puzzle['title']}"
        self.desc_text = puzzle["desc"]
        self.level_text = f"Level {self.current_level + 1} / 5"
        self.status_text = "Drag each block into a slot on the right."
        self.status_color = C["subtext"]
        self.next_btn.visible = False
        self.check_btn.visible = True

        n = len(puzzle["lines"])
        for i in range(n):
            sy = TOP_Y + i * (SLOT_H + SLOT_PAD)
            self.slots.append(Slot(RIGHT_X, sy, i, self.slot_font))

        shuffled = list(puzzle["lines"])
        random.shuffle(shuffled)
        while shuffled == self.correct_order and n > 1:
            random.shuffle(shuffled)

        for i, line in enumerate(shuffled):
            by = TOP_Y + i * (SLOT_H + SLOT_PAD)
            color = BLOCK_COLORS[i % len(BLOCK_COLORS)]
            self.blocks.append(Block(LEFT_X, by, line, color, self.code_font))

    def _on_check(self):
        if self.locked:
            return
        user_order = [s.code for s in self.slots]
        if None in user_order:
            self.status_text = "Fill all slots first!"
            self.status_color = C["yellow"]
            return

        if user_order == self.correct_order:
            self.locked = True
            for b in self.blocks:
                b.enabled = False
            for s in self.slots:
                s.bg_color = C["green"]
                s.border_color = C["green"]

            self._save_level_progress()

            if self.current_level + 1 < 5:
                self.status_text = f"Correct!  Loading Level {self.current_level + 2} ..."
                self.status_color = C["green"]
                self.auto_next_timer = FPS * 1.2
            else:
                self.status_text = "Correct! Module complete!"
                self.status_color = C["green"]
                self.module_done = True
        else:
            for i, s in enumerate(self.slots):
                if s.code != self.correct_order[i]:
                    s.bg_color = C["red"]
                    s.border_color = C["red"]
                else:
                    s.bg_color = C["green"]
                    s.border_color = C["green"]
            self.status_text = "Some blocks are wrong -- try again."
            self.status_color = C["red"]

    def _on_reset(self):
        self.locked = False
        self.auto_next_timer = 0
        self.module_done = False
        self._load_level()

    def _go_next(self):
        self.current_level += 1
        self.locked = False
        self.auto_next_timer = 0
        self._load_level()

    def _find_block_at(self, pos):
        for block in reversed(self.blocks):
            if block.contains(pos) and block.enabled:
                return block
        return None

    def _find_snap_slot(self, block):
        for slot in self.slots:
            if slot.code is not None:
                continue
            if block.rect.colliderect(slot.rect.inflate(SLOT_W * -0.2, SLOT_H * -0.1)):
                return slot
        return None

    def _get_menu_rects(self):
        rects = []
        start_y = 110
        item_h = 56
        gap = 8
        pad_x = 60
        w = WIDTH - pad_x * 2
        for i in range(len(MODULES)):
            y = start_y + i * (item_h + gap)
            rects.append(pygame.Rect(pad_x, y, w, item_h))
        return rects

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == "menu":
                self._handle_menu_event(event)
            else:
                self._handle_puzzle_event(event)

        return True

    def _handle_menu_event(self, event):
        rects = self._get_menu_rects()
        if event.type == pygame.MOUSEMOTION:
            self.menu_hovered = -1
            for i, r in enumerate(rects):
                if r.collidepoint(event.pos):
                    self.menu_hovered = i
                    break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(rects):
                if r.collidepoint(event.pos):
                    self._enter_module(i)
                    break

    def _handle_puzzle_event(self, event):
        if self.back_btn.handle_event(event):
            self._back_to_menu()
            return
        if self.reset_btn.handle_event(event):
            self._on_reset()
        if self.check_btn.handle_event(event):
            self._on_check()
        if self.next_btn.handle_event(event):
            if self.locked and self.current_level + 1 < 5:
                self._go_next()

        self.back_btn.handle_event(event)
        self.reset_btn.handle_event(event)
        self.next_btn.handle_event(event)
        self.check_btn.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._back_to_menu()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.locked:
            block = self._find_block_at(event.pos)
            if block:
                self.dragging_block = block
                self.drag_offset = (event.pos[0] - block.rect.x, event.pos[1] - block.rect.y)
                if block.snapped_slot is not None:
                    block.snapped_slot.code = None
                    block.snapped_slot.reset_color()
                    block.snapped_slot = None
                self.blocks.remove(block)
                self.blocks.append(block)

        elif event.type == pygame.MOUSEMOTION and self.dragging_block:
            self.dragging_block.rect.x = event.pos[0] - self.drag_offset[0]
            self.dragging_block.rect.y = event.pos[1] - self.drag_offset[1]
            for slot in self.slots:
                if slot.code is None:
                    if self.dragging_block.rect.colliderect(slot.rect):
                        slot.bg_color = C["overlay"]
                    else:
                        slot.reset_color()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging_block:
            block = self.dragging_block
            self.dragging_block = None
            snap = self._find_snap_slot(block)
            if snap:
                block.rect.x = snap.rect.x
                block.rect.y = snap.rect.y
                snap.code = block.code
                snap.bg_color = hex_to_rgb("#D0E8D0")
                snap.border_color = C["green"]
                block.snapped_slot = snap
            else:
                block.go_home()

            for slot in self.slots:
                if slot.code is None:
                    slot.reset_color()

            filled = all(s.code is not None for s in self.slots)
            if filled:
                self.status_text = "All slots filled -- click Check!"
                self.status_color = C["subtext"]
            else:
                self.status_text = "Drag each block into a slot on the right."
                self.status_color = C["subtext"]

    def update(self):
        if self.state == "puzzle" and self.auto_next_timer > 0:
            self.auto_next_timer -= 1
            if self.auto_next_timer <= 0:
                self._go_next()

    def draw(self):
        self.screen.fill(C["bg"])
        if self.state == "menu":
            self._draw_menu()
        else:
            self._draw_puzzle()
        pygame.display.flip()

    def _draw_menu(self):
        pygame.draw.rect(self.screen, C["surface"], (0, 0, WIDTH, HEADER_H))
        pygame.draw.line(self.screen, C["overlay"], (0, HEADER_H), (WIDTH, HEADER_H), 1)

        title_surf = self.title_font.render("Code Puzzle", True, C["blue"])
        self.screen.blit(title_surf, (20, (HEADER_H - title_surf.get_height()) // 2))

        user_surf = self.menu_sub_font.render(f"Player: {USERNAME}", True, C["subtext"])
        self.screen.blit(user_surf, (WIDTH - user_surf.get_width() - 20,
                                     (HEADER_H - user_surf.get_height()) // 2))

        sub_surf = self.desc_font.render("Select a module to practice", True, C["subtext"])
        self.screen.blit(sub_surf, (24, HEADER_H + 16))

        total_done = sum(1 for m in MODULES if self.progress.get(m["key"], 0) >= 5)
        total_surf = self.menu_small_font.render(
            f"Overall: {total_done} / {len(MODULES)} modules completed", True, C["subtext"])
        self.screen.blit(total_surf, (WIDTH - total_surf.get_width() - 24, HEADER_H + 18))

        rects = self._get_menu_rects()
        for i, module in enumerate(MODULES):
            r = rects[i]
            done = self.progress.get(module["key"], 0)
            mod_color = C[module["color"]]

            if self.menu_hovered == i:
                pygame.draw.rect(self.screen, C["overlay"], r, border_radius=8)
            else:
                pygame.draw.rect(self.screen, C["surface"], r, border_radius=8)
            pygame.draw.rect(self.screen, mod_color, r, 2, border_radius=8)

            bar_x = r.x + 4
            bar_w = 6
            bar_rect = pygame.Rect(bar_x, r.y + 4, bar_w, r.h - 8)
            pygame.draw.rect(self.screen, mod_color, bar_rect, border_radius=3)

            name_surf = self.menu_item_font.render(
                f"{module['name_cn']}  {module['name']}", True, C["text"])
            self.screen.blit(name_surf, (r.x + 20, r.y + 8))

            prog_bar_w = 120
            prog_bar_h = 10
            prog_x = r.x + r.w - prog_bar_w - 60
            prog_y = r.y + (r.h - prog_bar_h) // 2

            pygame.draw.rect(self.screen, C["progress_bg"],
                             (prog_x, prog_y, prog_bar_w, prog_bar_h), border_radius=5)
            if done > 0:
                fill_w = int(prog_bar_w * min(done, 5) / 5)
                pygame.draw.rect(self.screen, mod_color,
                                 (prog_x, prog_y, fill_w, prog_bar_h), border_radius=5)

            count_surf = self.menu_sub_font.render(f"{min(done, 5)}/5", True, C["text"])
            self.screen.blit(count_surf, (r.x + r.w - 50, r.y + (r.h - count_surf.get_height()) // 2))

            if done >= 5:
                star_surf = self.menu_item_font.render("*", True, C["gold"])
                self.screen.blit(star_surf, (r.x + r.w - 18, r.y + 4))

            desc_texts = {
                "basic_syntax": "Variables, strings, types",
                "control_structure": "if / for / while",
                "data_structure": "list / dict / tuple / set",
                "function": "def, return, lambda",
                "oop": "class, __init__, inheritance",
                "file_io": "open, read, write, with",
                "exception": "try / except / raise",
            }
            desc_surf = self.menu_small_font.render(
                desc_texts.get(module["key"], ""), True, C["subtext"])
            self.screen.blit(desc_surf, (r.x + 20, r.y + 30))

        pygame.draw.rect(self.screen, C["surface"], (0, HEIGHT - 34, WIDTH, 34))
        pygame.draw.line(self.screen, C["overlay"], (0, HEIGHT - 34), (WIDTH, HEIGHT - 34), 1)
        footer_surf = self.status_font.render("Click a module to start  |  ESC to quit",
                                              True, C["subtext"])
        self.screen.blit(footer_surf, (16, HEIGHT - 28))

    def _draw_puzzle(self):
        pygame.draw.rect(self.screen, C["surface"], (0, 0, WIDTH, HEADER_H))
        pygame.draw.line(self.screen, C["overlay"], (0, HEADER_H), (WIDTH, HEADER_H), 1)

        title_surf = self.title_font.render(self.title_text, True, C["blue"])
        self.screen.blit(title_surf, (90, (HEADER_H - title_surf.get_height()) // 2))

        self.back_btn.draw(self.screen)
        self.reset_btn.draw(self.screen)
        self.check_btn.draw(self.screen)
        self.next_btn.draw(self.screen)

        desc_surf = self.desc_font.render(self.desc_text, True, C["subtext"])
        self.screen.blit(desc_surf, (24, HEADER_H + 14))

        col1_surf = self.label_font.render("DRAG FROM HERE", True, C["slot_border"])
        self.screen.blit(col1_surf, (LEFT_X, TOP_Y - 24))
        col2_surf = self.label_font.render("DROP IN ORDER", True, C["slot_border"])
        self.screen.blit(col2_surf, (RIGHT_X, TOP_Y - 24))

        for slot in self.slots:
            slot.draw(self.screen)
        for block in self.blocks:
            block.draw(self.screen)

        pygame.draw.rect(self.screen, C["surface"], (0, HEIGHT - 34, WIDTH, 34))
        pygame.draw.line(self.screen, C["overlay"], (0, HEIGHT - 34), (WIDTH, HEIGHT - 34), 1)

        status_surf = self.status_font.render(self.status_text, True, self.status_color)
        self.screen.blit(status_surf, (16, HEIGHT - 28))

        level_surf = self.status_font.render(self.level_text, True, C["subtext"])
        self.screen.blit(level_surf, (WIDTH - level_surf.get_width() - 16, HEIGHT - 28))

        if self.module_done:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))

            box_w, box_h = 420, 160
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2
            pygame.draw.rect(self.screen, C["white"],
                             (box_x, box_y, box_w, box_h), border_radius=10)
            pygame.draw.rect(self.screen, C["green"],
                             (box_x, box_y, box_w, box_h), 3, border_radius=10)

            congrats_font = get_font(20, bold=True)
            msg_font = get_font(14)

            mod_name = MODULES[self.current_module]["name_cn"]
            t1 = congrats_font.render("Module Complete!", True, C["green"])
            t2 = msg_font.render(f"You finished all 5 levels of [{mod_name}]", True, C["text"])
            t3 = msg_font.render("Click anywhere to return to menu", True, C["subtext"])

            self.screen.blit(t1, (box_x + (box_w - t1.get_width()) // 2, box_y + 24))
            self.screen.blit(t2, (box_x + (box_w - t2.get_width()) // 2, box_y + 68))
            self.screen.blit(t3, (box_x + (box_w - t3.get_width()) // 2, box_y + 108))

            for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                self._back_to_menu()

        if self.locked and not self.module_done and self.auto_next_timer <= 0:
            self.next_btn.visible = True
            self.check_btn.visible = False

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    game = CodeDragPuzzle()
    game.run()
