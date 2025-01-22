import os
import sys
import pygame
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily("Comic Sans MS")

        self.setGeometry(0, 0, 2000, 1000)
        self.setFixedSize(2000, 1000)
        self.setStyleSheet('background-color: {}'.format('#000'))
        self.aviationButton = QPushButton('start', self)
        self.aviationButton.resize(500, 100)
        self.aviationButton.move(500, 400)
        self.aviationButton.setStyleSheet('''font-size: 20pt;
               background-color: red;''')
        self.armyButton = QPushButton(self)
        self.armyButton.setStyleSheet("background-color: {}".format('#e30b0b'))
        self.armyButton.move(500, 550)
        self.armyButton.resize(500, 100)
        self.aviationButton.clicked.connect(self.start)
        self.armyButton.setFont(font)
        self.aviationButton.setFont(font)
        self.nameProject = QLabel('               THE MAZE', self)
        self.nameProject.resize(2000, 100)
        self.nameProject.move(0, 20)
        self.nameProject.setStyleSheet('''font-size: 80pt;
               background-color: red;''')
        self.nameProject.setFont(font)

    def start(self):
        self.hide()
        start_game()
        sys.exit()


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()


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
                Box('wall', x, y, m_x, m_y)
            #                Tile('wall', x, y, m_x, m_y)
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


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(box_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + move_x, tile_height * pos_y + 5 + move_y)

    def move_l(self):
        self.rect.x -= 50
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.x += 50

    def move_r(self):
        self.rect.x += 50
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.x -= 50

    def move_up(self):
        self.rect.y -= 50
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.y += 50

    def move_down(self):
        self.rect.y += 50
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.y -= 50


class FirstPlayerBoard(Player):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(pos_x, pos_y, move_x, move_y)
        pass


class SecondPlayerBoard(Player):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(pos_x, pos_y, move_x, move_y)
        pass


width, height, player, player_image, tile_images, tile_width, tile_height = None, None, None, None, None, None, None


def start_game():
    global width, height, player, player_image, tile_images, tile_width, tile_height
    pygame.init()
    size = width, height = 3000, 1000
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    player = None
    player_image = load_image('mar.png')
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')}

    tile_width = tile_height = 50

    clock = pygame.time.Clock()
    FPS = 50
    screen.fill('black')
    pygame.display.set_caption('Игрушка')

    first_player = generate_level(load_level('first_level_0_0.txt'), 1, 200, 100)
    second_player = generate_level(load_level('first_level_0_1.txt'), 2, 1150, 100)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    second_player.move_l()
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    second_player.move_down()
                if pygame.key.get_pressed()[pygame.K_UP]:
                    second_player.move_up()
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    second_player.move_r()
                if pygame.key.get_pressed()[pygame.K_w]:
                    first_player.move_up()
                if pygame.key.get_pressed()[pygame.K_a]:
                    first_player.move_l()
                if pygame.key.get_pressed()[pygame.K_s]:
                    first_player.move_down()
                if pygame.key.get_pressed()[pygame.K_d]:
                    first_player.move_r()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Main()
    n.showFullScreen()
    sys.exit(app.exec())