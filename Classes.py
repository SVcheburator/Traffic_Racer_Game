import pygame


class Background:
    def __init__(self,image, width, height) -> None:
        self.img = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.bg_y1 = 0
        self.bg_y2 = self.img.get_height()
        self.speed = 2
    
    def move(self):
        self.bg_y1 += self.speed
        self.bg_y2 += self.speed

        if self.bg_y1 >= self.img.get_height():
            self.bg_y1 = -self.img.get_height()

        if self.bg_y2 >= self.img.get_height():
            self.bg_y2 = -self.img.get_height()


class Player:
    def __init__(self, img, pl_width, pl_height, screen_width, screen_height) -> None:
        self.size = (pl_width, pl_height)
        self.img = pygame.transform.scale(pygame.image.load(img), self.size)
        self.rect = pygame.Rect(screen_width//2, screen_height*0.6, *self.size)
        self.rect.center = (screen_width//2, screen_height*0.7)
        self.move_left = [-1.7, 0]
        self.move_right = [1.7, 0]


class Enemy:
    def __init__(self, rand_enemy, lane, lane_width) -> None:
        self.rand_enemy = rand_enemy
        self.lane = lane
        self.size = self.rand_enemy[1]
        self.img = pygame.transform.scale(pygame.image.load(self.rand_enemy[0]), self.size)
        self.rect = pygame.Rect(lane_width*self.lane, 0 - self.size[1], *self.size)
        self.rect.center = (lane_width*self.lane, 0 - self.size[1])