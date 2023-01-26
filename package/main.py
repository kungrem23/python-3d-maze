import pygame
import random
import sys
# from package import ...


def load_image(a):
    return pygame.image.load(a)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["3D Maze Python", "",
                  "Вы спавнитесь в рандомной точке лабиринта.",
                  "Вам необходимо найти выход", "",
                  "Для начала нажмите ЛКМ"]

    fon = pygame.transform.scale(load_image('../data/fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
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
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return # game()
        pygame.display.flip()
        clock.tick(FPS)

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


WIDTH, HEIGHT = 500, 500
FPS = 50
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
start_screen()