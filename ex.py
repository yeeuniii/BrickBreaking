import pygame
import sys
import random
import os
os.chdir("C:\\Users\\박예은\\PycharmProjects\\pythonProject\\BrickBreaking\\image")


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, location, boolean):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.Surface([90, 30])   # Brick size
        image.fill(color)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.boolean = boolean


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
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]


def animate(group, ball=None):
    for i in group:
        screen.blit(i.image, i.rect)
    if pygame.sprite.spritecollide(ball, group, True):
        my_ball.speed[1] = -my_ball.speed[1]


pygame.init()
screen = pygame.display.set_mode([1000, 630])
screen.fill([255, 255, 255])

ball_speed = [random.randint(8, 10), random.randint(5, 10)]
my_ball = Ball("ball.png", ball_speed, screen.get_rect().center)   # ball 객체 생성
# main_image = pygame.image.load("dumbo_image.png")
# main = Ball("dumbo_image.png", None,
# [screen.get_width()/2, screen.get_height()-main_image.get_height()])
# 우선 이미지의 높이를 안다는 전제하에. 근데 모른다면? 어떻게 할지 더 생각해보기
main = Ball("dumbo_image.png", [15, 0], [screen.get_width()/2, screen.get_height()-130])    # main 객체 생성


brick_group = pygame.sprite.Group()   # 벽돌 그룹 생성
for row in range(3):                    # 벽돌 객체 생성 후 그룹에 넣음
    for col in range(7):
        col_brick = pygame.colordict.THECOLORS["firebrick4"]
        brick = Brick(col_brick, [35+col*140, 30+row*80], random.choice([True, False]))
        if brick.boolean:
            brick_group.add(brick)
#        ball_speed = [random.randint(8, 10), random.randint(5, 10)]
#        ball_location = [random.randint(0, 500), random.randint(0, 300)]
#        ball = Ball(image_file, ball_speed, ball_location)
#        group.add(ball)

clock = pygame.time.Clock()
delay = 100
interval = 50
pygame.key.set_repeat(delay, interval)

while True:
    clock.tick(20)
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                main.rect.left = main.rect.left - main.speed[0]
            elif event.key == pygame.K_RIGHT:
                main.rect.left = main.rect.left + main.speed[0]
    my_ball.move()
    if pygame.sprite.spritecollide(main, pygame.sprite.Group(my_ball), False):
        my_ball.speed[1] = -my_ball.speed[1]
    screen.blit(main.image, main.rect)
    screen.blit(my_ball.image, my_ball.rect)
    animate(brick_group, my_ball)
    pygame.display.flip()
