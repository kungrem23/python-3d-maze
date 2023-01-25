import pygame, random, argparse
from pygame.locals import *
from pprint import pprint
FLOOR = 0
WALL = 1
PATH = 2

FLOOR_COLOUR = (0, 0, 0)
WALL_COLOUR = (255, 255, 255)
PATH_COLOUR = (0, 255, 0)
SOLVER_COLOUR = (255, 0, 0)
MAZE_COLOURS = [FLOOR_COLOUR, WALL_COLOUR, PATH_COLOUR]


def mazeArray(value, width, height):
    return [[value] * height for i in range(width)]


def cellRect(x, y, tile_size):
    return (x * tile_size, y * tile_size, tile_size, tile_size)


class maze():  # The main maze class
    def __init__(self, width, height, tile_size):
        self.layout = mazeArray(WALL, width, height)
        self.visited = mazeArray(0, width, height)
        self.neighbours = []
        self.stack = []
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.x = 0
        self.y = 0

        self.generate()

    def Regenerate(self):
        self.__init__(self.width, self.height, self.tile_size)

    def ClearPath(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.layout[i][j] == PATH:
                    self.layout[i][j] = FLOOR

    def draw(self, solver_x, solver_y):
        for i in range(self.width):
            for j in range(self.height):
                cell_type = self.layout[i][j]
                screen.fill(MAZE_COLOURS[cell_type], cellRect(i, j, self.tile_size))

        screen.fill(SOLVER_COLOUR, cellRect(solver_x, solver_y, self.tile_size))
        pygame.display.flip()

    def generate(self):
        while not self._generate_step():
            pass

    def _generate_step(self):
        # Do one step of generating a layout.

        # Pick a cell and mark it as part of the maze
        self.layout[self.x][self.y] = FLOOR
        # Mark as visited
        self.visited[self.x][self.y] = True

        self.neighbours = []  # Reset neighbours

        # Look for unvisited neighbours
        if (self.y - 2) >= 0:
            if not self.visited[self.x][self.y - 2]:  # Above
                self.neighbours.append((self.x, self.y - 2))

        if (self.x - 2) >= 0:
            if not self.visited[self.x - 2][self.y]:  # Left
                self.neighbours.append((self.x - 2, self.y))

        if (self.x + 2) < self.width:
            if not self.visited[self.x + 2][self.y]:  # Right
                self.neighbours.append((self.x + 2, self.y))

        if (self.y + 2) < self.height:
            if not self.visited[self.x][self.y + 2]:  # Down
                self.neighbours.append((self.x, self.y + 2))

        if self.neighbours:
            # Now choose one randomly
            newCell = self.neighbours[random.randint(0, len(self.neighbours) - 1)]

            # Add current cell to the stack
            self.stack.append((self.x, self.y))

            # Remove the wall between current and chosen cell
            new_x, new_y = newCell

            # Cell is above
            if new_x == self.x and (new_y + 2) == self.y:
                self.layout[new_x][new_y + 1] = FLOOR
            # Cell is below
            elif new_x == self.x and (new_y - 2) == self.y:
                self.layout[new_x][new_y - 1] = FLOOR
            # Cell is left
            elif (new_x + 2) == self.x and new_y == self.y:
                self.layout[new_x + 1][new_y] = FLOOR
            # Cell is right
            elif (new_x - 2) == self.x and new_y == self.y:
                self.layout[new_x - 1][new_y] = FLOOR

            self.x = new_x
            self.y = new_y

        else:  # Cell has no neighbours
            if self.stack:
                # Go back to the previous current cell
                self.x, self.y = self.stack.pop()

            if not self.stack:
                # Generation has finished
                return True




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Maze Generator/Solver')

    parser.add_argument('--width', action="store", dest="width", type=int, default=50,
                        help='Width (in tiles) of the maze generated.')
    parser.add_argument('--height', action="store", dest="height", type=int, default=50,
                        help='Height (in tiles) of the maze generated.')
    parser.add_argument('--tile-size', action="store", dest="tile_size", type=int, default=10,
                        help='Size in pixels of one maze cell. (10 = 10 by 10 square)')

    args = parser.parse_args()

    width_cells = max(1, args.width)
    height_cells = max(1, args.height)
    tile_size = max(1, args.tile_size)

    pygame.init()
    screen = pygame.display.set_mode((width_cells * tile_size, height_cells * tile_size))
    pygame.display.set_caption('Maze Solver')

    try:

        new_maze = maze(width_cells, height_cells, tile_size)
        print(new_maze.layout)


        screen.fill(FLOOR_COLOUR)
        run = True

    finally:
        pygame.quit()




