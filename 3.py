import pygame
from pygame.colordict import THECOLORS
import sys
import random
import os
os.chdir(".\\image")


class Brick(pygame.sprite.Sprite):
    def __init__(self, color_num, color, surface, location, displayed, clash):
        pygame.sprite.Sprite.__init__(self)
        self.num = color_num
        self.color = THECOLORS[color]
        self.image = surface.convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.displayed = displayed
        self.clash = clash

    def change_col(self):
        if self.clash and self.num > 0:
            self.num = self.num - 1


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


def init(ball_speed, ball_location, dumbo_location):
    pygame.init()
    pygame.key.set_repeat(100, 50)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1000, 630])
    screen.fill([255, 255, 255])
    ball_image = pygame.image.load("ball.png")
    ball = Ball(ball_image, ball_speed, ball_location)
    dumbo_image = pygame.image.load("dumbo_image.png")
    dumbo_speed = [15, 0]
    dumbo = Dumbo(dumbo_image, dumbo_speed, dumbo_location)
    bricks = pygame.sprite.Group()
    color_dic = {3: "indianred4", 2: "indianred3", 1: "darksalmon"}
    color_num = 3
    surface = pygame.Surface([90, 30])
    for row in range(3):
        for col in range(7):
            brick = Brick(color_num, color_dic[color_num], surface,
                          [35+col*140, 30+row*80], random.choice([True, False]), None)
            if brick.displayed:
                bricks.add(brick)

    my_list = [screen, ball, dumbo, bricks, clock]

    return my_list


def brick_blit(screen, group):
    for elt in group:
        screen.blit(elt.image, elt.rect)


def check_bnb(group, ball):
    for elt in group:
        if pygame.sprite.spritecollide(ball, pygame.sprite.Group(elt), False):
            ball.speed[1] = -ball.speed[1]
            elt.clash = True
            elt.change_col()



def check_bnd(ball, dumbo):
    if pygame.sprite.spritecollide(dumbo, pygame.sprite.Group(ball), False):
        ball.speed[1] = -ball.speed[1]


def event(screen, dumbo):
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            sys.exit()
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_LEFT:
                dumbo.move(screen, "left")
            elif evt.key == pygame.K_RIGHT:
                dumbo.move(screen, "right")


def main():
    global game_list
    screen = game_list[0]
    ball = game_list[1]
    dumbo = game_list[2]
    bricks = game_list[3]
    clock = game_list[4]
    clock.tick(30)
    screen.fill([255, 255, 255])

    event(screen, dumbo)

    ball.move(screen)
    check_bnb(bricks, ball)
    check_bnd(ball, dumbo)
    screen.blit(ball.image, ball.rect)
    screen.blit(dumbo.image, dumbo.rect)
    brick_blit(screen, bricks)
    pygame.display.flip()


game_list = init([10, 10], [500, 320], [500, 510])
while True:
    main()
