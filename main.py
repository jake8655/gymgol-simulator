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
            "question": "Kisova je 2+2?",
            "answers": ["Giovanni Giorgo", "Marcus Aurelius", "Napoleon Bonaparte"],
            "correct": 2,
        },
    ],
    "hladka": [
        {"question": "Hladka je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
    ],
    "horvath": [
        {"question": "Horvath je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
    ],
    "laurinska": [
        {"question": "Kolik je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
        {"question": "Kolik je 2+3?", "answers": ["2", "3", "5"], "correct": 2},
        {"question": "Kolik je 2+4?", "answers": ["6", "3", "8"], "correct": 1},
        {"question": "Kolik je 2+5?", "answers": ["2", "7", "4"], "correct": 2},
        {"question": "Kolik je 2+6?", "answers": ["2", "3", "8"], "correct": 2},
        {"question": "Kolik je 2+7?", "answers": ["2", "0", "4"], "correct": 0},
    ],
    "palenikova": [
        {"question": "Kolik je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
        {"question": "Kolik je 2+3?", "answers": ["2", "3", "5"], "correct": 2},
        {"question": "Kolik je 2+4?", "answers": ["6", "3", "8"], "correct": 1},
        {"question": "Kolik je 2+5?", "answers": ["2", "7", "4"], "correct": 2},
        {"question": "Kolik je 2+6?", "answers": ["2", "3", "8"], "correct": 2},
        {"question": "Kolik je 2+7?", "answers": ["2", "0", "4"], "correct": 0},
    ],
    "zilka": [
        {"question": "Kolik je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
        {"question": "Kolik je 2+3?", "answers": ["2", "3", "5"], "correct": 2},
        {"question": "Kolik je 2+4?", "answers": ["6", "3", "8"], "correct": 1},
        {"question": "Kolik je 2+5?", "answers": ["2", "7", "4"], "correct": 2},
        {"question": "Kolik je 2+6?", "answers": ["2", "3", "8"], "correct": 2},
        {"question": "Kolik je 2+7?", "answers": ["2", "0", "4"], "correct": 0},
    ],
}

pause = False
lost = False
time = 0
multiplier = 10


class LoseText(Sprite):
    def __init__(self, small_font: Font, sprites):
        Sprite.__init__(self)
        font = pygame.font.SysFont("Arial", 50)
        self.text = font.render("Dostal si 5 D:", True, (50, 0, 100))
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
        global lost, pause, time, multiplier
        lost, pause, time, multiplier = False, False, 1, 10
        self.sprites.remove(self)


class Button(Sprite):
    def __init__(self, text: str, correct: bool, font: Font, i: int, teacher, sprites):
        Sprite.__init__(self)
        self.debug = text
        self.text = font.render(text, True, (100, 100, 200))
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
            # Remove unused elements
            # So baaaad
            for _ in range(4):
                if (self.sprites[-1] is not self) and (
                    (type(self.sprites[-1]) is Button) or type(self.sprites[-1]) is Question
                ):
                    self.sprites.remove(self.sprites[-1])
                elif (self.sprites[-2] is not self) and (
                    (type(self.sprites[-2]) is Button) or type(self.sprites[-2]) is Question
                ):
                    self.sprites.remove(self.sprites[-2])
            self.die()
            global pause
            pause = False
        else:
            global lost
            lost = True


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
        self.text = font.render(self.question_text, True, (100, 200, 100))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (WIDTH // 2, HEIGHT - (BUTTONS_PLACE + 20))
        self.dead = False

    def die(self):
        self.dead = True
        self.kill()

    def draw(self, screen: Surface):
        screen.blit(self.text, self.text_rect)


class Teacher(MovingGameObject):
    def __init__(self, image_file: str, sprites, big_font: Font, small_font: Font):
        temp_sprite = pygame.image.load(image_file).get_rect()
        super().__init__(image_file, (randint(0, WIDTH - temp_sprite.width), randint(0, 20)), [0, 2])
        del temp_sprite
        self.dead = False
        self.name = image_file.split("/")[-1].split(".")[0]
        self.sprites = sprites
        self.big_font = big_font
        self.small_font = small_font

    def die(self):
        self.kill()
        self.sprites.remove(self)

    def ask(self):
        global pause
        pause = True
        question = QUESTIONS[self.name][randint(0, len(QUESTIONS[self.name]) - 1)]
        self.sprites.append(Question(question["question"], self.big_font))
        for i in range(3):
            self.sprites.append(
                Button(question["answers"][i], i == question["correct"], self.small_font, i, self, self.sprites)
            )

    def update(self, player_rect: Rect):
        if pause:
            return
        super().update()
        collision = self.rect.colliderect(player_rect)
        if collision:
            self.ask()
        if self.rect.top >= HEIGHT:
            self.die()


class Game:
    def __init__(self):
        pygame.init()

        global time, multiplier
        clock = pygame.time.Clock()
        big_font = pygame.font.SysFont("Arial", 20)
        small_font = pygame.font.SysFont("Arial", 15)
        screen = pygame.display.set_mode(SIZE, 0, 32)
        pygame.display.set_caption("Gymgol Simulator")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

        sprites: list[Union[Player, Teacher, Button, LoseText]] = [
            Player("./assets/sprites/student/student.png"),
        ]

        while True:
            if not pause and not lost:
                time += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    for sprite in sprites:
                        if type(sprite) == Player:
                            sprite.on_key_down(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for sprite in sprites:
                        if type(sprite) == Button or type(sprite) == LoseText:
                            sprite.on_click()

            screen.fill(BACKGROUND_COLOR)

            for sprite in sprites:
                if type(sprite) == Teacher:
                    sprite.update(sprites[0].rect)
                elif type(sprite) == Player or type(sprite) == Button:
                    sprite.update()
                sprite.draw(screen)
                if (type(sprite) == Teacher or type(sprite) == Question) and sprite.dead:
                    sprites.remove(sprite)
                    if multiplier > 2:
                        multiplier -= 1

            pygame.display.flip()
            clock.tick(60)

            if time == 1:
                sprites.append(Teacher("./assets/sprites/teachers/kisova.png", sprites, big_font, small_font))
            if time % (60 * multiplier) == 0:
                sprites.append(
                    Teacher(
                        f"./assets/sprites/teachers/{TEACHERS[randint(0, len(TEACHERS) - 1)]}.png",
                        sprites,
                        big_font,
                        small_font,
                    )
                )

            if lost:
                sprites = []
                sprites.append(LoseText(big_font, sprites))


game = Game()
