import pygame
import sys
import os
os.chdir(".\\image")


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

    def updown(self, num):
        self.rect.top = self.rect.top - self.speed[num]


def init():
    pygame.init()
    pygame.key.set_repeat(100, 50)


def make_dumbo(dumbo_location):
    dumbo_image = pygame.image.load("dumbo_image.png")
    dumbo_speed = [15, 10]
    return Dumbo(dumbo_image, dumbo_speed, dumbo_location)


def terminate(event):
    if event.type == pygame.QUIT:
        sys.exit()


def change_sign(num):
    num = - num



def press_key_event(event, dumbo):
    if event.type == pygame.KEYDOWN:
        dumbo.move_left(event.key)
        dumbo.move_right(event.key)


def do_event(dumbo, screen):
    for event in pygame.event.get():
        terminate(event)
        press_key_event(event, dumbo)


def jump1(dumbo):
    held_space = False
    if dumbo.rect.top >= 450:
        dumbo.rect.top = dumbo.rect.top - dumbo.speed[1]
    if dumbo.rect.top < 450:
        held_space = False
    elif dumbo.rect.top == 630:
        held_space = True
    return held_space


def jump2(dumbo):
    if dumbo.rect.top <= 630:
        dumbo.speed[1] = - dumbo.speed[1]
        dumbo.rect.top = dumbo.rect.top + dumbo.speed[1]


def main():
    init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1000, 630])
    dumbo = make_dumbo([500, 510])

    while True:
        screen.fill([255, 255, 255])
        clock.tick(30)

        do_event(dumbo, screen)

        dumbo.edge(screen)

        screen.blit(dumbo.image, dumbo.rect)
        pygame.display.flip()


main()
