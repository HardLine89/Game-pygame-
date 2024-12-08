import pygame
from pygame.locals import *
import config
from entities.hero import Hero
from utils import draw_tile, scale_tile_image, scale_background

pygame.init()
screen = pygame.display.set_mode(
    (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), RESIZABLE, DOUBLEBUF
)

clock = pygame.time.Clock()
running = True

# Загрузка ассетов
stone_tile = pygame.image.load("assets/floor/SmoothStone.png").convert_alpha()
water_tile = pygame.image.load("assets/floor/Water.png").convert_alpha()
wall_tile = pygame.image.load("assets/wall/Brick.png").convert_alpha()
player_sprite = pygame.image.load("assets/player/Soldier-Idle.png").convert_alpha()
background_image = pygame.image.load("assets/CavePixelArt.png").convert_alpha()

# Пример карты: 0 - земля, 1 - вода, 2 - стена
map_data = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
player_pos = [5, 0]
# Основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == VIDEORESIZE:

            width = min(config.MAXWIDTH, max(config.MINWIDTH, event.w))
            height = min(config.MAXHEIGHT, max(config.MINHEIGHT, event.h))

            if (width, height) != event.size:
                screen = pygame.display.set_mode((width, height), RESIZABLE)
        elif event.type == KEYDOWN:  # Управление персонажем
            if event.key == K_w:  # Вверх
                if (
                    player_pos[0] > 0
                    and map_data[player_pos[0] - 1][player_pos[1]] != 2
                ):
                    player_pos[0] -= 1
            elif event.key == K_s:  # Вниз
                if (
                    player_pos[0] < len(map_data) - 1
                    and map_data[player_pos[0] + 1][player_pos[1]] != 2
                ):
                    player_pos[0] += 1
            elif event.key == K_a:  # Влево
                if (
                    player_pos[1] > 0
                    and map_data[player_pos[0]][player_pos[1] - 1] != 2
                ):
                    player_pos[1] -= 1
            elif event.key == K_d:  # Вправо
                if (
                    player_pos[1] < len(map_data[0]) - 1
                    and map_data[player_pos[0]][player_pos[1] + 1] != 2
                ):
                    player_pos[1] += 1

    # Масштабируем ассеты в зависимости от размера окна
    stone_tile, water_tile, wall_tile, player_sprite = (
        scale_tile_image(image)
        for image in (stone_tile, water_tile, wall_tile, player_sprite)
    )
    # background = scale_background(screen.get_width(), screen.get_height())
    background = scale_background(screen.get_width(), screen.get_height(), background_image)

    # Расчет смещения для центрирования карты по экрану
    offset_x = screen.get_width() // 2
    offset_y = (screen.get_height() - config.MAP_HEIGHT) // 2

    screen.blit(background, (0, 0))  # Отображаем фон
    tile_images = {0: stone_tile, 1: water_tile, 2: wall_tile}  # Земля  # Вода  # Стена

    # Рисуем карту с ассетами
    for row in range(config.GRID_HEIGHT):
        for col in range(config.GRID_WIDTH):
            tile_x = offset_x + (col - row) * config.TILE_WIDTH // 2
            tile_y = offset_y + (col + row) * config.TILE_HEIGHT // 2
            tile_type = map_data[row][col]
            tile_image = tile_images[tile_type]
            draw_tile(screen, tile_x, tile_y, tile_image, tile_type)
    player_x = offset_x + (player_pos[1] - player_pos[0]) * config.TILE_WIDTH // 2
    player_y = offset_y + (player_pos[1] + player_pos[0]) * config.TILE_HEIGHT // 2
    screen.blit(
        player_sprite,
        (player_x - config.TILE_WIDTH // 2, player_y - config.TILE_HEIGHT * 2),
    )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
