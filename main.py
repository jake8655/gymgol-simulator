import sys, pygame
from random import randint
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

SIZE = WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = 200, 100, 100
BUTTONS_PLACE = 150

TEACHERS = ["kisova", "hladka", "horvath", "laurinska", "palenikova", "zilka"]
QUESTIONS = {
    "kisova": [
        {"question": "Kolik je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
        {"question": "Kolik je 2+3?", "answers": ["2", "3", "5"], "correct": 2},
        {"question": "Kolik je 2+4?", "answers": ["6", "3", "8"], "correct": 1},
        {"question": "Kolik je 2+5?", "answers": ["2", "7", "4"], "correct": 2},
        {"question": "Kolik je 2+6?", "answers": ["2", "3", "8"], "correct": 2},
        {"question": "Kolik je 2+7?", "answers": ["9", "0", "4"], "correct": 0},
    ],
    "hladka": [
        {"question": "Kolik je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
        {"question": "Kolik je 2+3?", "answers": ["2", "3", "5"], "correct": 2},
        {"question": "Kolik je 2+4?", "answers": ["6", "3", "8"], "correct": 1},
        {"question": "Kolik je 2+5?", "answers": ["2", "7", "4"], "correct": 2},
        {"question": "Kolik je 2+6?", "answers": ["2", "3", "8"], "correct": 2},
        {"question": "Kolik je 2+7?", "answers": ["2", "0", "4"], "correct": 0},
    ],
    "horvath": [
        {"question": "Kolik je 2+2?", "answers": ["2", "3", "4"], "correct": 2},
        {"question": "Kolik je 2+3?", "answers": ["2", "3", "5"], "correct": 2},
        {"question": "Kolik je 2+4?", "answers": ["6", "3", "8"], "correct": 1},
        {"question": "Kolik je 2+5?", "answers": ["2", "7", "4"], "correct": 2},
        {"question": "Kolik je 2+6?", "answers": ["2", "3", "8"], "correct": 2},
        {"question": "Kolik je 2+7?", "answers": ["2", "0", "4"], "correct": 0},
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


class Button(Sprite):
    def __init__(self, image_file: str, position: tuple[int, int], question: dict):
        Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(x=position[0], y=position[1])
        self.question = question

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)

    def check_click(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        # Also check for click (key event)
        return self.rect.collidepoint(mouse_pos)


class MovingGameObject(Sprite):
    def __init__(self, image_file: str, position: tuple[int, int], speed: list[int]):
        Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(x=position[0], y=position[1])
        self.speed = speed

    def update(self):
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


class Teacher(MovingGameObject):
    def __init__(self, image_file: str):
        temp_sprite = pygame.image.load(image_file).get_rect()
        super().__init__(image_file, (randint(0, WIDTH - temp_sprite.width), randint(0, 20)), [0, 2])
        del temp_sprite
        self.dead = False
        self.name = image_file.split("/")[-1].split(".")[0]

    def die(self):
        self.dead = True
        self.kill()

    def ask(self):
        pass

    def update(self, player_rect: Rect):
        super().update()
        collision = self.rect.colliderect(player_rect)
        if collision:
            self.ask()
        if self.rect.top >= HEIGHT:
            self.die()


class Game:
    def __init__(self):
        pygame.init()

        time = 0
        multiplier = 10
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SIZE, 0, 32)
        pygame.display.set_caption("Gymgol Simulator")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

        self.sprites = [Player("./assets/sprites/student/student.png"), Teacher("./assets/sprites/teachers/kisova.png")]

        while True:
            time += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    for sprite in self.sprites:
                        if hasattr(sprite, "on_key_down"):
                            sprite.on_key_down(event.key)

            self.screen.fill(BACKGROUND_COLOR)

            for sprite in self.sprites:
                if hasattr(sprite, "dead"):
                    sprite.update(self.sprites[0].rect)
                else:
                    sprite.update()
                sprite.draw(self.screen)
                if hasattr(sprite, "dead") and sprite.dead:
                    self.sprites.remove(sprite)
                    if multiplier > 2:
                        multiplier -= 1

            pygame.display.flip()
            clock.tick(60)

            if time % (60 * multiplier) == 0:
                self.sprites.append(Teacher(f"./assets/sprites/teachers/{TEACHERS[randint(0, len(TEACHERS) - 1)]}.png"))


game = Game()
