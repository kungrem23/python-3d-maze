from settings import *
import MazeToText
import pprint
import random
try:
    spawnpoint = 0
    pool = []
    text_map1 = MazeToText.maze(10, 10, 10).layout
    new_m = ['00' + '1' * 8]
    for i in text_map1:
        new_m.append("".join(list(map(str, i))))
    for i in new_m:
        print(i)
    for i in range(len(new_m)):
        if i != 0 and i != 1:
            new_m[i] = '1' + new_m[i] + '1'
        else:
            new_m[i] = '0' + new_m[i] + '1'

    for i in new_m:
        print(i)
    print()
    for i in range(0, len(new_m)):
        for j in range(0, len(new_m)):
            if new_m[i][j] == '0' and i != 0 and j != 0 and j != 1:
                pool.append([j, i])


    spawnpoint = random.choice(pool)

    print(1, spawnpoint)


   # print(text_map)
    world_map = set()
    for j, row in enumerate(new_m):
        for i, char in enumerate(row):
            if char == '1':

                world_map.add((i * TILE, j * TILE))

  #  print(world_map)
except Exception:
    pass
