import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from Classes import Background, Player, Enemy

pygame.init()

# Constants
FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 300
LANE_WIDTH = WIDTH//8

ENEMIES_CARS_PATH = 'images\Traffic\Cars\\'
ENEMIES_BIKES_PATH = 'images\Traffic\Bikes\\'
ENEMIES_CARS_IMAGES = os.listdir(ENEMIES_CARS_PATH)
ENEMIES_BIKES_IMAGES = os.listdir(ENEMIES_BIKES_PATH)
ENEMIES = [[ENEMIES_CARS_PATH+img, (45, 90)] for img in ENEMIES_CARS_IMAGES]
for img in ENEMIES_BIKES_IMAGES:
    ENEMIES.append([ENEMIES_BIKES_PATH+img, (25, 55)])


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

# Variables
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

background = Background(image='images\Road.jpg', width=WIDTH, height=HEIGHT)

player = Player(img='images\Player_Cars\BMW.png', pl_width=50, pl_height=100,screen_width=WIDTH , screen_height=HEIGHT)

enemies = []

# Functions
def event_parser(playing):
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

        if event.type == CREATE_ENEMY:
            new_enemy = Enemy(rand_enemy=random.choice(ENEMIES), lane=random.choice([1, 3, 5, 7]), lane_width=LANE_WIDTH)
            enemies.append(new_enemy)

    return playing

def pressed_keys_parser():
    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        background.speed += 0.01

    if keys[K_DOWN]:
        background.speed -= 0.03

    if keys[K_RIGHT] and player.rect.right < WIDTH:
        player.rect = player.rect.move(player.move_right)
    
    if keys[K_LEFT] and player.rect.left > 0:
        player.rect = player.rect.move(player.move_left)

def enemies_func(playing):
    for enemy in enemies:
        enemy_speed = background.speed - 2
        enemy.rect.move_ip(0, enemy_speed)
        main_display.blit(enemy.img, enemy.rect)

        if player.rect.colliderect(enemy.rect):
            playing = False

        for enemy in enemies:
            if enemy.rect.top > HEIGHT:
                enemies.pop(enemies.index(enemy))

    return playing

# Main function
def mainloop():
    playing = True

    while playing:
        FPS.tick(240)
        
        playing = event_parser(playing)

        background.move()
        
        main_display.blit(background.img, (0, background.bg_y1))
        main_display.blit(background.img, (0, background.bg_y2))

        pressed_keys_parser()

        playing = enemies_func(playing)
        
        main_display.blit(player.img, player.rect)

        pygame.display.flip()

if __name__ == '__main__':
    mainloop()