from entities.base import BaseEntity
from utils import find_path


class Hero(BaseEntity):
    def __init__(self, x, y, action_points, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.x = x
        self.y = y
        self.action_points = action_points

    def move_to(self, map_data, target_row, target_col):
        if map_data[target_row][target_col] != 2:  # 2 = стена
            distance = abs(self.x - target_row) + abs(self.y - target_col)
            if self.action_points >= distance:
                self.x = target_row
                self.y = target_col
                self.action_points -= distance
                return True
        return False
