import pygame
from pygame.colordict import THECOLORS
import sys
import random
import os
os.chdir(".\\image")


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, surface, location, displayed):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = surface.convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.displayed = displayed


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self, screen):
        self.rect = self.rect.move(self.speed)
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]


class Dumbo(pygame.sprite.Sprite):
    def __init__(self, image, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self, screen, direction):
        if direction == "left":
            self.rect.left = self.rect.left - self.speed[0]
        elif direction == "right":
            self.rect.left = self.rect.left + self.speed[0]

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()

    def move_left(self, key_type, screen):
        if key_type == pygame.K_LEFT:
            self.move(screen, "left")

    def move_right(self, key_type, screen):
        if key_type == pygame.K_RIGHT:
            self.move(screen, "right")


def init():
    pygame.init()
    pygame.key.set_repeat(100, 50)


def make_ball(ball_speed, ball_location):
    ball_image = pygame.image.load("ball.png")
    return Ball(ball_image, ball_speed, ball_location)


def make_dumbo(dumbo_location):
    dumbo_image = pygame.image.load("dumbo_image.png")
    dumbo_speed = [15, 0]
    return Dumbo(dumbo_image, dumbo_speed, dumbo_location)


def make_bricks():
    bricks = pygame.sprite.Group()
    color_dic = {3: "indianred4", 2: "indianred3", 1: "darksalmon"}
    surface = pygame.Surface([90, 30])
    for row in range(3):
        for col in range(7):
            brick = Brick(THECOLORS[color_dic[3]], surface, [35 + col * 140, 30 + row * 80],
                          random.choice([True, False]))
            if brick.displayed:
                bricks.add(brick)
    return bricks


def brick_blit(screen, group):
    for elt in group:
        screen.blit(elt.image, elt.rect)


def check2(target1, target2, displayed, ball):
    if pygame.sprite.spritecollide(target1, target2, displayed):
        ball.speed[1] = -ball.speed[1]


def check(group, ball, dumbo):
    check2(ball, group, True, ball)
    check2(dumbo, pygame.sprite.Group(ball), False, ball)


def terminate(event):
    if event.type == pygame.QUIT:
        sys.exit()


def press_key_event(event, dumbo, screen):
    if event.type == pygame.KEYDOWN:
        dumbo.move_left(event.key, screen)
        dumbo.move_right(event.key, screen)


def do_event(screen, dumbo):
    for event in pygame.event.get():
        terminate(event)
        press_key_event(event, dumbo, screen)


def main():
    init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1000, 630])
    ball = make_ball([10, 10], [500, 320])
    dumbo = make_dumbo([500, 510])
    bricks = make_bricks()
    while True:
        screen.fill([255, 255, 255])
        clock.tick(30)

        do_event(screen, dumbo)

        ball.move(screen)
        check(bricks, ball, dumbo)
        screen.blit(ball.image, ball.rect)
        screen.blit(dumbo.image, dumbo.rect)
        brick_blit(screen, bricks)
        pygame.display.flip()


main()
