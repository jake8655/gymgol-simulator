import sys, pygame
from typing import Union
from random import randint
from pygame.font import Font
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

SIZE = WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = 200, 100, 100
BUTTONS_PLACE = 150

TEACHERS = ["kisova", "hladka", "horvath", "laurinska", "palenikova", "zilka"]
QUESTIONS = {
    "kisova": [
        {
            "question": "Čo je kultúra?",
            "answers": [
                "Systém uznávaných hodnôt",
                "Prvá matka vied",
                "Veda skúmajúca poznatky o kráse",
            ],
            "correct": 0,
        },
        {
            "question": "Čo je gýč?",
            "answers": [
                "Navoňaná zdochlina",
                "Najvzácnejšie umenie",
                "Hudobný nástroj",
            ],
            "correct": 0,
        },
        {
            "question": "Čo je kalokagatia?",
            "answers": [
                "Všestranne rozvinutý človek",
                "Uctievanie boha",
                "Umelecké dielo",
            ],
            "correct": 0,
        },
    ],
    "hladka": [
        {"question": "Čo je H2SO4?", "answers": ["kys. sírová", "kys. siričitá", "kys. uhličitá"], "correct": 0},
        {"question": "Akú hodnotu má mólový objem? (dm3/mol)", "answers": ["22.41", "222.41", "2.241"], "correct": 0},
        {
            "question": "Ako sa zapíše roztok v termochémii?",
            "answers": ["aqua (aq)", "solidus (s)", "gaseus (g)"],
            "correct": 0,
        },
    ],
    "horvath": [
        {
            "question": 'Čo je výstupom tohto kódu? print("cislo: " + 2 + 2)',
            "answers": ["Error", "cislo: 4", "cislo: 22"],
            "correct": 0,
        },
        {
            "question": "Ktorý je najviac používaný operačný systém?",
            "answers": ["Linux", "Windows", "MacOS"],
            "correct": 0,
        },
        {
            "question": "Ako vytvoríme cyklus v Pythone?",
            "answers": ["for", "if", "with"],
            "correct": 0,
        },
    ],
    "laurinska": [
        {
            "question": "Ako je správne vzorec (a+b)^2",
            "answers": ["a^2 + 2ab + b^2", "a^2 + b^2", "a^2 - 2ab + b^2"],
            "correct": 0,
        },
        {
            "question": "Aká je monotónnosť funkcie? y=3",
            "answers": ["konštantná", "rastúca", "klesajúca"],
            "correct": 0,
        },
        {
            "question": "Ktorý je anulovaný tvar kvadratickej rovnice?",
            "answers": ["ax^2 + bx + c = 0", "bx^2 + ax + c = 0", "ax^2 + bx = c"],
            "correct": 0,
        },
    ],
    "palenikova": [
        {"question": "Ktorý z týchto je oceán?", "answers": ["Indický", "Beringov", "Japonský"], "correct": 0},
        {"question": "Slimák patrí medzi:", "answers": ["Mäkkýše", "Ploskavce", "Cicavce"], "correct": 0},
        {"question": "Ktorý z týchto sa nachádza v Európe?", "answers": ["Volga", "Amazonka", "Ob"], "correct": 0},
    ],
    "zilka": [
        {"question": "Ako sa robia kľuky?", "answers": ["Normálne", "V aute", "Vo vzduchu"], "correct": 0},
        {
            "question": "Kto vyhral majstrovstvá sveta vo futbale?",
            "answers": ["Argentína", "Francúzsko", "USA"],
            "correct": 0,
        },
        {"question": "Koľko treba pravideľne meškať na hodinu (min)", "answers": ["15", "0", "45"], "correct": 0},
    ],
}

pause = False
lost = False
time = 0
multiplier = 10
timer = 0
score = 0


class Background(Sprite):
    def __init__(self, image_file: str):
        Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        # self.rect.width, self.rect.height = WIDTH, HEIGHT


class Timer(Sprite):
    def __init__(self, font: Font):
        Sprite.__init__(self)
        self.font = font

    def draw(self, screen: Surface):
        global timer
        self.text = self.font.render(f"Čas: {str(7 - round(timer / 60, 1))[:3]}", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.x, self.rect.y = 20, 20
        screen.blit(self.text, self.rect)


class Score(Sprite):
    def __init__(self, font: Font):
        Sprite.__init__(self)
        self.font = font

    def draw(self, screen: Surface):
        global score
        self.text = self.font.render(f"Vyhnutí učitelia: {score}", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.x, self.rect.y = WIDTH - self.rect.width - 20, 20
        screen.blit(self.text, self.rect)


class LoseText(Sprite):
    def __init__(self, small_font: Font, sprites, big_font: Font):
        Sprite.__init__(self)
        font = pygame.font.SysFont("Arial", 50)
        self.text = font.render("Dostal si 5 D:", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.retry_text = small_font.render("Skúsiť znovu", True, (50, 0, 100))
        self.retry_box = Rect(
            WIDTH // 2 - self.retry_text.get_width() // 2,
            HEIGHT // 2 + 50,
            self.retry_text.get_width() + 20,
            self.retry_text.get_height() + 20,
        )
        self.sprites = sprites
        self.big_font = big_font

    def draw(self, screen: Surface):
        screen.blit(self.text, self.rect)
        pygame.draw.rect(screen, (100, 200, 100), self.retry_box, 0, 10)
        screen.blit(self.retry_text, (self.retry_box.x + 10, self.retry_box.y + 10))

    def on_click(self):
        if not self.retry_box.collidepoint(pygame.mouse.get_pos()):
            return
        for sprite in self.sprites:
            if type(sprite) != LoseText:
                self.sprites.remove(sprite)
        self.sprites.append(Player("./assets/sprites/student/student.png"))
        self.sprites.append(Score(self.big_font))
        global lost, pause, time, multiplier, score
        lost, pause, time, multiplier, score = False, False, 1, 10, 0
        self.sprites.remove(self)


class Button(Sprite):
    def __init__(self, text: str, correct: bool, font: Font, i: int, teacher, sprites, set_sprites):
        Sprite.__init__(self)
        self.debug = text
        self.text = font.render(text, True, (50, 0, 100))
        text_rect = self.text.get_rect()
        self.rect = Rect(
            # Center the buttons
            # So baaaad
            50 if i == 0 else WIDTH // 2 - text_rect.width // 2 if i == 1 else WIDTH - (50 + text_rect.width + 20),
            HEIGHT - BUTTONS_PLACE + 50,
            text_rect.width + 20,
            text_rect.height + 20,
        )
        self.correct = correct
        self.teacher = teacher
        self.sprites = sprites
        self.set_sprites = set_sprites

    def die(self):
        self.kill()
        self.sprites.remove(self)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, (100, 200, 100), self.rect, 0, 10)
        screen.blit(self.text, (self.rect.x + 10, self.rect.y + 10))

    def on_click(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return
        if self.correct:
            self.teacher.die()
            self.set_sprites(
                [
                    sprite
                    for sprite in self.sprites
                    if type(sprite) is not Question and type(sprite) is not Button and type(sprite) is not Timer
                ]
            )
            self.die()
            global pause, timer, multiplier
            timer = 0
            pause = False
            if multiplier > 2:
                multiplier -= 1
        else:
            global lost
            lost, multiplier = True, 10


class MovingGameObject(Sprite):
    def __init__(self, image_file: str, position: tuple[int, int], speed: list[int]):
        Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(x=position[0], y=position[1])
        self.speed = speed

    def update(self):
        if not pause:
            self.rect = self.rect.move(self.speed)

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)


class Player(MovingGameObject):
    def __init__(self, image_file: str):
        temp_sprite = pygame.image.load(image_file).get_rect()
        super().__init__(
            image_file, ((WIDTH // 2) - temp_sprite.width, HEIGHT - BUTTONS_PLACE - temp_sprite.height), [0, 0]
        )
        del temp_sprite
        self.direction = 1

    def set_direction(self, direction: int):
        if direction != self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction

    def update(self):
        super().update()
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]
            self.set_direction(-self.direction)
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

    def on_key_down(self, key: int):
        if key == pygame.K_LEFT:
            self.set_direction(-1)
            self.speed[0] = -5
        if key == pygame.K_RIGHT:
            self.set_direction(1)
            self.speed[0] = 5


class Question(Sprite):
    def __init__(self, question_text: str, font: Font):
        Sprite.__init__(self)
        self.question_text = question_text
        self.text = font.render(self.question_text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (WIDTH // 2, HEIGHT - (BUTTONS_PLACE + 20))
        self.dead = False

    def die(self):
        self.dead = True
        self.kill()

    def draw(self, screen: Surface):
        screen.blit(self.text, self.text_rect)


class Teacher(MovingGameObject):
    def __init__(self, image_file: str, sprites, big_font: Font, small_font: Font, set_sprites):
        temp_sprite = pygame.image.load(image_file).get_rect()
        super().__init__(image_file, (randint(0, WIDTH - temp_sprite.width), randint(0, 20)), [0, 2])
        del temp_sprite
        self.dead = False
        self.name = image_file.split("/")[-1].split(".")[0]
        self.sprites = sprites
        self.big_font = big_font
        self.small_font = small_font
        self.set_sprites = set_sprites

    def die(self):
        self.kill()
        self.sprites.remove(self)

    def ask(self):
        global pause
        pause = True
        question = QUESTIONS[self.name][randint(0, len(QUESTIONS[self.name]) - 1)]
        answers = [ans for ans in question["answers"]]
        self.sprites.append(Question(question["question"], self.big_font))
        for i in range(3):
            answer = answers[randint(0, len(answers) - 1)]
            self.sprites.append(
                Button(
                    answer,
                    question["answers"].index(answer) == question["correct"],
                    self.small_font,
                    i,
                    self,
                    self.sprites,
                    self.set_sprites,
                )
            )
            answers.remove(answer)

    def update(self, player_rect: Rect):
        if pause:
            return
        super().update()
        collision = self.rect.colliderect(player_rect)
        if collision:
            self.ask()
        if self.rect.top >= HEIGHT:
            global score, multiplier
            score += 1
            if multiplier > 2:
                multiplier -= 1
            self.die()


class Game:
    def __init__(self):
        pygame.init()

        global time, multiplier, timer, lost, pause
        clock = pygame.time.Clock()
        big_font = pygame.font.SysFont("Arial", 20)
        small_font = pygame.font.SysFont("Arial", 15)
        screen = pygame.display.set_mode(SIZE, 0, 32)
        pygame.display.set_caption("Gymgol Simulator")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
        bg = Background("./assets/background.png")

        self.sprites: list[Union[Player, Teacher, Button, LoseText, Timer, Score]] = [
            Player("./assets/sprites/student/student.png"),
            Score(big_font),
        ]

        self.set_sprites = lambda new_sprites: setattr(self, "sprites", new_sprites)

        while True:
            if not pause and not lost:
                time += 1
            if pause and not lost:
                timer_sprite = [x for x in self.sprites if type(x) == Timer]
                if len(timer_sprite) == 0:
                    self.sprites.append(Timer(big_font))
                timer += 1
            if timer == 60 * 7:
                timer_sprite = [x for x in self.sprites if type(x) == Timer][0]
                self.sprites.remove(timer_sprite)
                timer = 0
                lost = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    for sprite in self.sprites:
                        if type(sprite) == Player:
                            sprite.on_key_down(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for sprite in self.sprites:
                        if type(sprite) == Button or type(sprite) == LoseText:
                            sprite.on_click()

            screen.fill(BACKGROUND_COLOR)
            screen.blit(bg.image, bg.rect)

            for sprite in self.sprites:
                if type(sprite) == Teacher:
                    sprite.update(self.sprites[0].rect)
                elif type(sprite) == Player or type(sprite) == Button:
                    sprite.update()
                sprite.draw(screen)
                if (type(sprite) == Teacher or type(sprite) == Question) and sprite.dead:
                    self.sprites.remove(sprite)
                    if multiplier > 2:
                        multiplier -= 1

            pygame.display.flip()
            clock.tick(60)

            if time == 1:
                self.sprites.append(
                    Teacher(
                        "./assets/sprites/teachers/kisova.png", self.sprites, big_font, small_font, self.set_sprites
                    )
                )
            if time % (60 * multiplier) == 0:
                self.sprites.append(
                    Teacher(
                        f"./assets/sprites/teachers/{TEACHERS[randint(0, len(TEACHERS) - 1)]}.png",
                        self.sprites,
                        big_font,
                        small_font,
                        self.set_sprites,
                    )
                )

            if lost:
                self.sprites = []
                self.sprites.append(LoseText(big_font, self.sprites, big_font))


game = Game()
