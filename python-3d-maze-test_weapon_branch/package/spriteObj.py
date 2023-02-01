import pygame
from settings import *
import player
from collections import deque

lst = []


# Класс-управляющий спрайтами
class Sprites:

    def __init__(self):
        self.sprite_parameters = {
            'sprite_coin': {
                'sprite': pygame.image.load('sprites/coin/coin.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1,
                'scale': 0.4,
                'animation': None,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'is_dead': None,
                'dead_shift': 0.6,
                'flag': 'npc',
                'death_animation': deque([pygame.image.load(f'sprites/devil/death/{i}.png')
                                         .convert_alpha() for i in range(6)])
            },
            'sprite_cross': {
                'sprite': pygame.image.load('sprites/cross/cross.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1,
                'scale': 0.6,
                'animation': None,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': False,
                'is_dead': 'immortal',
                'dead_shift': 0.6,
                'flag': 'decor',
                'death_animation': False
            },
            'sprite_devil': {
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.1,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'death_animation': deque([pygame.image.load(f'sprites/devil/death/{i}.png')
                                         .convert_alpha() for i in range(6)]),
                'blocked': True,
                'is_dead': None,
                'dead_shift': 0.6,
                'flag': 'npc',
            }
        }

        self.list_of_objects = [

        ]

    @property
    def sprite_shot(self):
        try:
            return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))
        except Exception:
            pass

    def makelistofcoins(self, count, coords):

        for i in range(count):
            self.list_of_objects.append(SpriteObject(self.sprite_parameters['sprite_devil'], coords[i], True, True))
        global lst
        lst = self.list_of_objects

    def makecross(self, coords):
        self.list_of_objects.append(SpriteObject(self.sprite_parameters['sprite_cross'], coords, False, False))

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
    def __init__(self, parameters, pos, iscoords, isnpc):
        self.object = parameters['sprite']

        self.flag = parameters['flag']
        # self.obj_action = parameters['obj_action'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        if parameters['death_animation']:
            self.death_animation = parameters['death_animation'].copy()
            self.is_dead = parameters['is_dead']
            self.dead_shift = parameters['dead_shift']
        self.scale = parameters['scale']
        if parameters['animation'] is not None:
            self.animation = parameters['animation'].copy()
        else:
            self.animation = False
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.animation_count = 0
        self.dead_animation_count = 0
        self.delete = False
        if iscoords:
            self.pos = self.x, self.y = pos[0] * TILE + 20, pos[1] * TILE + 20
        else:
            self.pos = self.x, self.y = pos[0], pos[1]

        if isnpc is not True:
            self.side = 20
        else:
            self.side = 30
        self.pos = self.x - self.side // 2, self.y - self.side // 2
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite),
                                   HEIGHT)
            sprite_width = int(self.proj_height * self.scale)
            sprite_height = int(self.proj_height * self.scale)
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # sprite animation
            sprite_object = self.object
            if self.animation and self.distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            if self.is_dead and self.is_dead != 'immortal':

                sprite_object = self.dead_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            else:
                sprite_object = self.sprite_animation()

            sprite_pos = (self.current_ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))



            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation is not False:

            sprite_object = self.animation[0]

            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:

                self.animation_count = 0
            return sprite_object
        return self.object

    def dead_animation(self):

        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    @property
    def is_on_fire(self):
        try:
            if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked and self.proj_height != 0:
                return self.distance_to_sprite, self.proj_height
            return float('inf'), None
        except AttributeError:
            pass
