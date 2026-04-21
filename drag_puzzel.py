import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 820, 560
FPS = 60

PALETTE = {
    "bg":           "#F5F5F5",
    "surface":      "#FFFFFF",
    "overlay":      "#E0E0E0",
    "text":         "#212121",
    "subtext":      "#757575",
    "blue":         "#42A5F5",
    "green":        "#66BB6A",
    "red":          "#EF5350",
    "yellow":       "#FFA726",
    "mauve":        "#AB47BC",
    "teal":         "#26A69A",
    "peach":        "#FF7043",
    "slot_bg":      "#E8E8E8",
    "slot_border":  "#BDBDBD",
    "block_border": "#9E9E9E",
    "white":        "#FFFFFF",
}

BLOCK_COLORS_KEYS = ["blue", "mauve", "teal", "peach", "yellow", "green"]

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

SLOT_W = 340
SLOT_H = 38
SLOT_PAD = 6
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
    for name in ["consolas", "couriernew", "monospace"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)


def get_ui_font(size, bold=False):
    for name in ["segoeui", "arial", "helvetica"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)


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
        self.font = font
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
        self.title_font = get_ui_font(22, bold=True)
        self.desc_font = get_ui_font(13)
        self.label_font = get_ui_font(11, bold=True)
        self.btn_font = get_ui_font(12, bold=True)
        self.status_font = get_ui_font(12)

        self.level = 0
        self.blocks = []
        self.slots = []
        self.dragging_block = None
        self.drag_offset = (0, 0)
        self.locked = False
        self.auto_next_timer = 0
        self.status_text = ""
        self.status_color = C["subtext"]
        self.all_done = False

        self.reset_btn = Button(WIDTH - 200, 14, BTN_W, BTN_H, "Reset", C["red"], self.btn_font)
        self.check_btn = Button(WIDTH - 110, 14, BTN_W, BTN_H, "Check", C["green"], self.btn_font)
        self.next_btn = Button(WIDTH - 110, 14, BTN_W, BTN_H, "Next >>", C["blue"], self.btn_font)
        self.next_btn.visible = False

        self._load_level(self.level)

    def _load_level(self, idx):
        self.blocks.clear()
        self.slots.clear()

        puzzle = PUZZLES[idx]
        self.correct_order = list(puzzle["lines"])
        self.title_text = puzzle["title"]
        self.desc_text = puzzle["desc"]
        self.level_text = f"Level {idx + 1} / {len(PUZZLES)}"
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

            if self.level + 1 < len(PUZZLES):
                self.status_text = f"Correct!  Loading Level {self.level + 2} ..."
                self.status_color = C["green"]
                self.auto_next_timer = FPS * 1.2
            else:
                self.status_text = "Correct! You completed all levels!"
                self.status_color = C["green"]
                self.all_done = True
        else:
            for i, s in enumerate(self.slots):
                if s.code != self.correct_order[i]:
                    s.bg_color = C["red"]
                    s.border_color = C["red"]
                else:
                    s.bg_color = C["green"]
                    s.border_color = C["green"]
            self.status_text = "Some blocks are wrong — try again."
            self.status_color = C["red"]

    def _on_reset(self):
        self.locked = False
        self.auto_next_timer = 0
        self.all_done = False
        self._load_level(self.level)

    def _go_next(self):
        self.level += 1
        self.locked = False
        self.auto_next_timer = 0
        self._load_level(self.level)

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.reset_btn.handle_event(event):
                self._on_reset()
            if self.check_btn.handle_event(event):
                self._on_check()
            if self.next_btn.handle_event(event):
                if self.locked and self.level + 1 < len(PUZZLES):
                    self._go_next()

            self.reset_btn.handle_event(event)
            self.next_btn.handle_event(event)
            self.check_btn.handle_event(event)

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
                    self.status_text = "All slots filled — click Check!"
                    self.status_color = C["subtext"]
                else:
                    self.status_text = "Drag each block into a slot on the right."
                    self.status_color = C["subtext"]

        return True

    def update(self):
        if self.auto_next_timer > 0:
            self.auto_next_timer -= 1
            if self.auto_next_timer <= 0:
                self._go_next()

    def draw(self):
        self.screen.fill(C["bg"])

        pygame.draw.rect(self.screen, C["surface"], (0, 0, WIDTH, HEADER_H))
        pygame.draw.line(self.screen, C["overlay"], (0, HEADER_H), (WIDTH, HEADER_H), 1)

        title_surf = self.title_font.render(self.title_text, True, C["blue"])
        self.screen.blit(title_surf, (20, (HEADER_H - title_surf.get_height()) // 2))

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

        if self.all_done:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))

            box_w, box_h = 420, 140
            box_x = (WIDTH - box_w) // 2
            box_y = (HEIGHT - box_h) // 2
            pygame.draw.rect(self.screen, C["white"], (box_x, box_y, box_w, box_h), border_radius=10)
            pygame.draw.rect(self.screen, C["green"], (box_x, box_y, box_w, box_h), 3, border_radius=10)

            congrats_font = get_ui_font(20, bold=True)
            msg_font = get_ui_font(14)

            t1 = congrats_font.render("Congratulations!", True, C["green"])
            t2 = msg_font.render("You've completed all puzzle levels!", True, C["text"])
            t3 = msg_font.render("Well done!", True, C["text"])

            self.screen.blit(t1, (box_x + (box_w - t1.get_width()) // 2, box_y + 24))
            self.screen.blit(t2, (box_x + (box_w - t2.get_width()) // 2, box_y + 64))
            self.screen.blit(t3, (box_x + (box_w - t3.get_width()) // 2, box_y + 96))

        if self.locked and not self.all_done and self.auto_next_timer <= 0:
            self.next_btn.visible = True
            self.check_btn.visible = False

        pygame.display.flip()

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
