import pygame
from settings import *
from player import Player
from ray import ray_casting
import map
from spriteObj import *
import drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pygame.time.Clock()

drawing = drawing.Drawing(sc, sc_map)
sprites = Sprites()
draw = False
maps = map.world_map
player = Player()
while True:
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    if player.x < 68 and player.y < 68:
        print("You have won")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if draw:
                    draw = False
                else:
                    draw = True
    player.movement()
    sc.fill(BLACK)
    drawing.background(player.angle)
    print(player.x, player.y, sprites.list_of_objects)
    walls = ray_casting(player, drawing.texture)
    drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    if draw:
        drawing.mini_map(player)

    pygame.display.flip()
    clock.tick()
