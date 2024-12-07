import sys

import pygame
from pygame.locals import *

from config import *

pygame.init()
screen = pygame.display.set_mode((1280, 720), RESIZABLE, DOUBLEBUF)

clock = pygame.time.Clock()
clock.tick(FPS)
running = True

TILE_WIDTH = 32  # Уменьшенная ширина
TILE_HEIGHT = 16  # Уменьшенная высота
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Загрузка ассетов
stone_tile = pygame.image.load("assets/floor/SmoothStone.png").convert_alpha()
water_tile = pygame.image.load("assets/floor/Water.png").convert_alpha()


# Пример карты: 0 — трава, 1 — вода
map_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

]


# Функция отрисовки тайла
def draw_tile(screen, x, y, tile_type):
    if tile_type == 0:
        screen.blit(stone_tile, (x - TILE_WIDTH // 2, y - TILE_HEIGHT // 2))
    elif tile_type == 1:
        screen.blit(water_tile, (x - TILE_WIDTH // 2, y - TILE_HEIGHT // 2))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Рисуем карту с ассетами
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            tile_x = 400 + (col - row) * TILE_WIDTH // 2
            tile_y = 100 + (col + row) * TILE_HEIGHT // 2
            draw_tile(screen, tile_x, tile_y, map_data[row][col])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
