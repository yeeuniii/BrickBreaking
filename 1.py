import pygame
import sys
import random
import os
os.chdir("C:\\Users\\박예은\\AppData\\Local\\Programs\\Python\\Python37\\One_Big_Archive")


class Ball(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0 or self.rect.bottom >= screen.get_height():
            self.speed[1] = -self.speed[1]


def animate(group):
    for ball in group:
        ball.move()
        screen.blit(ball.image, ball.rect)


pygame.init()
screen = pygame.display.set_mode([1000, 630])
screen.fill([255, 255, 255])
image = "beach_ball.png"
group = pygame.sprite.Group()
control = Ball(image, None, screen.get_rect().center)
for i in range(3):
    ball_speed = [random.randint(8, 10), random.randint(5, 10)]
    ball_location = [random.randint(0, 500), random.randint(0, 300)]
    ball = Ball(image, ball_speed, ball_location)
    group.add(ball)
clock = pygame.time.Clock()

while True:
    clock.tick(20)
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            control.rect.center = pygame.mouse.get_pos()
            pygame.sprite.spritecollide(control, group, True)
    pygame.sprite.spritecollide(control, group, True)
    screen.blit(control.image, control.rect)
    animate(group)
    pygame.display.flip()
