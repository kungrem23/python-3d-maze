from settings import *
import pygame
import math
from map import collision_walls
import map
import settings
from spriteObj import TakeCoin


# Класс игрока
class Player:
    def __init__(self, sprites):
        self.x = map.spawnpoint[0] * settings.TILE + 15
        self.y = map.spawnpoint[1] * settings.TILE + 15
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004

        # collision parameters
        self.side = 20
        self.rect = pygame.Rect(self.x, self.y, self.side, self.side + 10)

        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls + self.collision_sprites

    @property
    def pos(self):
        return (self.x, self.y)

   # def updatecollisions(self, obj):

     #   self.collision_sprites.clear()
     #   self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
     #    self.sprites.list_of_objects]
      #S  self.collision_list = collision_walls + self.collision_sprites


    # Смотрим столкновения
    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if hit_rect.size == (20, 20):
                    # Столкнулись с монеткой
                    a = (hit_rect.x, hit_rect.y)
                    spr, lst = TakeCoin(a)
                    for i in range(len(self.sprites.list_of_objects)):
                        if self.sprites.list_of_objects[i] == spr:
                            self.sprites.list_of_objects.pop(i)
                    self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                              self.sprites.list_of_objects]
                    self.collision_list = collision_walls + self.collision_sprites
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()

        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    # Перемещение
    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        mouseMotion = pygame.mouse.get_rel()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)
        if mouseMotion[0] != 0:
        #     self.angle -= 0.003 * mouseMotion[0]
        #     pygame.mouse.set_pos(600, 400)
        # if mouseMotion[0] > 0:
            self.angle += 0.002 * mouseMotion[0]
            pygame.mouse.set_pos(600, 400)

        self.angle %= DOUBLE_PI

    # def mouse_motion(self, how_much):
    #     if keys[pygame.K_LEFT]:
    #         self.angle -= 0.03
    #     if keys[pygame.K_RIGHT]:
    #         self.angle += 0.03
