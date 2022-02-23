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

    def change_color(self):
        if self.color == INDIANRED3:
            self.color = DARKSALMON
        if self.color == INDIANRED4:
            self.color = INDIANRED3
        self.image.fill(self.color)

    def is_darksalmon(self):
        return self.color == DARKSALMON


class Bricks(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def add_brick(self, brick):
        if brick.displayed:
            self.add(brick)

    def delete_brick(self, brick):
        if brick.is_darksalmon():
            self.remove(brick)


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

    def move_left(self, key_type):
        if key_type == pygame.K_LEFT:
            self.rect.left = self.rect.left - self.speed[0]

    def move_right(self, key_type):
        if key_type == pygame.K_RIGHT:
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


class Status:
    def __init__(self, is_end, is_game_over):
        self.of_end = is_end
        self.of_game_over = is_game_over

    def change_end(self, end):
        self.of_end = end

    def change_game_over(self, game_over):
        self.of_game_over = game_over


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


def make_bricks():
    bricks = Bricks()
    surface = pygame.Surface([90, 30])
    num_list1 = [0, 1, 2] * 7
    num_list2 = [0, 1, 2, 3, 4, 5, 6] * 3
    for row, col in zip(num_list1, num_list2):
        brick_color = random.choice([INDIANRED4, INDIANRED3, DARKSALMON])
        brick_location = [35 + col * 140, 40 + row * 80]
        brick = Brick(brick_color, surface, brick_location, random.choice([True, False]))
        bricks.add_brick(brick)
    return bricks


def check_ball_and_bricks(ball, brick, bricks, points):
    if pygame.sprite.spritecollide(ball, pygame.sprite.Group(brick), False):
        ball.speed[1] = -ball.speed[1]
        bricks.delete_brick(brick)
        brick.change_color()
        points = points + 1
    return points


def change_brick_color(ball, bricks, points):
    for brick in bricks:
        points = check_ball_and_bricks(ball, brick, bricks, points)
    return points


def reset(group):
    if not group:
        pygame.time.delay(100)
        group = make_bricks()
    return group


def end_program(event, current):
    if event.type == pygame.QUIT:
        current.change_end(False)


def press_space_key(key_type, dumbo):
    if key_type == pygame.K_SPACE and not dumbo.speed[1]:
        dumbo.change_y_speed(10)


def press_key_event(event, dumbo):
    if event.type == pygame.KEYDOWN:
        dumbo.move_left(event.key)
        dumbo.move_right(event.key)
        press_space_key(event.key, dumbo)


def click_again_and_end(pos, current):
    again_rect = pygame.Rect(200, 450, 112, 34)
    end_rect = pygame.Rect(700, 450, 73, 34)
    if pygame.Rect.collidepoint(again_rect, pos):
        main()
    if pygame.Rect.collidepoint(end_rect, pos):
        current.change_end(False)


def show_or_not(current, pos):
    if current.of_game_over:
        click_again_and_end(pos, current)


def press_mouse_event(event, current):
    if event.type == pygame.MOUSEBUTTONDOWN:
        show_or_not(current, event.pos)


def do_event(dumbo, current):
    for event in pygame.event.get():
        end_program(event, current)
        press_key_event(event, dumbo)
        press_mouse_event(event, current)


def blit_font(font, string, screen, position):
    ft = font.render(string, True, [0, 0, 0])
    screen.blit(ft, position)


def show_ending(ball, screen, current, points):
    if ball.rect.bottom >= screen.get_height():
        current.change_game_over(True)
        screen.fill([255, 255, 255])
        font_b = pygame.font.Font(None, 70)
        font_s = pygame.font.Font(None, 50)
        blit_font(font_b, "GAME OVER", screen, [350, 100])
        blit_font(font_s, "You`r final score : " + str(points), screen, [320, 150])
        blit_font(font_s, "AGAIN", screen, [200, 450])
        blit_font(font_s, "END", screen, [700, 450])
    return screen


def blit_group(screen, group):
    for element in group:
        screen.blit(element.image, element.rect)


def blit_all(screen, ball, dumbo, bricks, points):
    font = pygame.font.Font(None, 30)
    blit_font(font, "SCORE : " + str(points), screen, [870, 20])
    screen.blit(ball.image, ball.rect)
    screen.blit(dumbo.image, dumbo.rect)
    blit_group(screen, bricks)


def main():
    init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1000, 630])
    ball = make_ball([8, 7], [500, 250])
    dumbo = make_dumbo([500, 500])
    bricks = make_bricks()
    points = 0
    current = Status(True, False)

    while current.of_end:
        screen.fill([255, 255, 255])
        clock.tick(30)

        do_event(dumbo, current)
        ball.move(screen, dumbo)
        dumbo.move_updown()
        dumbo.hit_edge(screen)
        points = change_brick_color(ball, bricks, points)
        bricks = reset(bricks)
        blit_all(screen, ball, dumbo, bricks, points)
        screen = show_ending(ball, screen, current, points)
        pygame.display.flip()


main()
