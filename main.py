import pygame
import sys
import random
import os
os.chdir(".\\image")
# 상대참조와 절대참조
# os.chdir("C:\\Users\\박예은\\PycharmProjects\\pythonProject\\BrickBreaking\\image")


class Brick(pygame.sprite.Sprite):
    def __init__(self, chance, location, boolean):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.Surface([90, 30])   # Brick size
        color = {3: "indianred4", 2: "indianred3", 1: "darksalmon"}
        self.chance = chance
        self.color = color[self.chance]
        image.fill(pygame.colordict.THECOLORS[self.color])
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.boolean = boolean


class Ball(pygame.sprite.Sprite):   # Marker
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


class Dumbo(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def dead_end(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()

    def jump(self):
        pygame.draw.rect(screen, [255, 255, 255], self.rect, 0)
        self.rect.top = self.rect.top - self.speed[1]
        screen.blit(self.image, self.rect)

    def down(self):
        pygame.draw.rect(screen, [255, 255, 255], self.rect, 0)
        self.rect.top = self.rect.top + self.speed[1]
        screen.blit(self.image, self.rect)


def animate(group):
    for i in group:
        screen.blit(i.image, i.rect)


def check(group, ball):
    for i in group:
        if pygame.sprite.spritecollide(ball, pygame.sprite.Group(i), True):
            ball.speed[1] = -ball.speed[1]
            rect = i.rect.left, i.rect.top
            chance = i.chance
            if chance > 1:
                new_brick = Brick(chance-1, rect, True)
                brick_group.add(new_brick)

pygame.init()
screen = pygame.display.set_mode([1000, 630])
screen.fill([255, 255, 255])

ball_speed = [random.randint(8, 10), random.randint(5, 10)]
my_ball = Ball("ball.png", ball_speed, screen.get_rect().center)   # ball 객체 생성
# main_image = pygame.image.load("dumbo_image.png")
# main = Ball("dumbo_image.png", None,
# [screen.get_width()/2, screen.get_height()-main_image.get_height()])
# 우선 이미지의 높이를 안다는 전제하에. 근데 모른다면? 어떻게 할지 더 생각해보기
main = Dumbo("dumbo_image.png", [15, 30], [screen.get_width()/2, screen.get_height()-130])    # main 객체 생성


def makebricks():
    groups = pygame.sprite.Group()
    for row in range(3):
        for col in range(7):
            brick_TF = random.choice([True, False])
            brick = Brick(random.choice([1, 2, 3]), [35+col*140, 30+row*80], brick_TF)
            if brick.boolean:
                groups.add(brick)
    return groups


brick_group = makebricks()
clock = pygame.time.Clock()
delay = 100
interval = 50
pygame.key.set_repeat(delay, interval)  # 연속 키


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
            elif event.key == pygame.K_SPACE:
                main.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_loc = event.pos
            held_down = True


    main.dead_end()
    my_ball.move()
    if pygame.sprite.spritecollide(main, pygame.sprite.Group(my_ball), False):
        my_ball.speed[1] = -my_ball.speed[1]

    screen.blit(main.image, main.rect)
    screen.blit(my_ball.image, my_ball.rect)
    animate(brick_group)
    check(brick_group, my_ball)

    if my_ball.rect.top >= screen.get_height():
        screen.fill([255, 255, 255])
        font1 = pygame.font.Font(None, 90)
        ft1 = font1.render("GAME   OVER", True, [0, 0, 0])
        font2 = pygame.font.Font(None, 70)
        ft2 = font2.render("restart", True, [0, 0, 0])
        ft3 = font2.render("end", True, [0, 0, 0])
        screen.blit(ft1, [(screen.get_width() - ft1.get_width()) / 2, 100])
        screen.blit(ft2, [screen.get_width() / 4 - ft2.get_width() / 2, 450])
        screen.blit(ft3, [screen.get_width() / 4 * 3 - ft3.get_width() / 2, 450])
        pygame.display.flip()
        if screen.get_width() / 4 - ft2.get_width() / 2 <= mouse_loc[0] \
                <= screen.get_width() / 4 + ft2.get_width() / 2 and \
                400 <= mouse_loc[1] <= 400 + ft2.get_height():
            brick_group = makebricks()
        elif screen.get_width() / 4 * 3 - ft3.get_width() / 2 <= mouse_loc[0] \
                <= screen.get_width() / 4 * 3 + ft3.get_width() / 2 and \
                400 <= mouse_loc[1] <= 400 + ft3.get_height():
            sys.exit()

    if len(brick_group) == 0:
        pygame.time.delay(1000)
        brick_group = makebricks()

    pygame.display.flip()

