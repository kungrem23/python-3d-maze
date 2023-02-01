import pygame
from settings import *
from player import Player
from ray import *
import map
from spriteObj import *
import sys
import drawing
import random
import time


# Выход из игры
def terminate():
    pygame.quit()
    sys.exit()


# Экран начала игры
def start_screen(sc):
    intro_text = ["3D Maze Python", "",
                  "Вы спавнитесь в рандомной точке лабиринта.",
                  "Вам необходимо найти выход", "",
                  "Постарайтесь собрать как можно больше монет",
                  "Для начала нажмите ЛКМ"]

    fon = pygame.transform.scale(pygame.image.load('sprites/fon/fon.jpg'), (WIDTH, HEIGHT))

    sc.blit(fon, (0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 46)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))

        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# Экран конца игры
def end_screen(sc, coins, all):
    intro_text = ["Поздравляем! Вы выбрались", "",
                  f"Вы собрали {coins} монет из {all}",
                  f"Время: {pygame.time.get_ticks() // (1000 * 60)}:{(pygame.time.get_ticks() - pygame.time.get_ticks() // (1000 * 60)) // 1000}",]

    fon = pygame.transform.scale(pygame.image.load('sprites/fon/fon.jpg'), (WIDTH, HEIGHT))

    sc.blit(fon, (0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 46)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))

        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
# Инициализация экрана, миникарты
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pygame.time.Clock()
start_screen(sc)
start_time = pygame.time.get_ticks()
check_time = False


sprites = Sprites()
draw = False
# карта мира
maps = map.world_map
d = map.new_m
countofcoins = 0
countofcross = 7

coins = []
# начинаем расставлять монетки
for i in range(0, len(d)):
    for j in range(0, len(d)):
        if d[i][j] == '0' and i != 0 and i != 1 and j != 0 and j != 1:
            a = random.randint(0, 100)
            if a < 10:
                coins.append([j, i])
                countofcoins += 1
if countofcoins == 0:
    countofcoins = 1
# сделали лист спрайтов монет
sprites.makelistofcoins(countofcoins, coins)

player = Player(sprites)
drawing = drawing.Drawing(sc, sc_map, player)

# Цикл игры
while True:

    # Если мышь не на экране, то скрываем
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
    # Вышли из лабиринти - конец игры
    if player.x < 80 and player.y < 80:
        end_screen(sc, countofcoins - len([i for i in sprites.list_of_objects if i.blocked]), countofcoins)
    # Нажатие кнопки q - режим разработчика с включенной картой
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player.shot:
                player.shot = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if draw:
                    draw = False
                else:
                    draw = True
            if event.key == pygame.K_e:
                if countofcross > 0:
                    sprites.makecross((player.x, player.y))

    # Движение игрока
    player.movement()

    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.texture)

    # отрисовка стен
  #  print(len(world_map), len(walls))
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.player_weapon([wall_shot, sprites.sprite_shot])
    drawing.fps(clock)
    drawing.coins(countofcoins - len([i for i in sprites.list_of_objects if i.blocked]), countofcoins)
    drawing.crosses(countofcross - len([i for i in sprites.list_of_objects if i.blocked is not True]))
    drawing.timer(pygame.time.get_ticks() - start_time)
    # миникарта
    if draw:
        print("Активирован режим разработчика")
        drawing.mini_map(player)

    pygame.display.flip()
    clock.tick()