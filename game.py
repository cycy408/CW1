import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Quiz Battle - Answer to Attack!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
PURPLE = (150, 0, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
DARK_GREEN = (0, 160, 0)

clock = pygame.time.Clock()
FPS = 60
WIN_SCORE = 50

# ---------------------- Player ----------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (30, 90, 210),
            [(30, 0), (22, 18), (18, 32), (20, 48), (40, 48), (42, 32), (38, 18)])
        pygame.draw.polygon(self.image, (20, 70, 180),
            [(22, 22), (0, 44), (4, 48), (20, 36)])
        pygame.draw.polygon(self.image, (20, 70, 180),
            [(38, 22), (60, 44), (56, 48), (40, 36)])
        pygame.draw.ellipse(self.image, (100, 200, 255), (25, 10, 10, 14))
        pygame.draw.rect(self.image, (80, 200, 255), (23, 46, 5, 4))
        pygame.draw.rect(self.image, (80, 200, 255), (32, 46, 5, 4))
        pygame.draw.line(self.image, (50, 120, 240), (30, 3), (30, 44), 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
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

# ---------------------- Boss ----------------------
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((180, 120), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (160, 20, 40),
            [(90, 115), (35, 45), (25, 25), (45, 5), (135, 5), (155, 25), (145, 45)])
        pygame.draw.polygon(self.image, (130, 10, 30),
            [(35, 45), (5, 75), (10, 85), (15, 80), (45, 55)])
        pygame.draw.polygon(self.image, (130, 10, 30),
            [(145, 45), (175, 75), (170, 85), (165, 80), (135, 55)])
        pygame.draw.rect(self.image, (200, 40, 60), (70, 15, 40, 25))
        pygame.draw.polygon(self.image, (220, 60, 80),
            [(75, 15), (105, 15), (100, 8), (80, 8)])
        pygame.draw.circle(self.image, (200, 60, 80), (20, 65), 7)
        pygame.draw.circle(self.image, (200, 60, 80), (160, 65), 7)
        for ex in [55, 75, 95, 115]:
            pygame.draw.rect(self.image, (255, 100, 20), (ex, 0, 8, 6))
        pygame.draw.line(self.image, (200, 50, 60), (50, 20), (130, 20), 2)
        pygame.draw.line(self.image, (200, 50, 60), (45, 40), (135, 40), 2)
        pygame.draw.rect(self.image, (255, 80, 0), (86, 90, 8, 25))
        pygame.draw.polygon(self.image, (255, 120, 30),
            [(86, 90), (94, 90), (92, 80), (88, 80)])
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 30
        self.hp = 10
        self.max_hp = 10
        self.speed = 3
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

# ---------------------- Bomb ----------------------
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        pygame.draw.circle(self.image, WHITE, (10, 10), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

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
        self.bombs = pygame.sprite.Group()

        self.player = Player()
        self.boss = Boss()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)

        self.score = 0
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

        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                       random.choice([1, 2, 3])) for _ in range(120)]

        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 60)

    def draw_background(self):
        screen.fill(BLACK)
        for i, (x, y, speed) in enumerate(self.stars):
            brightness = 100 + speed * 50
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), speed // 2 + 1)
            new_y = y + speed
            if new_y > SCREEN_HEIGHT:
                self.stars[i] = (random.randint(0, SCREEN_WIDTH), 0, random.choice([1, 2, 3]))
            else:
                self.stars[i] = (x, new_y, speed)

    def draw_boss_hp(self):
        bar_width = 200
        bar_height = 16
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 155
        fill = max(0, (self.boss.hp / self.boss.max_hp) * bar_width)
        pygame.draw.rect(screen, (80, 0, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, RED, (bar_x, bar_y, fill, bar_height))
        label = self.small_font.render("BOSS", True, RED)
        screen.blit(label, (bar_x - 50, bar_y - 2))

    def draw_score_bar(self):
        bar_width = 200
        bar_height = 16
        bar_x = 20
        bar_y = 55
        fill = min(self.score / WIN_SCORE, 1.0) * bar_width
        pygame.draw.rect(screen, (0, 40, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, (0, 50, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, DARK_GREEN, (bar_x, bar_y, fill, bar_height))
        label = self.small_font.render(f"{self.score}/{WIN_SCORE}", True, GREEN)
        screen.blit(label, (bar_x + bar_width + 10, bar_y - 2))

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        self.draw_score_bar()
        self.draw_boss_hp()

        if self.combo >= 2:
            combo_text = self.small_font.render(f"Combo x{self.combo}!", True, YELLOW)
            screen.blit(combo_text, (SCREEN_WIDTH - 160, 20))

        if self.quiz_ready and not self.show_question and not self.win:
            hint = self.small_font.render("Press SPACE to answer a question", True, (100, 100, 100))
            screen.blit(hint, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT - 30))

    def draw_feedback(self):
        if self.feedback_timer > 0:
            alpha = min(255, self.feedback_timer * 6)
            text = self.font.render(self.feedback_text, True, self.feedback_color)
            text.set_alpha(alpha)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            self.feedback_timer -= 1

    def new_question(self):
        self.current_question = random.choice(questions)
        self.show_question = True
        self.selected_option = 0

    def check_answer(self):
        if self.selected_option == self.current_question["answer"]:
            self.combo += 1
            bonus = 10 + (self.combo - 1) * 2
            self.score += bonus
            self.feedback_text = f"Correct! +{bonus} pts"
            self.feedback_color = GREEN
            bomb = Bomb(self.player.rect.centerx, self.player.rect.top)
            self.all_sprites.add(bomb)
            self.bombs.add(bomb)
        else:
            self.combo = 0
            penalty = min(self.score, 5)
            self.score -= penalty
            correct = self.current_question["options"][self.current_question["answer"]]
            self.feedback_text = f"Wrong! -{penalty} pts  (Answer: {correct})"
            self.feedback_color = RED
        self.feedback_timer = 45
        self.show_question = False
        self.quiz_ready = False
        self.quiz_cooldown = 90

        if self.score >= WIN_SCORE:
            self.win = True

    def draw_question(self):
        if not self.show_question:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        panel_w, panel_h = 600, 320
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
        pygame.draw.rect(screen, (20, 20, 40), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, BLUE, (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        q_text = self.font.render(self.current_question["question"], True, WHITE)
        screen.blit(q_text, (panel_x + 30, panel_y + 30))

        for i, opt in enumerate(self.current_question["options"]):
            is_selected = (i == self.selected_option)
            bg_color = (40, 60, 100) if is_selected else (20, 20, 40)
            text_color = YELLOW if is_selected else (180, 180, 180)
            opt_y = panel_y + 90 + i * 50
            pygame.draw.rect(screen, bg_color, (panel_x + 30, opt_y, panel_w - 60, 40), border_radius=6)
            if is_selected:
                pygame.draw.rect(screen, BLUE, (panel_x + 30, opt_y, panel_w - 60, 40), 2, border_radius=6)
            label = chr(65 + i)
            opt_text = self.small_font.render(f"  {label}. {opt}", True, text_color)
            screen.blit(opt_text, (panel_x + 40, opt_y + 8))

        tip = self.small_font.render("Up/Down to select  |  SPACE to confirm", True, (100, 140, 200))
        screen.blit(tip, (panel_x + panel_w // 2 - tip.get_width() // 2, panel_y + panel_h - 40))

    def draw_win(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))

        win_text = self.big_font.render("YOU WIN!", True, YELLOW)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        sub = self.font.render(f"Final Score: {self.score}  |  Python Master!", True, GREEN)
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        restart = self.small_font.render("Press R to restart  |  ESC to quit", True, (150, 150, 150))
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def reset(self):
        self.all_sprites.empty()
        self.bombs.empty()
        self.player = Player()
        self.boss = Boss()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)
        self.score = 0
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

                hits = pygame.sprite.spritecollide(self.boss, self.bombs, True)
                for hit in hits:
                    self.boss.hp -= 1

                if self.quiz_cooldown > 0:
                    self.quiz_cooldown -= 1
                    if self.quiz_cooldown <= 0:
                        self.quiz_ready = True

            self.draw_background()
            self.all_sprites.draw(screen)
            self.draw_hud()
            self.draw_feedback()
            self.draw_question()

            if self.win:
                self.draw_win()

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
