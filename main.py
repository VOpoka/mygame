import random
import os
import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

HEIGTH = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

FPS = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGTH))

bg = pygame.transform.scale(pygame.image.load(
    'background.png'), (WIDTH, HEIGTH))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale(pygame.image.load(
    'player.png'), (160, 100))
player_size = player.get_size()
player_rect = player.get_rect(midleft=(0, random.randint(100, 500)))
player_move_down = [0, 4]
player_move_left = [-5, 0]
player_move_up = [0, -4]
player_move_right = [4, 0]


def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy = pygame.transform.scale(pygame.image.load(
        'enemy.png'), (100, 40))
    enemy_size = enemy.get_size()
    enemy_rect = pygame.Rect(WIDTH, random.randint(-20, 500), *enemy_size)
    enemy_move = [random.randint(-7, -3), 0]
    return [enemy, enemy_rect, enemy_move]


CREATE_ENEMY = pygame.USEREVENT+1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []


def create_prize():
    prize = pygame.image.load('bonus.png').convert_alpha()
    prize = pygame.transform.scale(pygame.image.load(
        'bonus.png'), (130, 140))
    prize_size = prize.get_size()
    prize_rect = pygame.Rect(random.randint(0, WIDTH-50), 50, *prize_size)
    prize_move = [0, random.randint(4, 8)]
    return [prize, prize_rect, prize_move]


CREATE_PRIZE = pygame.USEREVENT+2
pygame.time.set_timer(CREATE_PRIZE, 1900)
prizeies = []

CHANGE_IMAGE = pygame.USEREVENT+3
pygame.time.set_timer(CHANGE_IMAGE, 200)

score = 0
image_index = 0

playing = True
while playing:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_PRIZE:
            prizeies.append(create_prize())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(
                IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_x1 -= bg_move
    bg_x2 -= bg_move
    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGTH:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    main_display.blit(FONT.render(str(score), True,
                      COLOR_BLUE), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for prize in prizeies:
        prize[1] = prize[1].move(prize[2])
        main_display.blit(prize[0], prize[1])

        if player_rect.colliderect(prize[1]):
            score += 1
            prizeies.pop(prizeies.index(prize))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for prize in prizeies:
        if prize[1].bottom < 0:
            prizeies.pop(prizeies.index(prize))
