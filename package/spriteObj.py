import pygame
from settings import *
import player

lst = []


# Класс-управляющий спрайтами
class Sprites:
    def __init__(self):
        self.sprite_types = {
            'coin': pygame.image.load('sprites/coin.png').convert_alpha(),
            'cross': pygame.image.load('sprites/cross.png').convert_alpha()
        }
        self.list_of_objects = [


        ]

    def makelistofcoins(self, count, coords):

        for i in range(count):
            self.list_of_objects.append(SpriteObject(self.sprite_types['coin'], True, coords[i], 1, 0.4, True, True))
        global lst
        lst = self.list_of_objects

    def makecross(self, coords):
        self.list_of_objects.append(SpriteObject(self.sprite_types['cross'], True, coords, 1, 0.4, False, False))

    def DeleteCoin(self, ind):
        self.list_of_objects.pop(ind)


# Когда подобрали монетку
def TakeCoin(coin_pos):
    global a
    for i in range(len(lst)):
        if (lst[i].x - 10, lst[i].y - 10) == coin_pos:
            a = lst[i]
            lst.pop(i)
            break
    return a, lst


# Сам объект спрайта
class SpriteObject:
    def __init__(self, object, static, pos, shift, scale, blocked, iscoords):
        self.object = object
        self.static = static
        if iscoords:
            self.pos = self.x, self.y = pos[0] * TILE + 15, pos[1] * TILE + 15
        else:
            self.pos = self.x, self.y = pos[0], pos[1]
        self.blocked = blocked
        self.shift = shift
        self.scale = scale
        if iscoords:
            self.side = 20
        else:
            self.side = 0
        self.pos = self.x - self.side // 2, self.y - self.side // 2
        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:

            if distance_to_sprite == 0:
                distance_to_sprite = 0.1
            elif self.scale == 0:
                self.scale = 0.1

            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)

            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))

            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
