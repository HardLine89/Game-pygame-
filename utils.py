import pygame

import config


def scale_background(screen_width, screen_height, background_image):
    background_scaled = pygame.transform.scale(
        background_image, (screen_width, screen_height)
    )
    return background_scaled


def scale_tile_image(tile_image):
    tile_scaled = pygame.transform.scale(
        tile_image, (config.TILE_WIDTH, config.TILE_WIDTH)
    )
    return tile_scaled


def draw_tile(screen_obj, x, y, tile_obj, tile_type):
    if tile_type == 2:
        screen_obj.blit(
            tile_obj, (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT // 2)
        )
        for i in range(4):  # Количество слоев стены
            screen_obj.blit(
                tile_obj,
                (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT * (0.5 + i)),
            )
    else:
        screen_obj.blit(
            tile_obj, (x - config.TILE_WIDTH // 2, y - config.TILE_HEIGHT // 2)
        )
