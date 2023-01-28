import pygame
from settings import *
from ray import ray_casting
import map


#Класс с отрисовкой фпс, мини-карты, и вызова рей кастинга
class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {'1': pygame.image.load('textures/1.png').convert(),
                         '2': pygame.image.load('textures/2.png').convert(),
                         '3': pygame.image.load('textures/brick1.jpg').convert(),
                         '4': pygame.image.load('textures/brick3.jpg').convert(),
                         '5': pygame.image.load('textures/rock3.jpg').convert(),
                         'S': pygame.image.load('textures/sky.png').convert()
                         }
        self.texture = self.textures[str(map.texture)]

    # Отрисовка неба и пола
    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    # Отрисовка мира
    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    # Отрисовка фпс
    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, RED)
        self.sc.blit(render, FPS_POS)

    # Отрисовка количества монет
    def coins(self, now, all):
        display_coins = f"Собрано {now} из {all}"
        render = self.font.render(display_coins, 0, RED)
        self.sc.blit(render, COINS_POS)

    # Отрисовка количества крестиков

    def crosses(self, now):
        display_coins = f"Осталось крестиков {now}"
        render = self.font.render(display_coins, 0, RED)
        self.sc.blit(render, CROSS_POS)

    # Отрисовка миникарты
    def mini_map(self, player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                               map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 5)
        for x, y in map.mini_map:
            pygame.draw.rect(self.sc_map, SANDY, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)
