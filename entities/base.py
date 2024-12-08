import pygame
from pygame.locals import *

from utils import scale_tile_image


class BaseEntity:
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_path = image_path
        self.sprite = pygame.image.load(self.image_path).convert_alpha()
        self.sprite_scaled = scale_tile_image(self.sprite)

    def move(self, event, map_data, obj_pos=None):
        if obj_pos is None:
            obj_pos = [self.x, self.y]
        if event.type == KEYDOWN:  # Управление персонажем
            if event.key == K_w:  # Вверх
                if obj_pos[0] > 0 and map_data[obj_pos[0] - 1][obj_pos[1]] != 2:
                    obj_pos[0] -= 1
            elif event.key == K_s:  # Вниз
                if (
                    obj_pos[0] < len(map_data) - 1
                    and map_data[obj_pos[0] + 1][obj_pos[1]] != 2
                ):
                    obj_pos[0] += 1
            elif event.key == K_a:  # Влево
                if obj_pos[1] > 0 and map_data[obj_pos[0]][obj_pos[1] - 1] != 2:
                    obj_pos[1] -= 1
            elif event.key == K_d:  # Вправо
                if (
                    obj_pos[1] < len(map_data[0]) - 1
                    and map_data[obj_pos[0]][obj_pos[1] + 1] != 2
                ):
                    obj_pos[1] += 1
