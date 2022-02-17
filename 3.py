import pygame
from pygame.colordict import THECOLORS
import sys
import random
import os
os.chdir(".\\image")


class Brick(pygame.sprite.Sprite):
    def __init__(self, surface, location, displayed):
        pygame.sprite.Sprite.__init__(self)
        self.color = THECOLORS[random.choice(["indianred4", "indianred3", "darksalmon"])]
        self.image = surface.convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.displayed = displayed

    def change_color(self, group):
        if self.color == THECOLORS["indianred4"]:
            self.color = THECOLORS["indianred3"]
        elif self.color == THECOLORS["indianred3"]:
            self.color = THECOLORS["darksalmon"]
        else:
            group.remove(self)
        self.image.fill(self.color)


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


def add_group(group, element):
    if element.displayed:
        group.add(element)


def make_bricks():
    bricks = pygame.sprite.Group()
    surface = pygame.Surface([90, 30])
    num_list1 = [0, 1, 2] * 7
    num_list2 = [0, 1, 2, 3, 4, 5, 6] * 3
    ordered_pair = []
    for row, col in zip(num_list1, num_list2):
        ordered_pair.append((row, col))
        brick = Brick(surface, [35 + col * 140, 30 + row * 80], random.choice([True, False]))
        add_group(bricks, brick)
    return bricks


def brick_blit(screen, group):
    for element in group:
        screen.blit(element.image, element.rect)


def check1(dumbo, ball):
    if pygame.sprite.spritecollide(dumbo, pygame.sprite.Group(ball), False):
        ball.speed[1] = -ball.speed[1]


def check2(ball, element, group):
    if pygame.sprite.spritecollide(ball, pygame.sprite.Group(element), False):
        ball.speed[1] = -ball.speed[1]
        element.change_color(group)


def change_brick_color(ball, group):
    for element in group:
        check2(ball, element, group)


def whole_check(group, ball, dumbo):
    check1(dumbo, ball)
    change_brick_color(ball, group)


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
    ball = make_ball([random.randint(6, 9), random.randint(5, 8)], [500, 320])
    dumbo = make_dumbo([500, 510])
    bricks = make_bricks()
    while True:
        screen.fill([255, 255, 255])
        clock.tick(30)

        do_event(screen, dumbo)

        ball.move(screen)
        whole_check(bricks, ball, dumbo)
        screen.blit(ball.image, ball.rect)
        screen.blit(dumbo.image, dumbo.rect)
        brick_blit(screen, bricks)
        pygame.display.flip()


main()
