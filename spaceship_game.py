import pygame
import random
import sys
import math

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Quiz Battle")

# -- Refined palette --
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
BOSS_MAX_HP = 50

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
        alpha = int(255 * (self.life / self.max_life))
        r, g, b = self.color
        r = min(255, int(r * (self.life / self.max_life)))
        g = min(255, int(g * (self.life / self.max_life)))
        b = min(255, int(b * (self.life / self.max_life)))
        sz = max(1, int(self.size * (self.life / self.max_life)))
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), sz)

# ---------------------- Player ----------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface((60, 56), pygame.SRCALPHA)
        # Hull - layered for depth
        pygame.draw.polygon(self.base_image, (20, 55, 130),
            [(30, 0), (18, 22), (14, 38), (18, 52), (42, 52), (46, 38), (42, 22)])
        pygame.draw.polygon(self.base_image, (35, 90, 190),
            [(30, 2), (21, 20), (17, 36), (20, 50), (40, 50), (43, 36), (39, 20)])
        # Wings
        pygame.draw.polygon(self.base_image, (15, 50, 120),
            [(20, 24), (0, 48), (4, 52), (18, 40)])
        pygame.draw.polygon(self.base_image, (15, 50, 120),
            [(40, 24), (60, 48), (56, 52), (42, 40)])
        # Wing edges
        pygame.draw.polygon(self.base_image, (50, 120, 220),
            [(0, 48), (4, 52), (6, 48)])
        pygame.draw.polygon(self.base_image, (50, 120, 220),
            [(60, 48), (56, 52), (54, 48)])
        # Cockpit
        pygame.draw.ellipse(self.base_image, (30, 60, 140), (24, 8, 12, 18))
        pygame.draw.ellipse(self.base_image, (80, 180, 255), (26, 10, 8, 13))
        # Nose accent
        pygame.draw.line(self.base_image, (70, 160, 255), (30, 3), (30, 8), 2)
        # Panel lines
        pygame.draw.line(self.base_image, (25, 70, 160), (24, 22), (20, 48), 1)
        pygame.draw.line(self.base_image, (25, 70, 160), (36, 22), (40, 48), 1)

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed = 8
        self.flame_tick = 0

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
        self.flame_tick += 1
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
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface((190, 130), pygame.SRCALPHA)
        img = self.base_image
        # Main hull shadow
        pygame.draw.polygon(img, (80, 10, 18),
            [(95, 120), (30, 48), (18, 26), (42, 4), (148, 4), (172, 26), (160, 48)])
        # Main hull
        pygame.draw.polygon(img, (140, 18, 35),
            [(95, 115), (34, 46), (22, 26), (45, 6), (145, 6), (168, 26), (156, 46)])
        # Hull highlight
        pygame.draw.polygon(img, (170, 30, 50),
            [(95, 100), (50, 42), (40, 25), (55, 12), (135, 12), (150, 25), (140, 42)])
        # Left wing
        pygame.draw.polygon(img, (110, 10, 25),
            [(34, 46), (2, 78), (8, 90), (14, 84), (48, 58)])
        pygame.draw.polygon(img, (140, 20, 35),
            [(34, 48), (6, 78), (10, 86), (46, 56)])
        # Right wing
        pygame.draw.polygon(img, (110, 10, 25),
            [(156, 46), (188, 78), (182, 90), (176, 84), (142, 58)])
        pygame.draw.polygon(img, (140, 20, 35),
            [(156, 48), (184, 78), (180, 86), (144, 56)])
        # Command bridge
        pygame.draw.rect(img, (90, 15, 25), (72, 14, 46, 28), border_radius=3)
        pygame.draw.rect(img, (180, 35, 55), (75, 17, 40, 22), border_radius=2)
        pygame.draw.polygon(img, (200, 50, 65), [(80, 17), (110, 17), (106, 10), (84, 10)])
        # Bridge window
        pygame.draw.rect(img, (255, 80, 60), (85, 22, 20, 8), border_radius=2)
        pygame.draw.rect(img, (255, 160, 100), (88, 24, 14, 4), border_radius=1)
        # Weapon pods
        pygame.draw.circle(img, (100, 20, 30), (22, 68), 9)
        pygame.draw.circle(img, (200, 55, 70), (22, 68), 6)
        pygame.draw.circle(img, (100, 20, 30), (168, 68), 9)
        pygame.draw.circle(img, (200, 55, 70), (168, 68), 6)
        # Engines
        for ex in [58, 78, 98, 118]:
            pygame.draw.rect(img, (120, 20, 30), (ex, 0, 10, 8), border_radius=2)
            pygame.draw.rect(img, (255, 120, 30), (ex + 2, 1, 6, 5), border_radius=1)
        # Armor lines
        pygame.draw.line(img, (180, 40, 55), (52, 22), (138, 22), 1)
        pygame.draw.line(img, (180, 40, 55), (48, 38), (142, 38), 1)
        # Central cannon
        pygame.draw.rect(img, (120, 30, 20), (90, 92, 10, 28), border_radius=2)
        pygame.draw.rect(img, (220, 70, 30), (91, 94, 8, 24), border_radius=1)
        pygame.draw.polygon(img, (255, 100, 40), [(90, 92), (100, 92), (98, 84), (92, 84)])

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 20
        self.hp = BOSS_MAX_HP
        self.max_hp = BOSS_MAX_HP
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

# ---------------------- Questions ----------------------
questions = [
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/* */", "--"],
        "answer": 1
    },
    {
        "question": "Which of the following is a Python keyword?",
        "options": ["class", "hello", "apple", "cat"],
        "answer": 0
    },
    {
        "question": "What is the output of print(2+2)?",
        "options": ["22", "4", "Error", "None"],
        "answer": 1
    },
    {
        "question": "Which keyword is used to define a function?",
        "options": ["func", "define", "def", "function"],
        "answer": 2
    },
    {
        "question": "Which brackets are used for a list?",
        "options": ["{}", "()", "[]", "<>"],
        "answer": 2
    },
    {
        "question": "What does len('hello') return?",
        "options": ["4", "5", "6", "Error"],
        "answer": 1
    },
    {
        "question": "Which type is immutable in Python?",
        "options": ["list", "dict", "set", "tuple"],
        "answer": 3
    },
    {
        "question": "What does 'break' do in a loop?",
        "options": ["Skip iteration", "Exit loop", "Pause loop", "Restart loop"],
        "answer": 1
    },
    {
        "question": "How do you start an if-else block?",
        "options": ["if x { }", "if (x):", "if x:", "if x then"],
        "answer": 2
    },
    {
        "question": "What is 10 // 3 in Python?",
        "options": ["3.33", "3", "4", "Error"],
        "answer": 1
    },
]

# ---------------------- Game ----------------------
class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.player = Player()
        self.boss = Boss()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)

        self.total_damage = 0
        self.show_question = False
        self.current_question = None
        self.selected_option = 0
        self.win = False

        self.feedback_text = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0

        self.combo = 0
        self.quiz_ready = True
        self.quiz_cooldown = 0

        self.particles = []

        # Star layers: (x, y, speed, brightness, size)
        self.stars = []
        for _ in range(60):
            self.stars.append(self._make_star(1, random.randint(0, SCREEN_HEIGHT)))
        for _ in range(40):
            self.stars.append(self._make_star(2, random.randint(0, SCREEN_HEIGHT)))
        for _ in range(15):
            self.stars.append(self._make_star(3, random.randint(0, SCREEN_HEIGHT)))
        # Nebula blobs
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

    def spawn_particles(self, x, y, color, count=12):
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-4, 1)
            life = random.randint(15, 35)
            size = random.randint(2, 4)
            self.particles.append(Particle(x, y, color, vx, vy, life, size))

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
            twinkle = bri + random.randint(-10, 10)
            twinkle = max(30, min(255, twinkle))
            if sz >= 3:
                pygame.draw.circle(screen, (twinkle, twinkle, twinkle + 20), (int(x), int(y)), 2)
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
        # Top-center: Boss HP (main display)
        bar_w = 400
        bar_x = SCREEN_WIDTH // 2 - bar_w // 2
        boss_hud = pygame.Surface((bar_w + 80, 50), pygame.SRCALPHA)
        pygame.draw.rect(boss_hud, (0, 0, 0, 120), (0, 0, bar_w + 80, 50), border_radius=10)
        screen.blit(boss_hud, (bar_x - 40, 10))

        boss_label = self.font.render("BOSS", True, RED)
        screen.blit(boss_label, (bar_x - 30, 16))
        self.draw_rounded_bar(bar_x + 40, 20, bar_w - 100, 14,
                              max(0, self.boss.hp / self.boss.max_hp),
                              RED, RED_DIM, (120, 30, 35))
        hp_text = self.font.render(f"{max(0, self.boss.hp)}/{self.boss.max_hp}", True, (200, 70, 80))
        screen.blit(hp_text, (bar_x + bar_w - 50, 16))

        # Top-left: damage dealt
        dmg_hud = pygame.Surface((180, 36), pygame.SRCALPHA)
        pygame.draw.rect(dmg_hud, (0, 0, 0, 100), (0, 0, 180, 36), border_radius=8)
        screen.blit(dmg_hud, (10, 10))
        dmg_label = self.small_font.render("DMG", True, TEXT_DIM)
        screen.blit(dmg_label, (22, 18))
        dmg_val = self.font.render(str(self.total_damage), True, CYAN)
        screen.blit(dmg_val, (68, 14))

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
        if self.quiz_ready and not self.show_question and not self.win:
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
        self.current_question = random.choice(questions)
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
            self.feedback_text = f"Wrong! Boss +{heal} HP  (Answer: {correct})"
            self.feedback_color = RED
        self.feedback_timer = 50
        self.show_question = False
        self.quiz_ready = False
        self.quiz_cooldown = 90

        if self.boss.hp <= 0:
            self.win = True

    def draw_question(self):
        if not self.show_question:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        pw, ph = 620, 340
        px = SCREEN_WIDTH // 2 - pw // 2
        py = SCREEN_HEIGHT // 2 - ph // 2

        # Shadow
        shadow = pygame.Surface((pw + 10, ph + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, pw + 10, ph + 10), border_radius=16)
        screen.blit(shadow, (px - 3, py + 3))

        # Panel
        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (*PANEL_BG, 240), (0, 0, pw, ph), border_radius=14)
        screen.blit(panel, (px, py))

        # Header stripe
        header = pygame.Surface((pw, 60), pygame.SRCALPHA)
        pygame.draw.rect(header, (25, 35, 65, 200), (0, 0, pw, 60),
                         border_top_left_radius=14, border_top_right_radius=14)
        screen.blit(header, (px, py))
        pygame.draw.line(screen, ACCENT, (px, py + 60), (px + pw, py + 60), 1)

        q_text = self.font.render(self.current_question["question"], True, WHITE)
        screen.blit(q_text, (px + 28, py + 16))

        for i, opt in enumerate(self.current_question["options"]):
            is_sel = (i == self.selected_option)
            opt_y = py + 80 + i * 56
            opt_rect = pygame.Rect(px + 24, opt_y, pw - 48, 44)

            opt_surf = pygame.Surface((opt_rect.w, opt_rect.h), pygame.SRCALPHA)
            bg = (*OPTION_HOVER, 220) if is_sel else (*OPTION_BG, 180)
            pygame.draw.rect(opt_surf, bg, (0, 0, opt_rect.w, opt_rect.h), border_radius=8)
            screen.blit(opt_surf, opt_rect.topleft)

            if is_sel:
                pygame.draw.rect(screen, ACCENT_LIGHT, opt_rect, 2, border_radius=8)
                # Selection indicator
                pygame.draw.rect(screen, ACCENT_LIGHT, (opt_rect.x, opt_rect.y + 8, 3, 28), border_radius=2)

            label = chr(65 + i)
            label_color = ACCENT_LIGHT if is_sel else TEXT_DIM
            text_color = WHITE if is_sel else (160, 165, 180)
            lt = self.small_font.render(label, True, label_color)
            screen.blit(lt, (opt_rect.x + 16, opt_rect.y + 12))
            ot = self.small_font.render(opt, True, text_color)
            screen.blit(ot, (opt_rect.x + 44, opt_rect.y + 12))

        # Border
        pygame.draw.rect(screen, PANEL_BORDER, (px, py, pw, ph), 1, border_radius=14)

        tip = self.small_font.render("Up / Down  to select     SPACE  to confirm", True, TEXT_DIM)
        screen.blit(tip, (px + pw // 2 - tip.get_width() // 2, py + ph - 32))

    def draw_win(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Glow behind title
        glow_r = 180 + int(30 * math.sin(self.tick * 0.06))
        glow = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (50, 40, 10, 25), (glow_r, glow_r), glow_r)
        screen.blit(glow, (SCREEN_WIDTH // 2 - glow_r, SCREEN_HEIGHT // 2 - 60 - glow_r))

        title = self.title_font.render("VICTORY", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        line = pygame.Surface((300, 2), pygame.SRCALPHA)
        line.fill((*YELLOW, 80))
        screen.blit(line, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 10))

        sub = self.font.render(f"Total Damage: {self.total_damage}", True, WHITE)
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        sub2 = self.small_font.render("Python Master!", True, GREEN)
        screen.blit(sub2, (SCREEN_WIDTH // 2 - sub2.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pulse = int(120 + 60 * math.sin(self.tick * 0.08))
        restart = self.small_font.render("[ R ] Restart     [ ESC ] Quit", True, TEXT_DIM)
        restart.set_alpha(pulse)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        if self.tick % 3 == 0:
            px = SCREEN_WIDTH // 2 + random.randint(-200, 200)
            py = SCREEN_HEIGHT // 2 + random.randint(-60, 60)
            c = random.choice([YELLOW, ORANGE, GREEN, CYAN, ACCENT_LIGHT])
            self.spawn_particles(px, py, c, 2)

    def reset(self):
        self.all_sprites.empty()
        self.projectiles.empty()
        self.particles.clear()
        self.player = Player()
        self.boss = Boss()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)
        self.total_damage = 0
        self.show_question = False
        self.current_question = None
        self.selected_option = 0
        self.win = False
        self.feedback_text = ""
        self.feedback_timer = 0
        self.combo = 0
        self.quiz_ready = True
        self.quiz_cooldown = 0

    def run(self):
        while True:
            clock.tick(FPS)
            self.tick += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if self.win:
                        if event.key == pygame.K_r:
                            self.reset()
                        continue

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

            if not self.win and not self.show_question:
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
            self.all_sprites.draw(screen)
            self.draw_particles()
            self.draw_hud()
            self.draw_feedback()
            self.draw_question()

            if self.win:
                self.draw_win()

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
