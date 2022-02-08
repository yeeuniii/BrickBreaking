import pygame
import sys
import random
import os
os.chdir("C:\\Users\\박예은\\PycharmProjects\\pythonProject\\BrickBreaking\\image")


pygame.init()
screen = pygame.display.set_mode([1000, 630])
screen.fill([255, 255, 255])
image_file = pygame.image.load("ddumbo.png")
screen.blit(image_file, [screen.get_width()/2, screen.get_height()-image_file.get_height()])
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()