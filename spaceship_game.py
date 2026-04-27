import pygame
import random
import sys
import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from data_manager import DataManager

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Quiz Battle")

BG = (6, 8, 18)
WHITE = (220, 225, 235)
ACCENT = (55, 130, 220)
ACCENT_LIGHT = (90, 170, 255)
CYAN = (0, 210, 200)
GREEN = (50, 210, 120)
GREEN_DIM = (25, 90, 55)
RED = (210, 55, 65)
RED_DIM = (80, 20, 25)
YELLOW = (255, 210, 50)
ORANGE = (240, 140, 40)
TEXT_DIM = (70, 80, 100)
PANEL_BG = (14, 18, 32)
PANEL_BORDER = (35, 50, 85)
OPTION_BG = (20, 26, 48)
OPTION_HOVER = (30, 50, 90)

clock = pygame.time.Clock()
FPS = 60
BOSS_HP_PER_LEVEL = 50

# ---------------------- Modules & Questions ----------------------
MODULES = [
    {
        "name": "Basic Syntax",
        "questions": [
            {"question": "Which symbol starts a comment in Python?",
             "options": ["//", "#", "/* */", "--"], "answer": 1},
            {"question": "What does type(3.14) return?",
             "options": ["int", "str", "float", "bool"], "answer": 2},
            {"question": "Which is a valid variable name?",
             "options": ["2x", "my_var", "my-var", "class"], "answer": 1},
            {"question": "What does print(10 % 3) output?",
             "options": ["3", "1", "0", "10"], "answer": 1},
            {"question": "How to convert '5' to an integer?",
             "options": ["str(5)", "int('5')", "float('5')", "bool('5')"], "answer": 1},
        ]
    },
    {
        "name": "Control Structures",
        "questions": [
            {"question": "How to write an if condition in Python?",
             "options": ["if x { }", "if (x):", "if x:", "if x then"], "answer": 2},
            {"question": "What does 'break' do in a loop?",
             "options": ["Skip iteration", "Exit the loop", "Pause loop", "Restart loop"], "answer": 1},
            {"question": "What does range(3) generate?",
             "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], "answer": 1},
            {"question": "Which keyword skips to the next iteration?",
             "options": ["break", "pass", "continue", "return"], "answer": 2},
            {"question": "What does 'elif' stand for?",
             "options": ["else finally", "else if", "end if", "extra if"], "answer": 1},
        ]
    },
    {
        "name": "Data Structures",
        "questions": [
            {"question": "Which brackets create a list?",
             "options": ["{}", "()", "[]", "<>"], "answer": 2},
            {"question": "Which type is immutable?",
             "options": ["list", "dict", "set", "tuple"], "answer": 3},
            {"question": "How to add an item to a list?",
             "options": ["list.add(x)", "list.append(x)", "list.insert(x)", "list.push(x)"], "answer": 1},
            {"question": "What stores key-value pairs?",
             "options": ["list", "tuple", "dict", "set"], "answer": 2},
            {"question": "Which collection has no duplicates?",
             "options": ["list", "tuple", "dict", "set"], "answer": 3},
        ]
    },
    {
        "name": "Functions",
        "questions": [
            {"question": "Which keyword defines a function?",
             "options": ["func", "define", "def", "function"], "answer": 2},
            {"question": "What does 'return' do in a function?",
             "options": ["Prints output", "Sends a value back", "Ends program", "Loops again"], "answer": 1},
            {"question": "What is a default parameter?",
             "options": ["Required input", "Preset value param", "Global variable", "Return value"], "answer": 1},
            {"question": "What does *args accept?",
             "options": ["Keyword args", "A single arg", "Multiple positional args", "No args"], "answer": 2},
            {"question": "What is a lambda function?",
             "options": ["A class method", "Anonymous function", "A loop construct", "An error handler"], "answer": 1},
        ]
    },
    {
        "name": "OOP",
        "questions": [
            {"question": "Which keyword defines a class?",
             "options": ["def", "struct", "class", "object"], "answer": 2},
            {"question": "What is __init__ used for?",
             "options": ["Delete object", "Initialize object", "Print object", "Copy object"], "answer": 1},
            {"question": "What does 'self' refer to?",
             "options": ["The class", "Current instance", "Parent class", "A module"], "answer": 1},
            {"question": "How to inherit from class A?",
             "options": ["class B <- A:", "class B(A):", "class B extends A:", "class B: A"], "answer": 1},
            {"question": "What is encapsulation?",
             "options": ["Looping data", "Hiding internal details", "Sorting objects", "Copying classes"], "answer": 1},
        ]
    },
    {
        "name": "File IO",
        "questions": [
            {"question": "How to open a file for reading?",
             "options": ["open('f','w')", "open('f','r')", "read('f')", "load('f')"], "answer": 1},
            {"question": "What does 'w' mode do?",
             "options": ["Read only", "Write (overwrite)", "Append", "Execute"], "answer": 1},
            {"question": "Which reads all lines as a list?",
             "options": ["read()", "readline()", "readlines()", "readall()"], "answer": 2},
            {"question": "What ensures a file is closed properly?",
             "options": ["try block", "with statement", "finally block", "close()"], "answer": 1},
            {"question": "What does 'a' mode do when writing?",
             "options": ["Overwrite file", "Read file", "Append to file", "Delete file"], "answer": 2},
        ]
    },
    {
        "name": "Exception Handling",
        "questions": [
            {"question": "Which keyword catches exceptions?",
             "options": ["catch", "except", "handle", "error"], "answer": 1},
            {"question": "What is try-except used for?",
             "options": ["Define functions", "Handle runtime errors", "Create loops", "Import modules"], "answer": 1},
            {"question": "What does 'finally' do?",
             "options": ["Catches error", "Runs after try/except", "Skips error", "Raises error"], "answer": 1},
            {"question": "How to raise an error manually?",
             "options": ["throw Error", "raise Exception()", "error()", "assert False"], "answer": 1},
            {"question": "When does ValueError occur?",
             "options": ["Missing file", "Invalid conversion", "Key not found", "Index too big"], "answer": 1},
        ]
    },
]

TOTAL_LEVELS = len(MODULES)

# ---------------------- Particle ----------------------
class Particle:
    def __init__(self, x, y, color, vx=0, vy=0, life=30, size=3):
        self.x, self.y = float(x), float(y)
        self.vx = vx + random.uniform(-1.5, 1.5)
        self.vy = vy + random.uniform(-1.5, 1.5)
        self.life = life
        self.max_life = life
        self.size = size
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1

    def draw(self, surface):
        r, g, b = self.color
        ratio = self.life / self.max_life
        r = min(255, int(r * ratio))
        g = min(255, int(g * ratio))
        b = min(255, int(b * ratio))
        sz = max(1, int(self.size * ratio))
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), sz)

# ---------------------- Player ----------------------
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface((60, 56), pygame.SRCALPHA)
        pygame.draw.polygon(self.base_image, (20, 55, 130),
            [(30, 0), (18, 22), (14, 38), (18, 52), (42, 52), (46, 38), (42, 22)])
        pygame.draw.polygon(self.base_image, (35, 90, 190),
            [(30, 2), (21, 20), (17, 36), (20, 50), (40, 50), (43, 36), (39, 20)])
        pygame.draw.polygon(self.base_image, (15, 50, 120),
            [(20, 24), (0, 48), (4, 52), (18, 40)])
        pygame.draw.polygon(self.base_image, (15, 50, 120),
            [(40, 24), (60, 48), (56, 52), (42, 40)])
        pygame.draw.polygon(self.base_image, (50, 120, 220),
            [(0, 48), (4, 52), (6, 48)])
        pygame.draw.polygon(self.base_image, (50, 120, 220),
            [(60, 48), (56, 52), (54, 48)])
        pygame.draw.ellipse(self.base_image, (30, 60, 140), (24, 8, 12, 18))
        pygame.draw.ellipse(self.base_image, (80, 180, 255), (26, 10, 8, 13))
        pygame.draw.line(self.base_image, (70, 160, 255), (30, 3), (30, 8), 2)
        pygame.draw.line(self.base_image, (25, 70, 160), (24, 22), (20, 48), 1)
        pygame.draw.line(self.base_image, (25, 70, 160), (36, 22), (40, 48), 1)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        self.image = self.base_image.copy()
        flicker = random.randint(-2, 2)
        h = 6 + abs(flicker)
        pygame.draw.polygon(self.image, (60, 140, 255),
            [(24, 52), (28, 52 + h), (30, 52)])
        pygame.draw.polygon(self.image, (60, 140, 255),
            [(30, 52), (32, 52 + h + flicker), (36, 52)])
        pygame.draw.polygon(self.image, (150, 200, 255),
            [(26, 52), (28, 52 + h - 2), (29, 52)])
        pygame.draw.polygon(self.image, (150, 200, 255),
            [(31, 52), (33, 52 + h - 2 + flicker), (35, 52)])

# ---------------------- Boss ----------------------
class BossShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface((190, 130), pygame.SRCALPHA)
        img = self.base_image
        pygame.draw.polygon(img, (80, 10, 18),
            [(95, 120), (30, 48), (18, 26), (42, 4), (148, 4), (172, 26), (160, 48)])
        pygame.draw.polygon(img, (140, 18, 35),
            [(95, 115), (34, 46), (22, 26), (45, 6), (145, 6), (168, 26), (156, 46)])
        pygame.draw.polygon(img, (170, 30, 50),
            [(95, 100), (50, 42), (40, 25), (55, 12), (135, 12), (150, 25), (140, 42)])
        pygame.draw.polygon(img, (110, 10, 25),
            [(34, 46), (2, 78), (8, 90), (14, 84), (48, 58)])
        pygame.draw.polygon(img, (140, 20, 35),
            [(34, 48), (6, 78), (10, 86), (46, 56)])
        pygame.draw.polygon(img, (110, 10, 25),
            [(156, 46), (188, 78), (182, 90), (176, 84), (142, 58)])
        pygame.draw.polygon(img, (140, 20, 35),
            [(156, 48), (184, 78), (180, 86), (144, 56)])
        pygame.draw.rect(img, (90, 15, 25), (72, 14, 46, 28), border_radius=3)
        pygame.draw.rect(img, (180, 35, 55), (75, 17, 40, 22), border_radius=2)
        pygame.draw.polygon(img, (200, 50, 65), [(80, 17), (110, 17), (106, 10), (84, 10)])
        pygame.draw.rect(img, (255, 80, 60), (85, 22, 20, 8), border_radius=2)
        pygame.draw.rect(img, (255, 160, 100), (88, 24, 14, 4), border_radius=1)
        pygame.draw.circle(img, (100, 20, 30), (22, 68), 9)
        pygame.draw.circle(img, (200, 55, 70), (22, 68), 6)
        pygame.draw.circle(img, (100, 20, 30), (168, 68), 9)
        pygame.draw.circle(img, (200, 55, 70), (168, 68), 6)
        for ex in [58, 78, 98, 118]:
            pygame.draw.rect(img, (120, 20, 30), (ex, 0, 10, 8), border_radius=2)
            pygame.draw.rect(img, (255, 120, 30), (ex + 2, 1, 6, 5), border_radius=1)
        pygame.draw.line(img, (180, 40, 55), (52, 22), (138, 22), 1)
        pygame.draw.line(img, (180, 40, 55), (48, 38), (142, 38), 1)
        pygame.draw.rect(img, (120, 30, 20), (90, 92, 10, 28), border_radius=2)
        pygame.draw.rect(img, (220, 70, 30), (91, 94, 8, 24), border_radius=1)
        pygame.draw.polygon(img, (255, 100, 40), [(90, 92), (100, 92), (98, 84), (92, 84)])
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 20
        self.hp = BOSS_HP_PER_LEVEL
        self.max_hp = BOSS_HP_PER_LEVEL
        self.speed = 3
        self.direction = 1
        self.hit_flash = 0

    def take_hit(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        self.hit_flash = 8

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
        if self.hit_flash > 0:
            self.hit_flash -= 1
            flash_img = self.base_image.copy()
            overlay = pygame.Surface(flash_img.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 80))
            flash_img.blit(overlay, (0, 0))
            self.image = flash_img
        else:
            self.image = self.base_image

# ---------------------- Projectile ----------------------
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 24), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (40, 180, 255), (2, 4, 4, 20), border_radius=2)
        pygame.draw.rect(self.image, (160, 230, 255), (3, 6, 2, 16), border_radius=1)
        pygame.draw.circle(self.image, (200, 240, 255), (4, 4), 4)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 12

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# ---------------------- Game ----------------------
class Game:
    def __init__(self, username):
        self.username = username
        self.dm = DataManager()
        saved = self.dm.load_spaceship_progress(username)
        self.current_level = saved.get("level", 1)
        self.total_damage_all = saved.get("total_damage", 0)

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player = PlayerShip()
        self.boss = BossShip()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)

        self.total_damage = 0
        self.show_question = False
        self.current_question = None
        self.selected_option = 0

        self.feedback_text = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0
        self.combo = 0
        self.quiz_ready = True
        self.quiz_cooldown = 0
        self.particles = []

        # intro / playing / level_complete / victory
        self.state = "intro"

        self.stars = []
        for _ in range(60):
            self.stars.append(self._make_star(1, random.randint(0, SCREEN_HEIGHT)))
        for _ in range(40):
            self.stars.append(self._make_star(2, random.randint(0, SCREEN_HEIGHT)))
        for _ in range(15):
            self.stars.append(self._make_star(3, random.randint(0, SCREEN_HEIGHT)))
        self.nebulae = []
        for _ in range(6):
            self.nebulae.append([
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.randint(60, 140),
                random.choice([(15, 8, 30), (8, 15, 30), (10, 10, 25), (20, 8, 15)]),
                random.uniform(0.2, 0.5)
            ])

        self.tick = 0
        self.font = pygame.font.SysFont("consolas", 32)
        self.small_font = pygame.font.SysFont("consolas", 22)
        self.big_font = pygame.font.SysFont("consolas", 56)
        self.title_font = pygame.font.SysFont("consolas", 72)

    def _make_star(self, layer, y):
        speed = layer * 0.4
        brightness = 40 + layer * 35
        size = layer
        return [random.randint(0, SCREEN_WIDTH), y, speed, brightness, size]

    def get_module(self):
        idx = min(self.current_level - 1, TOTAL_LEVELS - 1)
        return MODULES[idx]

    def setup_level(self):
        self.all_sprites.empty()
        self.projectiles.empty()
        self.particles.clear()
        self.player = PlayerShip()
        self.boss = BossShip()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)
        self.total_damage = 0
        self.show_question = False
        self.current_question = None
        self.selected_option = 0
        self.feedback_text = ""
        self.feedback_timer = 0
        self.combo = 0
        self.quiz_ready = True
        self.quiz_cooldown = 0

    def spawn_particles(self, x, y, color, count=12):
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-4, 1)
            life = random.randint(15, 35)
            size = random.randint(2, 4)
            self.particles.append(Particle(x, y, color, vx, vy, life, size))

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = current + (" " if current else "") + word
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    # ---- Drawing ----
    def draw_background(self):
        screen.fill(BG)
        for nb in self.nebulae:
            x, y, radius, color, spd = nb
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, 18), (radius, radius), radius)
            pygame.draw.circle(surf, (*color, 10), (radius, radius), radius // 2)
            screen.blit(surf, (x - radius, y - radius))
            nb[1] += spd
            if nb[1] - radius > SCREEN_HEIGHT:
                nb[0] = random.randint(0, SCREEN_WIDTH)
                nb[1] = -radius
                nb[2] = random.randint(60, 140)
        for star in self.stars:
            x, y, spd, bri, sz = star
            twinkle = max(30, min(255, bri + random.randint(-10, 10)))
            if sz >= 3:
                pygame.draw.circle(screen, (twinkle, twinkle, min(255, twinkle + 20)), (int(x), int(y)), 2)
                glow = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(glow, (twinkle, twinkle, twinkle, 40), (4, 4), 4)
                screen.blit(glow, (int(x) - 4, int(y) - 4))
            elif sz >= 2:
                pygame.draw.circle(screen, (twinkle, twinkle, twinkle), (int(x), int(y)), 1)
            else:
                screen.set_at((int(x) % SCREEN_WIDTH, int(y) % SCREEN_HEIGHT), (twinkle, twinkle, twinkle))
            star[1] += spd
            if star[1] > SCREEN_HEIGHT:
                star[0] = random.randint(0, SCREEN_WIDTH)
                star[1] = 0

    def draw_rounded_bar(self, x, y, w, h, ratio, fg_color, bg_color, border_color):
        pygame.draw.rect(screen, bg_color, (x, y, w, h), border_radius=h // 2)
        fill_w = max(0, int(w * ratio))
        if fill_w > 0:
            fill_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(fill_surf, fg_color, (0, 0, fill_w, h), border_radius=h // 2)
            screen.blit(fill_surf, (x, y))
        pygame.draw.rect(screen, border_color, (x, y, w, h), 1, border_radius=h // 2)

    def draw_hud(self):
        module = self.get_module()

        # Top-left: level & module
        hud_bg = pygame.Surface((280, 50), pygame.SRCALPHA)
        pygame.draw.rect(hud_bg, (0, 0, 0, 100), (0, 0, 280, 50), border_radius=8)
        screen.blit(hud_bg, (10, 10))
        lvl = self.small_font.render(f"Lv.{self.current_level}/{TOTAL_LEVELS}", True, ACCENT_LIGHT)
        screen.blit(lvl, (22, 14))
        mod_name = self.small_font.render(module["name"], True, WHITE)
        screen.blit(mod_name, (22, 36))

        # Top-center: Boss HP
        bar_w = 340
        bar_x = SCREEN_WIDTH // 2 - bar_w // 2
        boss_hud = pygame.Surface((bar_w + 80, 50), pygame.SRCALPHA)
        pygame.draw.rect(boss_hud, (0, 0, 0, 120), (0, 0, bar_w + 80, 50), border_radius=10)
        screen.blit(boss_hud, (bar_x - 40, 10))
        boss_label = self.font.render("BOSS", True, RED)
        screen.blit(boss_label, (bar_x - 30, 16))
        self.draw_rounded_bar(bar_x + 40, 22, bar_w - 100, 14,
                              max(0, self.boss.hp / self.boss.max_hp),
                              RED, RED_DIM, (120, 30, 35))
        hp_text = self.font.render(f"{max(0, self.boss.hp)}/{self.boss.max_hp}", True, (200, 70, 80))
        screen.blit(hp_text, (bar_x + bar_w - 50, 16))

        # Top-right: combo
        if self.combo >= 2:
            combo_hud = pygame.Surface((140, 36), pygame.SRCALPHA)
            pygame.draw.rect(combo_hud, (0, 0, 0, 100), (0, 0, 140, 36), border_radius=8)
            screen.blit(combo_hud, (SCREEN_WIDTH - 155, 10))
            pulse = abs(math.sin(self.tick * 0.1)) * 30
            c = (255, int(200 + pulse), 0)
            combo_text = self.font.render(f"x{self.combo}", True, c)
            screen.blit(combo_text, (SCREEN_WIDTH - 100, 12))
            label = self.small_font.render("COMBO", True, YELLOW)
            screen.blit(label, (SCREEN_WIDTH - 148, 18))

        # Bottom hint
        if self.quiz_ready and not self.show_question:
            pulse_alpha = int(120 + 60 * math.sin(self.tick * 0.05))
            hint = self.small_font.render("[  SPACE  ]  Answer a question to attack", True, TEXT_DIM)
            hint.set_alpha(pulse_alpha)
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 36))

    def draw_feedback(self):
        if self.feedback_timer > 0:
            progress = self.feedback_timer / 50
            y_offset = int((1 - progress) * 20)
            alpha = min(255, int(progress * 300))
            text = self.font.render(self.feedback_text, True, self.feedback_color)
            text.set_alpha(alpha)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - 90 - y_offset))
            self.feedback_timer -= 1

    def draw_particles(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
            else:
                p.draw(screen)

    def new_question(self):
        module = self.get_module()
        self.current_question = random.choice(module["questions"])
        self.show_question = True
        self.selected_option = 0

    def check_answer(self):
        if self.selected_option == self.current_question["answer"]:
            self.combo += 1
            damage = 10 + (self.combo - 1) * 2
            self.boss.take_hit(damage)
            self.total_damage += damage
            self.feedback_text = f"Correct! DMG -{damage}"
            self.feedback_color = GREEN
            proj = Projectile(self.player.rect.centerx, self.player.rect.top)
            self.all_sprites.add(proj)
            self.projectiles.add(proj)
            self.spawn_particles(self.player.rect.centerx, self.player.rect.top, (60, 180, 255), 8)
        else:
            self.combo = 0
            heal = 5
            self.boss.hp = min(self.boss.max_hp, self.boss.hp + heal)
            correct = self.current_question["options"][self.current_question["answer"]]
            self.feedback_text = f"Wrong! Boss +{heal} HP (Ans: {correct})"
            self.feedback_color = RED
        self.feedback_timer = 50
        self.show_question = False
        self.quiz_ready = False
        self.quiz_cooldown = 90

        if self.boss.hp <= 0:
            self.total_damage_all += self.total_damage
            if self.current_level >= TOTAL_LEVELS:
                self.state = "victory"
            else:
                self.state = "level_complete"
            self.save_progress()

    def save_progress(self):
        next_level = min(self.current_level + 1, TOTAL_LEVELS + 1)
        self.dm.save_spaceship_progress(self.username, {
            "level": next_level,
            "total_damage": self.total_damage_all,
        })

    def draw_question(self):
        if not self.show_question:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        text_area_w = 560
        q_lines = self.wrap_text(self.current_question["question"], self.font, text_area_w)
        q_line_count = len(q_lines)
        extra_h = max(0, (q_line_count - 1) * 34)

        pw, ph = 620, 340 + extra_h
        px = SCREEN_WIDTH // 2 - pw // 2
        py = SCREEN_HEIGHT // 2 - ph // 2

        shadow = pygame.Surface((pw + 10, ph + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, pw + 10, ph + 10), border_radius=16)
        screen.blit(shadow, (px - 3, py + 3))

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (*PANEL_BG, 240), (0, 0, pw, ph), border_radius=14)
        screen.blit(panel, (px, py))

        header_h = 26 + q_line_count * 34
        header = pygame.Surface((pw, header_h), pygame.SRCALPHA)
        pygame.draw.rect(header, (25, 35, 65, 200), (0, 0, pw, header_h),
                         border_top_left_radius=14, border_top_right_radius=14)
        screen.blit(header, (px, py))
        pygame.draw.line(screen, ACCENT, (px, py + header_h), (px + pw, py + header_h), 1)

        for li, line in enumerate(q_lines):
            q_surf = self.font.render(line, True, WHITE)
            screen.blit(q_surf, (px + 28, py + 14 + li * 34))

        opt_start_y = py + header_h + 14
        for i, opt in enumerate(self.current_question["options"]):
            is_sel = (i == self.selected_option)
            opt_y = opt_start_y + i * 56
            opt_rect = pygame.Rect(px + 24, opt_y, pw - 48, 44)
            opt_surf = pygame.Surface((opt_rect.w, opt_rect.h), pygame.SRCALPHA)
            bg = (*OPTION_HOVER, 220) if is_sel else (*OPTION_BG, 180)
            pygame.draw.rect(opt_surf, bg, (0, 0, opt_rect.w, opt_rect.h), border_radius=8)
            screen.blit(opt_surf, opt_rect.topleft)
            if is_sel:
                pygame.draw.rect(screen, ACCENT_LIGHT, opt_rect, 2, border_radius=8)
                pygame.draw.rect(screen, ACCENT_LIGHT, (opt_rect.x, opt_rect.y + 8, 3, 28), border_radius=2)
            label = chr(65 + i)
            label_color = ACCENT_LIGHT if is_sel else TEXT_DIM
            text_color = WHITE if is_sel else (160, 165, 180)
            lt = self.small_font.render(label, True, label_color)
            screen.blit(lt, (opt_rect.x + 16, opt_rect.y + 12))
            ot = self.small_font.render(opt, True, text_color)
            screen.blit(ot, (opt_rect.x + 44, opt_rect.y + 12))

        pygame.draw.rect(screen, PANEL_BORDER, (px, py, pw, ph), 1, border_radius=14)
        tip = self.small_font.render("Up / Down  to select     SPACE  to confirm", True, TEXT_DIM)
        screen.blit(tip, (px + pw // 2 - tip.get_width() // 2, py + ph - 32))

    def draw_intro(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        module = self.get_module()
        lvl_text = self.title_font.render(f"Level {self.current_level}", True, ACCENT_LIGHT)
        screen.blit(lvl_text, (SCREEN_WIDTH // 2 - lvl_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        line = pygame.Surface((300, 2), pygame.SRCALPHA)
        line.fill((*ACCENT, 80))
        screen.blit(line, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))

        name_text = self.big_font.render(module["name"], True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - 10))

        info = self.small_font.render(f"{len(module['questions'])} questions  |  Boss HP: {BOSS_HP_PER_LEVEL}", True, TEXT_DIM)
        screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pulse = int(120 + 60 * math.sin(self.tick * 0.08))
        hint = self.small_font.render("[  SPACE  ]  Start", True, TEXT_DIM)
        hint.set_alpha(pulse)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 110))

    def draw_level_complete(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        module = self.get_module()
        title = self.big_font.render("Level Complete!", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        line = pygame.Surface((300, 2), pygame.SRCALPHA)
        line.fill((*GREEN, 80))
        screen.blit(line, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

        detail = self.font.render(f'"{module["name"]}" cleared!', True, WHITE)
        screen.blit(detail, (SCREEN_WIDTH // 2 - detail.get_width() // 2, SCREEN_HEIGHT // 2))

        dmg = self.font.render(f"Damage dealt: {self.total_damage}", True, CYAN)
        screen.blit(dmg, (SCREEN_WIDTH // 2 - dmg.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        next_mod = MODULES[self.current_level] if self.current_level < TOTAL_LEVELS else None
        if next_mod:
            nxt = self.small_font.render(f"Next: Level {self.current_level + 1} - {next_mod['name']}", True, TEXT_DIM)
            screen.blit(nxt, (SCREEN_WIDTH // 2 - nxt.get_width() // 2, SCREEN_HEIGHT // 2 + 85))

        pulse = int(120 + 60 * math.sin(self.tick * 0.08))
        hint = self.small_font.render("[  SPACE  ]  Continue", True, TEXT_DIM)
        hint.set_alpha(pulse)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 130))

        if self.tick % 4 == 0:
            px = SCREEN_WIDTH // 2 + random.randint(-150, 150)
            py_r = SCREEN_HEIGHT // 2 + random.randint(-40, 40)
            self.spawn_particles(px, py_r, random.choice([GREEN, CYAN, ACCENT_LIGHT]), 2)

    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        glow_r = 180 + int(30 * math.sin(self.tick * 0.06))
        glow = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (50, 40, 10, 25), (glow_r, glow_r), glow_r)
        screen.blit(glow, (SCREEN_WIDTH // 2 - glow_r, SCREEN_HEIGHT // 2 - 60 - glow_r))

        title = self.title_font.render("VICTORY", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        line = pygame.Surface((300, 2), pygame.SRCALPHA)
        line.fill((*YELLOW, 80))
        screen.blit(line, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 10))

        sub = self.font.render("All 7 modules completed!", True, WHITE)
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        dmg = self.font.render(f"Total Damage: {self.total_damage_all}", True, CYAN)
        screen.blit(dmg, (SCREEN_WIDTH // 2 - dmg.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pulse = int(120 + 60 * math.sin(self.tick * 0.08))
        restart = self.small_font.render("[ R ] Restart     [ ESC ] Quit", True, TEXT_DIM)
        restart.set_alpha(pulse)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        if self.tick % 3 == 0:
            px = SCREEN_WIDTH // 2 + random.randint(-200, 200)
            py_r = SCREEN_HEIGHT // 2 + random.randint(-60, 60)
            c = random.choice([YELLOW, ORANGE, GREEN, CYAN, ACCENT_LIGHT])
            self.spawn_particles(px, py_r, c, 2)

    def full_reset(self):
        self.current_level = 1
        self.total_damage_all = 0
        self.dm.save_spaceship_progress(self.username, {"level": 1, "total_damage": 0})
        self.setup_level()
        self.state = "intro"

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            self.tick += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

                    if self.state == "intro":
                        if event.key == pygame.K_SPACE:
                            self.setup_level()
                            self.state = "playing"

                    elif self.state == "playing":
                        if self.show_question:
                            if event.key == pygame.K_UP:
                                self.selected_option = (self.selected_option - 1) % 4
                            elif event.key == pygame.K_DOWN:
                                self.selected_option = (self.selected_option + 1) % 4
                            elif event.key == pygame.K_SPACE:
                                self.check_answer()
                        else:
                            if event.key == pygame.K_SPACE and self.quiz_ready:
                                self.new_question()

                    elif self.state == "level_complete":
                        if event.key == pygame.K_SPACE:
                            self.current_level += 1
                            self.state = "intro"

                    elif self.state == "victory":
                        if event.key == pygame.K_r:
                            self.full_reset()

            if not running:
                break

            if self.state == "playing" and not self.show_question:
                self.all_sprites.update()
                hits = pygame.sprite.spritecollide(self.boss, self.projectiles, True)
                for hit in hits:
                    self.boss.hit_flash = 8
                    self.spawn_particles(hit.rect.centerx, hit.rect.centery, (255, 100, 40), 15)
                if self.quiz_cooldown > 0:
                    self.quiz_cooldown -= 1
                    if self.quiz_cooldown <= 0:
                        self.quiz_ready = True

            self.draw_background()
            if self.state == "playing":
                self.all_sprites.draw(screen)
            elif self.state in ("intro", "level_complete", "victory"):
                self.all_sprites.draw(screen)
            self.draw_particles()

            if self.state == "playing":
                self.draw_hud()
                self.draw_feedback()
                self.draw_question()
            elif self.state == "intro":
                self.draw_hud()
                self.draw_intro()
            elif self.state == "level_complete":
                self.draw_level_complete()
            elif self.state == "victory":
                self.draw_victory()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "Guest"
    game = Game(username)
    game.run()
