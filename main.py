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

    def edge(self, screen):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()

    def move_left(self, key_type):
        if key_type == pygame.K_LEFT:
            self.rect.left = self.rect.left - self.speed[0]

    def move_right(self, key_type):
        if key_type == pygame.K_RIGHT:
            self.rect.left = self.rect.left + self.speed[0]

    def up(self, screen):
        for i in range(3):

            screen.blit(self.image, self.rect)

    def down(self, screen):
        for i in range(3):
            self.rect.top = self.rect.top + self.speed[1]
            screen.blit(self.image, self.rect)

    def jump(self, key_type, screen):
        if key_type == pygame.K_SPACE:
            self.up(screen)


def init():
    pygame.init()
    pygame.key.set_repeat(100, 50)


def make_ball(ball_speed, ball_location):
    ball_image = pygame.image.load("ball.png")
    return Ball(ball_image, ball_speed, ball_location)


def make_dumbo(dumbo_location):
    dumbo_image = pygame.image.load("dumbo_image.png")
    dumbo_speed = [15, 5]
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
        brick = Brick(surface, [35 + col * 140, 40 + row * 80], random.choice([True, False]))
        add_group(bricks, brick)
    return bricks


def check1(dumbo, ball):
    if pygame.sprite.spritecollide(dumbo, pygame.sprite.Group(ball), False):
        ball.speed[1] = -ball.speed[1]


def check2(ball, element, group, points):
    if pygame.sprite.spritecollide(ball, pygame.sprite.Group(element), False):
        ball.speed[1] = -ball.speed[1]
        element.change_color(group)
        points = points + 1
    return points


def change_brick_color(ball, group, points):
    for element in group:
        points = check2(ball, element, group, points)
    return points


def whole_check(group, ball, dumbo, points):
    check1(dumbo, ball)
    points = change_brick_color(ball, group, points)
    return points


def reset(group):
    if not group:
        pygame.time.delay(100)
        group = make_bricks()
    return group


def terminate(event):
    if event.type == pygame.QUIT:
        sys.exit()


def press_key_event(event, dumbo):
    if event.type == pygame.KEYDOWN:
        dumbo.move_left(event.key)
        dumbo.move_right(event.key)


def ending_event(event):
    if 200 <= event.pos[0] <= 312 and 450 <= event.pos[1] <= 484:
        main()
    if 700 <= event.pos[0] <= 773 and 450 <= event.pos[1] <= 484:
        sys.exit()


def press_mouse_event(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        ending_event(event)


def do_event(dumbo):
    for event in pygame.event.get():
        terminate(event)
        press_key_event(event, dumbo)
        press_mouse_event(event)


def show_font(font, string, screen, position):
    ft = font.render(string, True, [0, 0, 0])
    screen.blit(ft, position)


def show_ending(screen, points):
    screen.fill([255, 255, 255])
    font_b = pygame.font.Font(None, 70)
    font_s = pygame.font.Font(None, 50)
    show_font(font_b, "GAME OVER", screen, [350, 100])
    show_font(font_s, "You`r final score : " + str(points), screen, [320, 150])
    show_font(font_s, "AGAIN", screen, [200, 450])
    show_font(font_s, "END", screen, [700, 450])
    return screen


def group_blit(screen, group):
    for element in group:
        screen.blit(element.image, element.rect)


def whole_blit(screen, ball, dumbo, bricks, points):
    font = pygame.font.Font(None, 30)
    show_font(font, "SCORE : " + str(points), screen, [870, 20])
    screen.blit(ball.image, ball.rect)
    screen.blit(dumbo.image, dumbo.rect)
    group_blit(screen, bricks)
    if ball.rect.bottom >= screen.get_height():
        show_ending(screen, points)


def main():
    init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1000, 630])
    ball = make_ball([8, 7], [500, 250])
    dumbo = make_dumbo([500, 510])
    bricks = make_bricks()
    points = 0

    while True:
        screen.fill([255, 255, 255])
        clock.tick(30)

        do_event(dumbo)

        ball.move(screen)
        dumbo.edge(screen)
        points = whole_check(bricks, ball, dumbo, points)
        bricks = reset(bricks)
        whole_blit(screen, ball, dumbo, bricks, points)
        pygame.display.flip()


main()
