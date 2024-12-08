import heapq

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


def heuristic(a, b):
    """Возвращает расстояние Манхэттена между двумя точками"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(map_data, start, goal):
    """Алгоритм A* для нахождения кратчайшего пути"""
    rows, cols = len(map_data), len(map_data[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if (
                    0 <= neighbor[0] < rows
                    and 0 <= neighbor[1] < cols
                    and map_data[neighbor[0]][neighbor[1]] != 2
            ):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Если путь не найден


def is_point_in_rhombus(point, center, width, height):
    """
    Проверяет, находится ли точка внутри ромба.
    :param point: Точка (x, y), например, координаты мыши.
    :param center: Центр ромба (x, y), например, центр тайла.
    :param width: Ширина ромба (TILE_WIDTH).
    :param height: Высота ромба (TILE_HEIGHT).
    :return: True, если точка внутри ромба.
    """
    px, py = point
    cx, cy = center
    dx = abs(px - cx) / (width / 2)
    dy = abs(py - cy) / (height / 2)
    return dx + dy <= 1
