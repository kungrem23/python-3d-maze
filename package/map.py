import time
import pygame
from settings import *
import MazeToText

import random

try:
    spawnpoint = 0
    pool = []
    x_size = 18
    y_size = 18
    # Получили текстовый вид лабиринта из класса MazeToText
    text_map1 = MazeToText.maze(x_size, y_size, 10).layout
    new_m = ['00' + '1' * (x_size - 2)]
    for i in text_map1:
        new_m.append("".join(list(map(str, i))))

    texture = random.randint(1, 5)
    # Добавили новые стены
    for i in range(len(new_m)):
        if i != 0 and i != 1:
            new_m[i] = '1' + new_m[i] + '1'
        else:
            new_m[i] = '0' + new_m[i] + '1'
    for i in new_m:
        print(i)
    for i in range(0, len(new_m)):
        for j in range(0, len(new_m)):
            if new_m[i][j] == '0' and i != 0 and j != 0 and j != 1:
                pool.append([j, i])

    # Выбрали случайную точку спавна
    spawnpoint = random.choice(pool)

    world_map = {}
    mini_map = set()
    collision_walls = []
    # Окончательный вид карты, миникарты, стен для коллизий
    for j, row in enumerate(new_m):
        for i, char in enumerate(row):
            if char != '0':
                mini_map.add((i * MAP_TILE, j * MAP_TILE))
                collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                if char == '1':
                    world_map[(i * TILE, j * TILE)] = '1'


except Exception:
    pass
