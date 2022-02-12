import pygame
import os
os.chdir("C:\\Users\\박예은\\PycharmProjects\\pythonProject\\BrickBreaking\\image")


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

def ex():
    pygame.init()
    screen = pygame.display.set_mode([1000, 640])
    screen.fill([255, 255, 255])
    image = pygame.image.load("ball.png")
    ball = Ball(image, [10, 10], [100, 100])
    screen.blit(ball.image, ball.rect)
    pygame.display.flip()
    return ball

while True:
    ball = ex()