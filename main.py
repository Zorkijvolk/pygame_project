import os
import sys
import pygame
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily("Comic Sans MS")

        button_size = (500, 150)
        screen_w, screen_h = self.screen().size().width(), self.screen().size().height()

        self.pixmap = QPixmap('data/космос.png')
        self.pixmap = self.pixmap.scaled(screen_w, screen_h,
                                         aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, screen_w, screen_h)
        self.background.setPixmap(self.pixmap)
        self.startButton = QPushButton('start', self)
        self.startButton.resize(button_size[0], button_size[1])
        self.startButton.move((screen_w - button_size[0]) // 2, 250)
        self.startButton.setStyleSheet('''font-size: 20pt;
               background-color: blue;''')

        self.exitButton = QPushButton('exit', self)
        self.exitButton.setStyleSheet('''font-size: 20pt;
               background-color: blue;''')
        self.exitButton.move((screen_w - button_size[0]) // 2, 650)
        self.exitButton.resize(button_size[0], button_size[1])
        self.exitButton.setFont(font)

        self.settingsButton = QPushButton('settings', self)
        self.settingsButton.setStyleSheet('''font-size: 20pt;
               background-color: blue;''')
        self.settingsButton.move((screen_w - button_size[0]) // 2, 450)
        self.settingsButton.resize(button_size[0], button_size[1])
        self.exitButton.setFont(font)

        self.backButton = QPushButton('back', self)
        self.backButton.setStyleSheet('''font-size: 20pt;
               background-color: blue;''')
        self.backButton.resize(100, 100)
        self.backButton.move(10, 10)
        self.backButton.setFont(font)
        self.backButton.hide()

        self.startButton.setFont(font)

        self.startButton.clicked.connect(self.start)
        self.exitButton.clicked.connect(lambda x: self.close())
        self.settingsButton.clicked.connect(self.settings)
        self.backButton.clicked.connect(self.first_page)

        self.nameProject = QLabel('               THE MAZE', self)
        self.nameProject.resize(self.screen().size().width(), 200)
        self.nameProject.move(0, 0)
        self.nameProject.setStyleSheet('''font-size: 80pt;
               background-color: blue;''')
        self.nameProject.setFont(font)

    def start(self):
        self.hide()
        start_game()
        sys.exit()

    def settings(self):
        self.startButton.hide()
        self.exitButton.hide()
        self.nameProject.hide()
        self.settingsButton.hide()
        self.backButton.show()

    def first_page(self):
        self.startButton.show()
        self.exitButton.show()
        self.nameProject.show()
        self.settingsButton.show()
        self.backButton.hide()


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
        self.frames = [player_image, player_animation]
        self.cur_image = 0
        self.image = self.frames[self.cur_image]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + move_x, tile_height * pos_y + 5 + move_y)

    def update(self):
        if self.cur_image:
            self.cur_image = 0
        else:
            self.cur_image = 1
        self.image = self.frames[self.cur_image]

    def move_l(self, m):
        self.rect.x -= m
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.x += m

    def move_r(self, m):
        self.rect.x += m
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.x -= m

    def move_up(self, m):
        self.rect.y -= m
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.y += m

    def move_down(self, m):
        self.rect.y += m
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect.y -= m


class FirstPlayerBoard(Player):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(pos_x, pos_y, move_x, move_y)
        pass


class SecondPlayerBoard(Player):
    def __init__(self, pos_x, pos_y, move_x, move_y):
        super().__init__(pos_x, pos_y, move_x, move_y)
        pass


width, height, player, player_image, tile_images, tile_width, tile_height = None, None, None, None, None, None, None
player_animation = None


def start_game():
    global width, height, player, player_image, tile_images, tile_width, tile_height, player_animation
    pygame.init()

    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    player = None
    player_image = load_image('player.png')
    player_animation = load_image('player2.png')
    tile_images = {
        'wall': load_image('brick.png'),
        'empty': load_image('path.png')}
#        'key1': load_image(),
#        'key2': load_image()}

    tile_width = tile_height = 70

    clock = pygame.time.Clock()
    FPS = 50
    screen.fill('black')
    pygame.display.set_caption('THE MAZE')

    first_player = generate_level(load_level('first_level_0_0.txt'), 1,
                                  (width - 2100) // 3, (height - 1050) // 2)
    second_player = generate_level(load_level('first_level_0_1.txt'), 2,
                                   2 * ((width - 2100) // 3) + 1050, (height - 1050) // 2)

    running = True
    t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    second_player.move_l(70)
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    second_player.move_down(70)
                if pygame.key.get_pressed()[pygame.K_UP]:
                    second_player.move_up(70)
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    second_player.move_r(70)
                if pygame.key.get_pressed()[pygame.K_w]:
                    first_player.move_up(70)
                if pygame.key.get_pressed()[pygame.K_a]:
                    first_player.move_l(70)
                if pygame.key.get_pressed()[pygame.K_s]:
                    first_player.move_down(70)
                if pygame.key.get_pressed()[pygame.K_d]:
                    first_player.move_r(70)
        if t == 4:
            t = 0
            first_player.update()
            second_player.update()
        else:
            t += 1
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
