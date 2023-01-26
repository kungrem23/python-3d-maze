import pygame
from settings import *
from player import Player
import math
import map
from ray import ray_casting

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None

maps = None

while True:
    try:
        if maps is None:
            maps = map.world_map
            player = Player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        player.movement()
        sc.fill(BLACK)

        pygame.draw.rect(sc, BLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

        ray_casting(sc, player.pos, player.angle)

        pygame.draw.circle(sc, BLACK, (int(player.x), int(player.y)), 12)
        pygame.draw.line(sc, GREEN, player.pos, (player.x + WIDTH * math.cos(player.angle),
                                                 player.y + WIDTH * math.sin(player.angle)), 2)
        if maps is not None:

            for x, y in maps:
                pygame.draw.rect(sc, PURPLE, (x, y, TILE, TILE), 1)

        pygame.display.flip()
        clock.tick(FPS)


    except Exception:
        pass
