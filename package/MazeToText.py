import pygame, random, argparse
import map
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

    def ReturnMaze(self):
        return self.layout

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


class mazeSolver():
    def __init__(self, maze, x=0, y=0):
        # Initial position in the maze given
        self.x = x
        self.y = y
        self.maze = maze
        self.neighbours = []
        self.stack = []

    def Reset(self, maze, x=0, y=0):
        self.__init__(maze, x=x, y=y)

    def solve(self):
        # Call this to find and make next move
        self.neighbours = []
        self.maze.layout[self.x][self.y] = PATH

        # Look for open cells
        if (self.y - 1) >= 0:
            if self.maze.layout[self.x][self.y - 1] == FLOOR:  # Above
                self.neighbours.append((self.x, self.y - 1))

        if (self.x - 1) >= 0:
            if self.maze.layout[self.x - 1][self.y] == FLOOR:  # Left
                self.neighbours.append((self.x - 1, self.y))

        if (self.x + 1) < self.maze.width:
            if self.maze.layout[self.x + 1][self.y] == FLOOR:  # Right
                self.neighbours.append((self.x + 1, self.y))

        if (self.y + 1) < self.maze.height:
            if self.maze.layout[self.x][self.y + 1] == FLOOR:  # Down
                self.neighbours.append((self.x, self.y + 1))

        if self.neighbours:  # If we found some neighbours that are open
            new_x, new_y = self.neighbours[0]  # Take the first option
            self.stack.append((self.x, self.y))  # Save old position to stack
            self.x = new_x
            self.y = new_y

        else:  # Cell has no open neighbours
            if self.stack:
                # Go back to the previous current cell
                self.x, self.y = self.stack.pop()

        return self.x, self.y


def checkControls(maze, solver):
    # check player controls (return False if we need to quit)
    pygame.event.pump()
    key = pygame.key.get_pressed()

    if key[pygame.K_ESCAPE]:
        return False

    if key[pygame.K_TAB]:
        screen.fill(FLOOR_COLOUR)
        maze.Regenerate()
        solver.Reset(maze)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x /= maze.tile_size
            mouse_y /= maze.tile_size

            if (maze.layout[mouse_x][mouse_y] != WALL):
                maze.ClearPath()
                solver.Reset(maze, x=mouse_x, y=mouse_y)
        elif event.type == pygame.QUIT:
            return False

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

        new_solver = mazeSolver(new_maze)
        screen.fill(FLOOR_COLOUR)
        run = True
        while True:
            new_maze.draw(*new_solver.solve())
            run = checkControls(new_maze, new_solver)

    finally:
        pygame.quit()




