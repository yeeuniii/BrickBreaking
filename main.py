import pygame
import random
THECOLORS = pygame.colordict.THECOLORS
INDIANRED4 = THECOLORS["indianred4"]
INDIANRED3 = THECOLORS["indianred3"]
DARKSALMON = THECOLORS["darksalmon"]


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, surface, location, displayed):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = surface.convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.displayed = displayed

    def change_color(self, color):
        self.color = color
        self.image.fill(self.color)

    def is_indianred4(self):
        return self.color == INDIANRED4

    def is_indianred3(self):
        return self.color == INDIANRED3

    def is_darksalmon(self):
        return self.color == DARKSALMON


class Bricks(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.reset()
        self.broken_number = 0

    def make(self):
        surface = pygame.Surface([90, 30])
        row_list = [0, 1, 2] * 7
        col_list = [0, 1, 2, 3, 4, 5, 6] * 3
        for row, col in zip(row_list, col_list):
            brick_color = random.choice([INDIANRED4, INDIANRED3, DARKSALMON])
            brick_location = [35 + col * 140, 40 + row * 80]
            brick = Brick(brick_color, surface, brick_location, random.choice([True, False]))
            self.add_brick(brick)

    def add_brick(self, brick):
        if brick.displayed:
            self.add(brick)

    def hit_brick(self, brick):
        if brick.is_darksalmon():
            self.remove(brick)
        if brick.is_indianred3():
            brick.change_color(DARKSALMON)
        if brick.is_indianred4():
            brick.change_color(INDIANRED3)
        self.broken_number += 1

    def reset(self):
        if not self:
            self.make()

    def blit_group(self, screen):
        for element in self:
            screen.blit(element.image, element.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self, screen, dumbo):
        self.rect = self.rect.move(self.speed)
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        if pygame.sprite.spritecollide(dumbo, pygame.sprite.Group(self), False):
            self.speed[1] = -self.speed[1]

    def is_visible(self, screen):
        return self.rect.bottom < screen.get_height()


class Dumbo(pygame.sprite.Sprite):
    def __init__(self, image, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def hit_edge(self, screen):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()

    def move_left(self):
        self.rect.left = self.rect.left - self.speed[0]

    def move_right(self):
        self.rect.left = self.rect.left + self.speed[0]

    def change_y_speed(self, speed):
        self.speed[1] = speed

    def move_updown(self):
        self.rect.top = self.rect.top - self.speed[1]
        if self.rect.top < 450:
            self.rect.top = 450
            self.speed[1] = - self.speed[1]
        if self.rect.bottom == 630:
            self.speed[1] = 0

    def is_not_jumping(self):
        return self.speed[1] == 0


def init():
    pygame.init()
    pygame.key.set_repeat(100, 50)


def make_ball(ball_speed, ball_location):
    ball_image = pygame.image.load("./image/ball.png")
    return Ball(ball_image, ball_speed, ball_location)


def make_dumbo(dumbo_location):
    dumbo_image = pygame.image.load("./image/dumbo_image.png")
    dumbo_speed = [15, 0]
    return Dumbo(dumbo_image, dumbo_speed, dumbo_location)


def check_ball_and_bricks(ball, bricks):
    for brick in pygame.sprite.spritecollide(ball, bricks, False):
        ball.speed[1] = -ball.speed[1]
        bricks.hit_brick(brick)
        bricks.reset()


def press_space_key(key, dumbo):
    if key[pygame.K_SPACE] and dumbo.is_not_jumping():
        dumbo.change_y_speed(10)


def press_left_key(key, dumbo):
    if key[pygame.K_LEFT]:
        dumbo.move_left()


def press_right_key(key, dumbo):
    if key[pygame.K_RIGHT]:
        dumbo.move_right()


def press_key_event(dumbo):
    key = pygame.key.get_pressed()
    press_left_key(key, dumbo)
    press_right_key(key, dumbo)
    press_space_key(key, dumbo)


def click_again():
    clicked = pygame.event.get(pygame.MOUSEBUTTONDOWN)
    pos = pygame.mouse.get_pos()
    if pygame.Rect.collidepoint(pygame.Rect(200, 450, 112, 34), pos) and clicked:
        main()


def not_click_end():
    clicked = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    return not (pygame.Rect.collidepoint(pygame.Rect(700, 450, 73, 34), pos) and clicked[0])


def blit_font(font, string, screen, position):
    ft = font.render(string, True, [0, 0, 0])
    screen.blit(ft, position)


def show_ending(screen, point):
    screen.fill([255, 255, 255])
    font_b = pygame.font.Font(None, 70)
    font_s = pygame.font.Font(None, 50)
    blit_font(font_b, "GAME OVER", screen, [350, 100])
    blit_font(font_s, "You`r final score : " + str(point), screen, [320, 150])
    blit_font(font_s, "AGAIN", screen, [200, 450])
    blit_font(font_s, "END", screen, [700, 450])


def blit_all(screen, ball, dumbo, bricks):
    font = pygame.font.Font(None, 30)
    blit_font(font, "SCORE : " + str(bricks.broken_number), screen, [870, 20])
    screen.blit(ball.image, ball.rect)
    screen.blit(dumbo.image, dumbo.rect)
    bricks.blit_group(screen)


def terminate():
    if bool(pygame.event.get(pygame.QUIT)):
        quit()


def play(ball, screen, clock, dumbo, bricks):
    while ball.is_visible(screen):
        terminate()
        screen.fill([255, 255, 255])
        clock.tick(30)
        press_key_event(dumbo)
        ball.move(screen, dumbo)
        dumbo.move_updown()
        dumbo.hit_edge(screen)
        check_ball_and_bricks(ball, bricks)
        blit_all(screen, ball, dumbo, bricks)
        pygame.display.flip()


def do_again(screen, bricks):
    show_ending(screen, bricks.broken_number)
    pygame.display.flip()
    while not_click_end():
        terminate()
        click_again()


def main():
    init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1000, 630])
    ball = make_ball([8, 7], [500, 250])
    dumbo = make_dumbo([500, 500])
    bricks = Bricks()

    play(ball, screen, clock, dumbo, bricks)
    do_again(screen, bricks)


main()
