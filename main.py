import os
import sys
import pygame
import datetime as dt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.startButton.move((screen_w - button_size[0]) // 2, 550)
        self.startButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.startButton.setFont(font)

        self.settingsButton = QPushButton('settings', self)
        self.settingsButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.settingsButton.move((screen_w - button_size[0]) // 2, 750)
        self.settingsButton.resize(button_size[0], button_size[1])
        self.settingsButton.setFont(font)

        self.exitButton = QPushButton('exit', self)
        self.exitButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.exitButton.move((screen_w - button_size[0]) // 2, 950)
        self.exitButton.resize(button_size[0], button_size[1])
        self.exitButton.setFont(font)

        self.backButton = QPushButton('back', self)
        self.backButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.backButton.resize(100, 100)
        self.backButton.move(10, 10)
        self.backButton.setFont(font)
        self.backButton.hide()

        self.startButton.clicked.connect(self.start)
        self.exitButton.clicked.connect(lambda x: self.close())
        self.settingsButton.clicked.connect(self.settings)
        self.backButton.clicked.connect(self.first_page)

        self.nameProject = QLabel('THE MAZE', self)
        self.nameProject.resize(self.screen().size().width(), 200)
        self.nameProject.move(0, 0)
        self.nameProject.setStyleSheet('''font-size: 80pt;
               background-color: blue;''')
        self.nameProject.setFont(font)
        self.nameProject.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def start(self):
        self.hide()
        start_game()

    #        sys.exit()

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
                obj = Tile('empty', x, y, m_x, m_y)
            elif level[y][x] == '#':
                obj = Box('wall', x, y, m_x, m_y)
            elif level[y][x] == '@':
                obj = Tile('empty', x, y, m_x, m_y)
                if not (f_players_group and s_players_group):
                    if n_player == 1:
                        new_player = Player(x, y, m_x, m_y, 1)
                    else:
                        new_player = Player(x, y, m_x, m_y, 2)
            elif level[y][x] == 'n':
                obj = Door('north_door', x, y, m_x, m_y)
                door_group_1.add(obj)
                player1_tiles_group.add(obj)
            elif level[y][x] == 's':
                obj = Door('south_door', x, y, m_x, m_y)
                door_group_1.add(obj)
                player1_tiles_group.add(obj)
            elif level[y][x] == 'w':
                obj = Door('west_door', x, y, m_x, m_y)
                door_group_1.add(obj)
                player1_tiles_group.add(obj)
            elif level[y][x] == 'e':
                obj = Door('east_door', x, y, m_x, m_y)
                door_group_1.add(obj)
                player1_tiles_group.add(obj)
            elif level[y][x] == '1':
                obj = Door('north_door', x, y, m_x, m_y)
                door_group_2.add(obj)
                player2_tiles_group.add(obj)
            elif level[y][x] == '2':
                obj = Door('south_door', x, y, m_x, m_y)
                door_group_2.add(obj)
                player2_tiles_group.add(obj)
            elif level[y][x] == '3':
                obj = Door('west_door', x, y, m_x, m_y)
                door_group_2.add(obj)
                player2_tiles_group.add(obj)
            elif level[y][x] == '4':
                obj = Door('east_door', x, y, m_x, m_y)
                door_group_2.add(obj)
                player2_tiles_group.add(obj)
            if isinstance(obj, Box):
                if n_player == 1:
                    player1_box_group.add(obj)
                else:
                    player2_box_group.add(obj)
            elif isinstance(obj, Tile):
                if n_player == 1:
                    player1_tiles_group.add(obj)
                else:
                    player2_tiles_group.add(obj)
    return new_player


def fpause():
    global text_x, text1_y, text2_y
    font = pygame.font.Font(None, 80)
    text1 = font.render("Выйти в меню", True, (0, 255, 0))
    text2 = font.render('Выйти из игры', True, (0, 255, 0))
    text_x = text2.get_width()
    text1_y = text1.get_height()
    text2_y = text2.get_height()
    screen.blit(text1, (width // 2 - text1.get_width() // 2, height // 3))
    screen.blit(text2, (width // 2 - text2.get_width() // 2, height // 3 * 2))
    pygame.draw.rect(screen, (255, 215, 0), (width // 2 - text2.get_width() // 2 - 10, height // 3 - 10,
                                             text2.get_width() + 20, text2.get_height() + 20), 10)
    pygame.draw.rect(screen, (255, 215, 0), (width // 2 - text2.get_width() // 2 - 10, height // 3 * 2 - 10,
                                             text2.get_width() + 20, text2.get_height() + 20), 10)


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites, borders)
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface([w, h])


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)
        self.type = tile_type


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, move_x, move_y, player):
        super().__init__(all_sprites)
        self.frames = [player_image, player_animation]
        self.cur_image = 0
        self.image = self.frames[self.cur_image]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + move_x, tile_height * pos_y + 5 + move_y)
        self.m_x = move_x
        self.m_y = move_y
        if player == 1:
            self.cur_room = 6
        else:
            self.cur_room = 7

    def update(self):
        if self.cur_image:
            self.cur_image = 0
        else:
            self.cur_image = 1
        self.image = self.frames[self.cur_image]

    def move_l(self, m, player_n):
        self.rect.x -= m // 2
        if player_n == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.x += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x += m // 2
                if (self.cur_room - 1) % 4:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    generate_level(load_level(f'map1.{self.cur_room - 1}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room -= 1
                    self.rect.x += (gaming_pole_width - m)
            else:
                self.rect.x -= m // 2
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.x += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x += m // 2
                if (self.cur_room - 1) % 4:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    generate_level(load_level(f'map1.{self.cur_room - 1}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room -= 1
                    self.rect.x += (gaming_pole_width - m)
            else:
                self.rect.x -= m // 2

    def move_r(self, m, player_n):
        self.rect.x += m // 2
        if player_n == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.x -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x -= m // 2
                if self.cur_room % 4:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    generate_level(load_level(f'map1.{self.cur_room + 1}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room += 1
                    self.rect.x -= (gaming_pole_width - m)
            else:
                self.rect.x += m // 2

        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.x -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x -= m // 2
                if self.cur_room % 4:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    generate_level(load_level(f'map1.{self.cur_room + 1}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room += 1
                    self.rect.x -= (gaming_pole_width - m)
            else:
                self.rect.x += m // 2

    def move_up(self, m, player_n):
        self.rect.y -= m // 2
        if player_n == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.y += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y += m // 2
                if self.cur_room - 4 > 0:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    generate_level(load_level(f'map1.{self.cur_room - 4}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room -= 4
                    self.rect.y += (gaming_pole_height - m)
            else:
                self.rect.y -= m // 2
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.y += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y += m // 2
                if self.cur_room - 4 > 0:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    generate_level(load_level(f'map1.{self.cur_room - 4}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room -= 4
                    self.rect.y += (gaming_pole_height - m)
            else:
                self.rect.y -= m // 2

    def move_down(self, m, player_n):
        self.rect.y += m // 2
        if player_n == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.y -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y -= m // 2
                if self.cur_room + 4 < 13:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    generate_level(load_level(f'map1.{self.cur_room + 4}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room += 4
                    self.rect.y -= (gaming_pole_height - m)
            else:
                self.rect.y += m // 2
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.y -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y -= m // 2
                if self.cur_room + 4 < 13:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    generate_level(load_level(f'map1.{self.cur_room + 4}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room += 4
                    self.rect.y -= (gaming_pole_height - m)
            else:
                self.rect.y += m // 2

    def check_doors(self, player_n):
        if player_n == 1 and pygame.sprite.spritecollideany(self, door_group_1):
            pygame.draw.rect(screen, pygame.Color('blue'),
                             (left_x, everyone_y, gaming_pole_width + 1, gaming_pole_height + 1))
            f_players_group.empty()
            player1_tiles_group.empty()
            player1_box_group.empty()
            door_group_1.empty()
        elif player_n == 2 and pygame.sprite.spritecollideany(self, door_group_2):
            pygame.draw.rect(screen, pygame.Color('blue'),
                             (right_x, everyone_y, gaming_pole_width + 1, gaming_pole_height + 1))
            s_players_group.empty()
            player2_tiles_group.empty()
            player2_box_group.empty()
            door_group_2.empty()


width, height, player, player_image, tile_images, screen = None, None, None, None, None, None
gaming_pole_width, gaming_pole_height, left_x, right_x, everyone_y = 0, 0, 0, 0, 0
text_x, text1_y, text2_y = None, None, None
tile_width = tile_height = 50
tile_count_w = 15
tile_count_h = 15
player_animation = None
duplicate_for_f_pl = None
duplicate_for_s_pl = None
all_sprites = pygame.sprite.Group()

player1_tiles_group = pygame.sprite.Group()
player1_box_group = pygame.sprite.Group()

player2_tiles_group = pygame.sprite.Group()
player2_box_group = pygame.sprite.Group()

f_players_group = pygame.sprite.Group()
s_players_group = pygame.sprite.Group()

door_group_1 = pygame.sprite.Group()
door_group_2 = pygame.sprite.Group()

borders = pygame.sprite.Group()


def start_game():
    global width, height, player, player_image, tile_images, tile_width, tile_height, player_animation, screen
    global gaming_pole_width, gaming_pole_height, left_x, right_x, everyone_y
    pygame.init()

    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    player = None
    player_image = load_image('player.png', -1)
    player_animation = load_image('player2.png', -1)
    tile_images = {
        'wall': load_image('brick.png'),
        'empty': load_image('path.png'),
        'north_door': load_image('door_opened.png'),
        'east_door': load_image('door_opened_west.png'),
        'west_door': load_image('door_opened_east.png'),
        'south_door': load_image('door_opened_south.png')}
    #        'key1': load_image(),
    #        'key2': load_image()}

    gaming_pole_width = tile_width * tile_count_w
    gaming_pole_height = tile_height * tile_count_h

    clock = pygame.time.Clock()
    FPS = 50
    screen.fill('black')
    pygame.display.set_caption('THE MAZE')

    left_x = (width - gaming_pole_width * 2) // 3 - 1
    right_x = 2 * left_x + gaming_pole_width - 1
    everyone_y = (height - gaming_pole_height) // 2 - 1

    Border(left_x, everyone_y, gaming_pole_width + 1, 1)
    Border(left_x, everyone_y + gaming_pole_height, gaming_pole_width + 1, 1)
    Border(left_x, everyone_y, 1, gaming_pole_height + 1)
    Border(left_x + gaming_pole_width, everyone_y, 1, gaming_pole_height + 1)

    Border(right_x, everyone_y, gaming_pole_width + 1, 1)
    Border(right_x, everyone_y + gaming_pole_height, gaming_pole_width + 1, 1)
    Border(right_x, everyone_y, 1, gaming_pole_height + 1)
    Border(right_x + gaming_pole_width, everyone_y, 1, gaming_pole_height + 1)

    first_player = generate_level(load_level('map1.6.txt'), 1,
                                  left_x + 1, everyone_y + 1)
    second_player = generate_level(load_level('map1.7.txt'), 2,
                                   right_x + 1, everyone_y + 1)

    f_players_group.add(first_player)
    s_players_group.add(second_player)

    pygame.mouse.set_visible(False)

    running = True
    t = 0
    pause = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause:
                    x, y = pygame.mouse.get_pos()
                    if width // 2 - text_x // 2 - 10 < x < width // 2 - text_x // 2 - 10 + text_x + 20:
                        if height // 3 - 10 < y < height // 3 - 10 + text2_y:
                            running = False
                            n.showFullScreen()
                        elif height // 3 * 2 - 10 < y < height // 3 * 2 - 10 + text2_y:
                            running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    if pause:
                        pause = False
                        pygame.mouse.set_visible(False)
                        screen.fill('black')
                    else:
                        pause = True
                        pygame.mouse.set_visible(True)

                if not pause:
                    if event.key == pygame.K_e:
                        first_player.check_doors(1)
                    if event.key == pygame.K_SLASH:
                        second_player.check_doors(2)
                    if event.key == pygame.K_w:
                        first_player.move_up(50, 1)
                        if duplicate_for_f_pl is not None:
                            duplicate_for_f_pl.move_up(50, 1)
                    if event.key == pygame.K_a:
                        first_player.move_l(50, 1)
                        if duplicate_for_f_pl is not None:
                            duplicate_for_f_pl.move_l(50, 1)
                    if event.key == pygame.K_s:
                        first_player.move_down(50, 1)
                        if duplicate_for_f_pl is not None:
                            duplicate_for_f_pl.move_down(50, 1)
                    if event.key == pygame.K_d:
                        first_player.move_r(50, 1)
                        if duplicate_for_f_pl is not None:
                            duplicate_for_f_pl.move_r(50, 1)
                    if event.key == pygame.K_LEFT:
                        second_player.move_l(50, 2)
                        if duplicate_for_s_pl is not None:
                            duplicate_for_s_pl.move_l(50, 2)
                    if event.key == pygame.K_DOWN:
                        second_player.move_down(50, 2)
                        if duplicate_for_s_pl is not None:
                            duplicate_for_s_pl.move_down(50, 2)
                    if event.key == pygame.K_UP:
                        second_player.move_up(50, 2)
                        if duplicate_for_s_pl is not None:
                            duplicate_for_s_pl.move_up(50, 2)
                    if event.key == pygame.K_RIGHT:
                        second_player.move_r(50, 2)
                        if duplicate_for_s_pl is not None:
                            duplicate_for_s_pl.move_r(50, 2)

        if not pause:
            t = (t + 1) % 4
            if t == 0:
                first_player.update()
                second_player.update()
        player1_tiles_group.draw(screen)
        player1_box_group.draw(screen)

        player2_tiles_group.draw(screen)
        player2_box_group.draw(screen)

        f_players_group.draw(screen)
        s_players_group.draw(screen)

        if pause:
            fpause()

        pygame.display.flip()
        clock.tick(FPS)
        if not running:
            screen.fill('black')
            f_players_group.empty()
            s_players_group.empty()
            player2_box_group.empty()
            player1_box_group.empty()
            player2_tiles_group.empty()
            player1_tiles_group.empty()
    pygame.quit()
    if n.isVisible():
        pass
    else:
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Main()
    n.showFullScreen()
    sys.exit(app.exec())
