import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 300
LANE_WIDTH = WIDTH//8

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('images\Road.jpg'), (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = bg.get_height()
bg_move = 5

player_size = (50, 100)
player = pygame.transform.scale(pygame.image.load('images\Player_Cars\BMW.png'), player_size)
player_rect = pygame.Rect(WIDTH//2, HEIGHT*0.6, *player_size)
player_rect.center = (WIDTH//2, HEIGHT*0.6)

player_move_left = [-5, 0]
player_move_right = [5, 0]

ENEMIES_CARS_PATH = 'images\Traffic\Cars\\'
ENEMIES_BIKES_PATH = 'images\Traffic\Bikes\\'
ENEMIES_CARS_IMAGES = os.listdir(ENEMIES_CARS_PATH)
ENEMIES_BIKES_IMAGES = os.listdir(ENEMIES_BIKES_PATH)
ENEMIES = [[ENEMIES_CARS_PATH+img, (45, 90)] for img in ENEMIES_CARS_IMAGES]
for img in ENEMIES_BIKES_IMAGES:
    ENEMIES.append([ENEMIES_BIKES_PATH+img, (25, 55)])

def create_enemy():
    global enemy_size
    enemy_choice = random.choice(ENEMIES)
    enemy_size = enemy_choice[1]
    enemy = pygame.transform.scale(pygame.image.load(enemy_choice[0]), enemy_size)
    lane = random.choice([1, 3, 5, 7])
    enemy_rect = pygame.Rect(LANE_WIDTH*lane, 0 - enemy_size[1], *enemy_size)
    enemy_rect.center = (LANE_WIDTH*lane, 0 - enemy_size[1])
    return [enemy, enemy_rect]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

playing = True


while playing:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

    bg_y1 += bg_move
    bg_y2 += bg_move

    if bg_y1 >= bg.get_height():
        bg_y1 = -bg.get_height()

    if bg_y2 >= bg.get_height():
        bg_y2 = -bg.get_height()
    
    main_display.blit(bg, (0, bg_y1))
    main_display.blit(bg, (0, bg_y2))

    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        bg_move += 0.1
    if keys[K_DOWN]:
        bg_move -= 0.1

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy_speed = bg_move - 4
        enemy[1].move_ip(0, enemy_speed)
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False
    
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].top > HEIGHT:
            enemies.pop(enemies.index(enemy))