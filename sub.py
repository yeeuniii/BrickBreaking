import sys
import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, location, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = location
        self.speed = speed

    def move(self):
        self.rect.move(self.speed)


class Game:
    def __init__(self, ball, group):
        self.ball = ball
        self.group = group

    def do_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def make_group(self):
        group = pygame.sprite.Group()
        for element in group:
            element = Ball()
