import os
import sys
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, n_player, m_x=0, m_y=0):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, m_x, m_y)
            elif level[y][x] == '#':
                Tile('wall', x, y, m_x, m_y)
            elif level[y][x] == '@':
                Tile('empty', x, y, m_x, m_y)
                if n_player == 1:
                    new_player = FirstPlayerBoard(x, y, m_x, m_y)
                else:
                    new_player = SecondPlayerBoard(x, y, m_x, m_y)
    return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + move_x, tile_height * pos_y + 5 + move_y)

    def update(self, x, y):
        x = tile_width * x
        y = tile_height * y
        self.rect.x += x
        self.rect.y += y


class FirstPlayerBoard(Player):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(pos_x, pos_y, move_x, move_y)
        pass


class SecondPlayerBoard(Player):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(pos_x, pos_y, move_x, move_y)
        pass


pygame.init()
size = width, height = 2100, 1000
screen = pygame.display.set_mode(size)
screen.fill('black')
pygame.display.set_caption('Игрушка')

game_started = 1
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player_image = load_image('mar.png')
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')}

tile_width = tile_height = 50

clock = pygame.time.Clock()
FPS = 50

first_player = generate_level(load_level('first_level_0_0.txt'), 1, 200, 100)
second_player = generate_level(load_level('first_level_0_1.txt'), 2, 1150, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
