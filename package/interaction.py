from settings import *
from map import world_map
from ray import mapping
import math
import pygame
from spriteObj import *


def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing

    def interaction_objects(self, player):
        if self.player.shot and self.drawing.shot_animation_trigger:
            try:
                for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                    if obj.is_on_fire[1]:
                        if obj.is_dead != 'immortal' and not obj.is_dead:

                            if ray_casting_npc_player(obj.x, obj.y,
                                                      world_map, self.player.pos):

                                obj.is_dead = True
                                obj.blocked = None
                                self.drawing.shot_animation_trigger = False

                                player.update_collision()
                        break
            except Exception:
                pass


    def clear_world(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]