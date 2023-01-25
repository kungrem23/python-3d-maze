import random
import time

import pygame

from package.ThreeD_object_setter import make_wall, destroy_wall

#maze vars
x = 0
y = 0
wCell = 20
wMaze = 20
grid = []
visited = []
stack = []
solution = {}

#build grid
def build_grid(x, y, screen):
    global wCell
    global wMaze
    for i in range(1, wMaze + 1):
        x = wCell
        y = y + wCell
        for i in range(1, wMaze + 1):
            # make_wall([x, y], [x + wCell, y])
            # make_wall([x + wCell, y], [x + wCell, y + wCell])
            # make_wall([x + wCell, y + wCell], [x, y + wCell])
            # make_wall([x, y + wCell], [x, y])
            pygame.draw.line(screen, 'white', [x, y], [x + wCell, y])
            pygame.draw.line(screen, 'white', [x + wCell, y], [x + wCell, y + wCell])
            pygame.draw.line(screen, 'white', [x + wCell, y + wCell], [x, y + wCell])
            pygame.draw.line(screen, 'white', [x, y + wCell], [x, y])
            pygame.display.flip()
            grid.append((x, y))
            x += 20

#destroy unnecessary walls
def push_up(x, y, screen):
    # destroy_wall(x, y, 'up')
    pygame.draw.rect(screen, 'blue', (x + 1, y - wCell + 1, 19, 39), 0)
    pygame.display.flip()

def push_down(x, y, screen):
    # destroy_wall(x, y, 'down')
    pygame.draw.rect(screen, 'blue', (x + 1, y + 1, 19, 39), 0)
    pygame.display.flip()


def push_left(x, y, screen):
    # destroy_wall(x, y, 'left')
    pygame.draw.rect(screen, 'blue', (x - wCell + 1, y + 1, 39, 19), 0)
    pygame.display.flip()


def push_right(x, y, screen):
    # destroy_wall(x, y, 'right')
    pygame.draw.rect(screen, 'blue', (x + 1, y + 1, 39, 19), 0)
    pygame.display.flip()

#можно убрать
def single_cell(x, y, screen):
    pass
    #pygame.draw.rect(screen, 'green', (x + 1, y + 1, 18, 18), 0)

def carve_out_maze(x, y, screen):
    single_cell(x, y, screen)
    stack.append((x, y))
    visited.append((x, y))
    while len(stack) > 0:
        time.sleep(.07)
        cell = []
        if (x + wCell, y) not in visited and (x + wCell, y) in grid:
            cell.append('right')
        if (x - wCell, y) not in visited and (x - wCell, y) in grid:
            cell.append('left')
        if (x, y + wCell) not in visited and (x, y + wCell) in grid:
            cell.append('down')
        if (x, y - wCell) not in visited and (x, y - wCell) in grid:
            cell.append('up')
        if len(cell) > 0:
            cell_choosen = (random.choice(cell))
            if cell_choosen == 'right':
                push_right(x, y, screen)
                x += wCell
                visited.append((x, y))
                stack.append((x, y))
            elif cell_choosen == 'left':
                push_left(x, y, screen)
                x -= wCell
                visited.append((x, y))
                stack.append((x, y))
            elif cell_choosen == 'down':
                push_down(x, y, screen)
                y += wCell
                visited.append((x, y))
                stack.append((x, y))
            elif cell_choosen == 'up':
                push_up(x, y, screen)
                y -= wCell
                visited.append((x, y))
                stack.append((x, y))
        else:
            time.sleep(.05)
            x, y = stack.pop()
            single_cell(x, y, screen)


x = 20
y = 20

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()

build_grid(40, 0, screen)
carve_out_maze(x, y, screen)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()