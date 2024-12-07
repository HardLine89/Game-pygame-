import pygame
from pygame.locals import *
import config

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


# Масштабируем тайлы в зависимости от размера окна
def scale_tile_images():
    stone_tile_scaled = pygame.transform.scale(
        stone_tile, (config.TILE_WIDTH, config.TILE_WIDTH)
    )
    water_tile_scaled = pygame.transform.scale(
        water_tile, (config.TILE_WIDTH, config.TILE_WIDTH)
    )
    wall_tile_scaled = pygame.transform.scale(
        wall_tile, (config.TILE_WIDTH, config.TILE_WIDTH)
    )
    player_sprite_scaled = pygame.transform.scale(
        player_sprite, (config.TILE_WIDTH, config.TILE_WIDTH)
    )
    return stone_tile_scaled, water_tile_scaled, wall_tile_scaled, player_sprite_scaled


def scale_background(screen_width, screen_height):
    background_scaled = pygame.transform.scale(
        background_image, (screen_width, screen_height)
    )
    return background_scaled


# Функция отрисовки тайла
def draw_tile(screen_obj, x, y, tile_type):
    if tile_type == 0:
        screen_obj.blit(
            stone_tile, (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT // 2)
        )
    elif tile_type == 1:
        screen_obj.blit(
            water_tile, (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT // 2)
        )
    elif tile_type == 2:  # Тайл стены
        screen_obj.blit(
            wall_tile, (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT // 2)
        )
        for i in range(4):  # Количество слоев стены
            screen_obj.blit(
                wall_tile,
                (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT * (0.5 + i)),
            )


# Пример карты: 0 — трава, 1 — вода
map_data = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
                if player_pos[0] > 0 and map_data[player_pos[0] - 1][player_pos[1]] != 2:
                    player_pos[0] -= 1
            elif event.key == K_s:  # Вниз
                if player_pos[0] < len(map_data) - 1 and map_data[player_pos[0] + 1][player_pos[1]] != 2:
                    player_pos[0] += 1
            elif event.key == K_a:  # Влево
                if player_pos[1] > 0 and map_data[player_pos[0]][player_pos[1] - 1] != 2:
                    player_pos[1] -= 1
            elif event.key == K_d:  # Вправо
                if player_pos[1] < len(map_data[0]) - 1 and map_data[player_pos[0]][player_pos[1] + 1] != 2:
                    player_pos[1] += 1
    # Масштабируем ассеты в зависимости от размера окна
    stone_tile, water_tile, wall_tile, player_sprite = scale_tile_images()
    background = scale_background(screen.get_width(), screen.get_height())

    # Расчет смещения для центрирования карты по экрану
    map_width = config.GRID_WIDTH * config.TILE_WIDTH
    map_height = config.GRID_HEIGHT * config.TILE_HEIGHT
    offset_x = screen.get_width() // 2
    offset_y = (screen.get_height() - map_height) // 2

    screen.blit(background, (0, 0))  # Отображаем фон

    # Рисуем карту с ассетами
    for row in range(config.GRID_HEIGHT):
        for col in range(config.GRID_WIDTH):
            tile_x = offset_x + (col - row) * config.TILE_WIDTH // 2
            tile_y = offset_y + (col + row) * config.TILE_HEIGHT // 2
            draw_tile(screen, tile_x, tile_y, map_data[row][col])
    player_x = offset_x + (player_pos[1] - player_pos[0]) * config.TILE_WIDTH // 2
    player_y = offset_y + (player_pos[1] + player_pos[0]) * config.TILE_HEIGHT // 2
    screen.blit(player_sprite, (player_x - config.TILE_WIDTH // 2, player_y - config.TILE_HEIGHT * 2))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
