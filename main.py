import sys, pygame
from random import randint
from pygame.sprite import Sprite
from pygame.surface import Surface

size = width, height = 800, 600
background_color = 200, 100, 100
buttons_place = 150


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
        sprite_height = pygame.image.load(image_file).get_rect().height
        super().__init__(image_file, (0, height - (sprite_height + buttons_place)), [0, 0])
        del sprite_height

    def update(self):
        super().update()
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > width:
                self.rect.right = width

    def on_key_down(self, key: int):
        if key == pygame.K_LEFT:
            self.speed[0] = -5
        if key == pygame.K_RIGHT:
            self.speed[0] = 5


class Teacher(MovingGameObject):
    def __init__(self, image_file: str):
        sprite_width = pygame.image.load(image_file).get_rect().width
        super().__init__(image_file, (randint(0, width - sprite_width), randint(0, 20)), [0, 5])
        del sprite_width
        self.dead = False

    def update(self):
        super().update()
        if not self.dead and self.rect.bottom >= (height - buttons_place):
            self.dead = True
            self.kill()


class Game:
    def __init__(self):
        pygame.init()

        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption("Gymgol Simulator")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

        self.sprites = [Player("./assets/intro_ball.gif"), Teacher("./assets/intro_ball.gif")]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    for sprite in self.sprites:
                        if hasattr(sprite, "on_key_down"):
                            sprite.on_key_down(event.key)

            self.screen.fill(background_color)

            for sprite in self.sprites:
                sprite.update()
                sprite.draw(self.screen)
                if hasattr(sprite, "dead") and sprite.dead:
                    self.sprites.remove(sprite)

            pygame.display.flip()
            clock.tick(60)


game = Game()
