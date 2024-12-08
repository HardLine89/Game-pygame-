import pygame
from pygame.locals import *
import config
from entities.hero import Hero
from utils import draw_tile, scale_tile_image, scale_background, is_point_in_rhombus

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
# Создаем героя перед циклом
character = Hero(
    5,
    0,
    action_points=10000,
    width=config.TILE_WIDTH,
    height=config.TILE_HEIGHT,
    image_path="assets/player/Soldier-Idle.png",
)
player_pos = [character.x, character.y]
tile_rects = {}

while running:
    offset_x = screen.get_width() // 2
    offset_y = (screen.get_height() - config.MAP_HEIGHT) // 2
    player_x = offset_x + (player_pos[1] - player_pos[0]) * config.TILE_WIDTH // 2
    player_y = offset_y + (player_pos[1] + player_pos[0]) * config.TILE_HEIGHT // 2
    tile_centers = {}

    for row in range(config.GRID_HEIGHT):
        for col in range(config.GRID_WIDTH):
            # Расчет координат центра каждого тайла
            tile_x = offset_x + (col - row) * config.TILE_WIDTH // 2
            tile_y = offset_y + (col + row) * config.TILE_HEIGHT // 2
            tile_centers[(row, col)] = (tile_x, tile_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == VIDEORESIZE:
            width = min(config.MAXWIDTH, max(config.MINWIDTH, event.w))
            height = min(config.MAXHEIGHT, max(config.MINHEIGHT, event.h))
            if (width, height) != event.size:
                screen = pygame.display.set_mode((width, height), RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for (row, col), rect in tile_rects.items():
                if rect.collidepoint(mouse_x, mouse_y):
                    print(f"Mouse clicked on tile: row={row}, col={col}")
                    if character.move_to(map_data, row, col):
                        player_pos = [character.x, character.y]

    # Масштабируем ассеты
    stone_tile, water_tile, wall_tile, player_sprite = (
        scale_tile_image(image)
        for image in (stone_tile, water_tile, wall_tile, player_sprite)
    )
    background = scale_background(
        screen.get_width(), screen.get_height(), background_image
    )

    screen.blit(background, (0, 0))
    tile_images = {0: stone_tile, 1: water_tile, 2: wall_tile}

    for row in range(config.GRID_HEIGHT):
        for col in range(config.GRID_WIDTH):
            tile_x = offset_x + (col - row) * config.TILE_WIDTH // 2
            tile_y = offset_y + (col + row) * config.TILE_HEIGHT // 2
            tile_type = map_data[row][col]
            tile_image = tile_images[tile_type]
            draw_tile(screen, tile_x, tile_y, tile_image, tile_type)

            rect = pygame.Rect(
                tile_x - config.TILE_WIDTH // 2,
                tile_y - config.TILE_HEIGHT // 2,
                config.TILE_WIDTH,
                config.TILE_HEIGHT,
            )
            tile_rects[(row, col)] = rect

    screen.blit(
        player_sprite,
        (player_x - config.TILE_WIDTH // 2, player_y - config.TILE_HEIGHT * 2),
    )

    highlighted_tile = None
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Проверка, попадает ли точка в ромб
    for (row, col), (tile_x, tile_y) in tile_centers.items():
        if is_point_in_rhombus((mouse_x, mouse_y), (tile_x, tile_y), config.TILE_WIDTH, config.TILE_HEIGHT):
            highlighted_tile = (row, col)
            break

    # Создаем полупрозрачную поверхность для подсветки
    highlight_surface = pygame.Surface((config.TILE_WIDTH, config.TILE_HEIGHT), pygame.SRCALPHA)
    highlight_surface.fill((255, 255, 0, 128))  # 128 — уровень прозрачности

    if highlighted_tile:
        row, col = highlighted_tile
        tile_x, tile_y = tile_centers[(row, col)]

        # Вычисляем вершины ромба для заданного тайла, используя центр тайла
        half_width = config.TILE_WIDTH // 2
        half_height = config.TILE_HEIGHT // 2
        vertices = [
            (tile_x, tile_y - half_height),  # Верхняя точка
            (tile_x - half_width, tile_y),  # Левая точка
            (tile_x, tile_y + half_height),  # Нижняя точка
            (tile_x + half_width, tile_y)  # Правая точка
        ]

        # Рисуем ромб на поверхности
        pygame.draw.polygon(highlight_surface, (255, 255, 0, 128), vertices)

        # Отображаем подсветку на экране в правильной позиции
        screen.blit(highlight_surface, (tile_x - half_width, tile_y - half_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
