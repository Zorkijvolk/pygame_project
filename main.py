import os
import sys
import pygame
import datetime as dt
from pathlib import Path
from winshell import desktop
from win32com.client import Dispatch
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt


# класс начального экрана
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
        self.startButton.move((screen_w - button_size[0]) // 2, 350)
        self.startButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.startButton.setFont(font)

        self.settingsButton = QPushButton('settings', self)
        self.settingsButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.settingsButton.move((screen_w - button_size[0]) // 2, 550)
        self.settingsButton.resize(button_size[0], button_size[1])
        self.settingsButton.setFont(font)

        self.exitButton = QPushButton('exit', self)
        self.exitButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.exitButton.move((screen_w - button_size[0]) // 2, 750)
        self.exitButton.resize(button_size[0], button_size[1])
        self.exitButton.setFont(font)

        self.backButton = QPushButton('back', self)
        self.backButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.backButton.resize(100, 100)
        self.backButton.move(10, 10)
        self.backButton.setFont(font)
        self.backButton.hide()

        self.desktopButton = QPushButton('create a desktop shortcut', self)
        self.desktopButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.desktopButton.resize(button_size[0], button_size[1])
        self.desktopButton.move((screen_w - button_size[0]) // 2, 150)
        self.desktopButton.setFont(font)
        self.desktopButton.hide()

        self.resetButton = QPushButton('reset statistics', self)
        self.resetButton.setStyleSheet('''font-size: 20pt; background-color: blue;''')
        self.resetButton.resize(button_size[0], button_size[1])
        self.resetButton.move((screen_w - button_size[0]) // 2, 550)
        self.resetButton.setFont(font)
        self.resetButton.hide()

        self.startButton.clicked.connect(self.start)
        self.exitButton.clicked.connect(lambda x: self.close())
        self.settingsButton.clicked.connect(self.settings)
        self.backButton.clicked.connect(self.first_page)
        self.desktopButton.clicked.connect(self.desktop)
        self.resetButton.clicked.connect(self.reset_statistic)

        self.nameProject = QLabel('THE MAZE', self)
        self.nameProject.resize(self.screen().size().width(), 200)
        self.nameProject.move(0, 0)
        self.nameProject.setStyleSheet('''font-size: 80pt;
               background-color: blue;''')
        self.nameProject.setFont(font)
        self.nameProject.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # функция, запускающая основной экран
    def start(self):
        self.hide()
        start_game()

    # функция, открывающая настройки
    def settings(self):
        self.startButton.hide()
        self.exitButton.hide()
        self.nameProject.hide()
        self.settingsButton.hide()
        self.backButton.show()
        self.resetButton.show()
        self.desktopButton.show()

    # функция, возвращающая начальный экран
    def first_page(self):
        self.startButton.show()
        self.exitButton.show()
        self.nameProject.show()
        self.settingsButton.show()
        self.backButton.hide()
        self.resetButton.hide()
        self.desktopButton.hide()

    # функция, которая создаёт ярлык на рабочий стол.
    def desktop(self):
        t = os.path.abspath('__Main__')[:-8]
        target = rf"{t}TheMaze.exe"
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(Path(desktop()) / "TheMaze.lnk"))
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = str(Path(target).parent)
        shortcut.IconLocation = target
        shortcut.save()

    # функция, которая обнуляет статистику.
    def reset_statistic(self):
        t = open('data/record.txt', 'w', encoding='UTF-8')
        t.write('0')
        t.close()


# функция загрузки изображения.
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


# функция загрузки карт.
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# функция создания карт.
def generate_level(level, n_player, m_x=0, m_y=0, new_level=0):
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
                        new_player = Player(x, y, m_x, m_y, 6, 1, 1)
                    else:
                        new_player = Player(x, y, m_x, m_y, 7, 1, 2)
                elif new_level:
                    if n_player == 1:
                        first_player.rect.x = tile_width * x + m_x + 15
                        first_player.rect.y = tile_height * y + m_y + 5
                    else:
                        second_player.rect.x = tile_width * x + m_x + 15
                        second_player.rect.y = tile_height * y + m_y + 5
            elif level[y][x] == 'K':
                obj = Tile('empty', x, y, m_x, m_y)
                k = Key('key1', x, y, m_x, m_y)
                if n_player == 1:
                    if not key1:
                        key_interatc_group_1.add(k)
                elif n_player == 2:
                    if second_player is None:
                        key_drawing_group_2.add(k)
                    elif second_player.level > first_player.level:
                        key_drawing_group_2.add(k)
                    elif second_player.level == first_player.level:
                        if not key1:
                            key_drawing_group_2.add(k)
            elif level[y][x] == 'k':
                obj = Tile('empty', x, y, m_x, m_y)
                k = Key('key2', x, y, m_x, m_y)
                if n_player == 1:
                    if first_player is None:
                        key_drawing_group_1.add(k)
                    elif first_player.level > second_player.level:
                        key_drawing_group_1.add(k)
                    elif first_player.level == second_player.level:
                        if not key2:
                            key_drawing_group_1.add(k)
                elif n_player == 2:
                    if not key2:
                        key_interatc_group_2.add(k)
            elif level[y][x] == 'm':
                obj = Tile('key1', x, y, m_x, m_y)
            elif level[y][x] == 'n':
                obj = Door('north_door', x, y, m_x, m_y)
                if n_player == 1:
                    door_group_1.add(obj)
                    player1_tiles_group.add(obj)
                else:
                    player2_tiles_group.add(obj)
            elif level[y][x] == 's':
                obj = Door('south_door', x, y, m_x, m_y)
                if n_player == 1:
                    door_group_1.add(obj)
                    player1_tiles_group.add(obj)
                else:
                    player2_tiles_group.add(obj)
            elif level[y][x] == 'w':
                obj = Door('west_door', x, y, m_x, m_y)
                if n_player == 1:
                    door_group_1.add(obj)
                    player1_tiles_group.add(obj)
                else:
                    player2_tiles_group.add(obj)
            elif level[y][x] == 'e':
                obj = Door('east_door', x, y, m_x, m_y)
                if n_player == 1:
                    door_group_1.add(obj)
                    player1_tiles_group.add(obj)
                else:
                    player2_tiles_group.add(obj)
            elif level[y][x] == '1':
                obj = Door('north_door2', x, y, m_x, m_y)
                if n_player == 2:
                    door_group_2.add(obj)
                    player2_tiles_group.add(obj)
                else:
                    player1_tiles_group.add(obj)
            elif level[y][x] == '2':
                obj = Door('south_door2', x, y, m_x, m_y)
                if n_player == 2:
                    door_group_2.add(obj)
                    player2_tiles_group.add(obj)
                else:
                    player1_tiles_group.add(obj)
            elif level[y][x] == '3':
                obj = Door('west_door2', x, y, m_x, m_y)
                if n_player == 2:
                    door_group_2.add(obj)
                    player2_tiles_group.add(obj)
                else:
                    player1_tiles_group.add(obj)
            elif level[y][x] == '4':
                obj = Door('east_door2', x, y, m_x, m_y)
                if n_player == 2:
                    door_group_2.add(obj)
                    player2_tiles_group.add(obj)
                else:
                    player1_tiles_group.add(obj)
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


# класс границ экранов.
class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites, borders)
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface([w, h])


# класс дверей.
class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)
        self.type = tile_type


# класс тропинок.
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


# класс стен.
class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


# класс ключей
class Key(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, move_x, move_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x, tile_height * pos_y + move_y)


# класс, реализующий действия игроков
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, move_x, move_y, room, level, player, dupl=0):
        super().__init__(all_sprites)
        self.frames = [player_image_1, player_animation_1, player_image_2, player_animation_2]
        if (player == 1 and not dupl) or (player == 2 and dupl):
            self.cur_image = 0
        else:
            self.cur_image = 2
        self.image = self.frames[self.cur_image]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + move_x + 15, tile_height * pos_y + move_y + 5)
        self.m_x = move_x
        self.m_y = move_y
        self.level = level
        self.cur_room = room
        self.player = player
        self.key = 0
        self.staying_in_door = 0

    def update(self):
        if self.cur_image < 2:
            self.cur_image = 1 - self.cur_image
        else:
            self.cur_image = 5 - self.cur_image
        self.image = self.frames[self.cur_image]

    def move_l(self, m):
        global first_player_duplicate, second_player_duplicate
        self.rect.x -= m // 2
        if self.player == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.x += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x += m // 2
                if (self.cur_room - 1) % 4 and self != second_player_duplicate:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    key_drawing_group_1.empty()
                    key_interatc_group_1.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room - 1}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room -= 1
                    self.rect.x += (gaming_pole_width - m)
                    if self.cur_room == second_player.cur_room and self.level == second_player.level:
                        first_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                        (self.rect.y - self.m_y - 5) // tile_height,
                                                        second_player.m_x, second_player.m_y, self.cur_room, self.level,
                                                        2, 1)
                        second_player_duplicate = Player((second_player.rect.x - second_player.m_x - 15) // tile_width,
                                                         (second_player.rect.y - second_player.m_y - 5) // tile_height,
                                                         self.m_x, self.m_y, self.cur_room, self.level, 1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.x -= m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_1):
                    if self != second_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == second_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.x += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x += m // 2
                if (self.cur_room - 1) % 4 and self != first_player_duplicate:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    key_drawing_group_2.empty()
                    key_interatc_group_2.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room - 1}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room -= 1
                    self.rect.x += (gaming_pole_width - m)
                    if self.cur_room == first_player.cur_room and self.level == first_player.level:
                        first_player_duplicate = Player((first_player.rect.x - first_player.m_x - 15) // tile_width,
                                                        (first_player.rect.y - first_player.m_y - 5) // tile_height,
                                                        self.m_x, self.m_y, self.cur_room, self.level, 2, 1)
                        second_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                         (self.rect.y - self.m_y - 5) // tile_height,
                                                         first_player.m_x, first_player.m_y, self.cur_room, self.level,
                                                         1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.x -= m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_2):
                    if self != first_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == first_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0

    def move_r(self, m):
        global first_player_duplicate, second_player_duplicate
        self.rect.x += m // 2
        if self.player == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.x -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x -= m // 2
                if self.cur_room % 4 and self != second_player_duplicate:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    key_drawing_group_1.empty()
                    key_interatc_group_1.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room + 1}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room += 1
                    self.rect.x -= (gaming_pole_width - m)
                    if self.cur_room == second_player.cur_room and self.level == second_player.level:
                        first_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                        (self.rect.y - self.m_y - 5) // tile_height,
                                                        second_player.m_x, second_player.m_y, self.cur_room, self.level,
                                                        2, 1)
                        second_player_duplicate = Player((second_player.rect.x - second_player.m_x - 15) // tile_width,
                                                         (second_player.rect.y - second_player.m_y - 5) // tile_height,
                                                         self.m_x, self.m_y, self.cur_room, self.level, 1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.x += m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_1):
                    if self != second_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == second_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.x -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.x -= m // 2
                if self.cur_room % 4 and self != first_player_duplicate:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    key_drawing_group_2.empty()
                    key_interatc_group_2.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room + 1}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room += 1
                    self.rect.x -= (gaming_pole_width - m)
                    if self.cur_room == first_player.cur_room and self.level == first_player.level:
                        first_player_duplicate = Player((first_player.rect.x - first_player.m_x - 15) // tile_width,
                                                        (first_player.rect.y - first_player.m_y - 5) // tile_height,
                                                        self.m_x, self.m_y, self.cur_room, self.level, 2, 1)
                        second_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                         (self.rect.y - self.m_y - 5) // tile_height,
                                                         first_player.m_x, first_player.m_y, self.cur_room, self.level,
                                                         1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.x += m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_2):
                    if self != first_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == first_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0

    def move_up(self, m):
        global first_player_duplicate, second_player_duplicate
        self.rect.y -= m // 2
        if self.player == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.y += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y += m // 2
                if self.cur_room - 4 > 0 and self != second_player_duplicate:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    key_drawing_group_1.empty()
                    key_interatc_group_1.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room - 4}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room -= 4
                    self.rect.y += (gaming_pole_height - m)
                    if self.cur_room == second_player.cur_room and self.level == second_player.level:
                        first_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                        (self.rect.y - self.m_y - 5) // tile_height,
                                                        second_player.m_x, second_player.m_y, self.cur_room, self.level,
                                                        2, 1)
                        second_player_duplicate = Player((second_player.rect.x - second_player.m_x - 15) // tile_width,
                                                         (second_player.rect.y - second_player.m_y - 5) // tile_height,
                                                         self.m_x, self.m_y, self.cur_room, self.level, 1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.y -= m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_1):
                    if self != second_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == second_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.y += m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y += m // 2
                if self.cur_room - 4 > 0 and self != first_player_duplicate:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    key_drawing_group_2.empty()
                    key_interatc_group_2.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room - 4}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room -= 4
                    self.rect.y += (gaming_pole_height - m)
                    if self.cur_room == first_player.cur_room and self.level == first_player.level:
                        first_player_duplicate = Player((first_player.rect.x - first_player.m_x - 15) // tile_width,
                                                        (first_player.rect.y - first_player.m_y - 5) // tile_height,
                                                        self.m_x, self.m_y, self.cur_room, self.level, 2, 1)
                        second_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                         (self.rect.y - self.m_y - 5) // tile_height,
                                                         first_player.m_x, first_player.m_y, self.cur_room, self.level,
                                                         1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.y -= m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_2):
                    if self != first_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == first_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0

    def move_down(self, m):
        global first_player_duplicate, second_player_duplicate
        self.rect.y += m // 2
        if self.player == 1:
            if pygame.sprite.spritecollideany(self, player1_box_group):
                self.rect.y -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y -= m // 2
                if self.cur_room + 4 < 13 and self != second_player_duplicate:
                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    key_drawing_group_1.empty()
                    key_interatc_group_1.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room + 4}.txt'), 1, self.m_x, self.m_y)
                    self.cur_room += 4
                    self.rect.y -= (gaming_pole_height - m)
                    if self.cur_room == second_player.cur_room and self.level == second_player.level:
                        first_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                        (self.rect.y - self.m_y - 5) // tile_height,
                                                        second_player.m_x, second_player.m_y, self.cur_room, self.level,
                                                        2, 1)
                        second_player_duplicate = Player((second_player.rect.x - second_player.m_x - 15) // tile_width,
                                                         (second_player.rect.y - second_player.m_y - 5) // tile_height,
                                                         self.m_x, self.m_y, self.cur_room, self.level, 1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.y += m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_1):
                    if self != second_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == second_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0
        else:
            if pygame.sprite.spritecollideany(self, player2_box_group):
                self.rect.y -= m // 2
            elif pygame.sprite.spritecollideany(self, borders):
                self.rect.y -= m // 2
                if self.cur_room + 4 < 13 and self != first_player_duplicate:
                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    key_drawing_group_2.empty()
                    key_interatc_group_2.empty()
                    generate_level(load_level(f'map{self.level}.{self.cur_room + 4}.txt'), 2, self.m_x, self.m_y)
                    self.cur_room += 4
                    self.rect.y -= (gaming_pole_height - m)
                    if self.cur_room == first_player.cur_room and self.level == first_player.level:
                        first_player_duplicate = Player((first_player.rect.x - first_player.m_x - 15) // tile_width,
                                                        (first_player.rect.y - first_player.m_y - 5) // tile_height,
                                                        self.m_x, self.m_y, self.cur_room, self.level, 2, 1)
                        second_player_duplicate = Player((self.rect.x - self.m_x - 15) // tile_width,
                                                         (self.rect.y - self.m_y - 5) // tile_height,
                                                         first_player.m_x, first_player.m_y, self.cur_room, self.level,
                                                         1, 1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
                    else:
                        first_player_duplicate = None
                        second_player_duplicate = None
                        duplicate_group.empty()
            else:
                self.rect.y += m // 2
            if self.level == 3 and self.key:
                if pygame.sprite.spritecollideany(self, door_group_2):
                    if self != first_player_duplicate:
                        self.staying_in_door = 1
                        if self.staying_in_door == first_player.staying_in_door:
                            end_game()
                else:
                    self.staying_in_door = 0

    def interaction(self):
        global key1, key2, first_player_duplicate, second_player_duplicate
        if self.player == 1:
            if pygame.sprite.spritecollideany(self, door_group_1) and self.key:
                key1 = 0
                self.key = 0
                if self.level < 3:
                    self.level += 1

                    player1_tiles_group.empty()
                    player1_box_group.empty()
                    door_group_1.empty()
                    key_drawing_group_1.empty()
                    key_interatc_group_1.empty()
                    duplicate_group.empty()

                    self.cur_room = 6
                    generate_level(load_level(f'map{self.level}.6.txt'), 1, self.m_x, self.m_y, 1)
                    if first_player.cur_room == second_player.cur_room and first_player.level == second_player.level:
                        first_player_duplicate = Player((first_player.rect.x - first_player.m_x - 15) // tile_width,
                                                        (first_player.rect.y - first_player.m_y - 5) // tile_height,
                                                        second_player.m_x, second_player.m_y, second_player.cur_room,
                                                        self.level, 2,
                                                        1)
                        second_player_duplicate = Player((second_player.rect.x - second_player.m_x - 15) // tile_width,
                                                         (second_player.rect.y - second_player.m_y - 5) // tile_height,
                                                         first_player.m_x, first_player.m_y, first_player.cur_room,
                                                         self.level, 1,
                                                         1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
            elif pygame.sprite.spritecollideany(self, key_interatc_group_1):
                key1 = 1
                self.key = 1
                key_interatc_group_1.empty()
                if self.level == second_player.level:
                    key_drawing_group_2.empty()
        elif self.player == 2:
            if pygame.sprite.spritecollideany(self, door_group_2) and self.key:
                key2 = 0
                self.key = 0
                if self.level < 3:
                    self.level += 1

                    player2_tiles_group.empty()
                    player2_box_group.empty()
                    door_group_2.empty()
                    key_drawing_group_2.empty()
                    key_interatc_group_2.empty()
                    duplicate_group.empty()

                    self.cur_room = 7
                    generate_level(load_level(f'map{self.level}.7.txt'), 2, self.m_x, self.m_y, 1)
                    if first_player.cur_room == second_player.cur_room and first_player.level == second_player.level:
                        first_player_duplicate = Player((first_player.rect.x - first_player.m_x - 15) // tile_width,
                                                        (first_player.rect.y - first_player.m_y - 5) // tile_height,
                                                        second_player.m_x, second_player.m_y, second_player.cur_room,
                                                        self.level, 2,
                                                        1)
                        second_player_duplicate = Player((second_player.rect.x - second_player.m_x - 15) // tile_width,
                                                         (second_player.rect.y - second_player.m_y - 5) // tile_height,
                                                         first_player.m_x, first_player.m_y, first_player.cur_room,
                                                         self.level, 1,
                                                         1)
                        duplicate_group.add(first_player_duplicate)
                        duplicate_group.add(second_player_duplicate)
            elif pygame.sprite.spritecollideany(self, key_interatc_group_2):
                key2 = 1
                self.key = 1
                key_interatc_group_2.empty()
                if self.level == first_player.level:
                    key_drawing_group_1.empty()


width, height, player, tile_images, screen = None, None, None, None, None
gaming_pole_width, gaming_pole_height, left_x, right_x, everyone_y, final1, final2 = 0, 0, 0, 0, 0, 0, 0
text_x, text1_y, text2_y = None, None, None
first_player, second_player = None, None
key1, key2 = 0, 0
tile_width = tile_height = 50
tile_count_w = 15
tile_count_h = 15
player_image_1, player_animation_1 = None, None
player_image_2, player_animation_2 = None, None
first_player_duplicate = None
second_player_duplicate = None
move_duplicate = 0
all_sprites = pygame.sprite.Group()

player1_tiles_group = pygame.sprite.Group()
player1_box_group = pygame.sprite.Group()

player2_tiles_group = pygame.sprite.Group()
player2_box_group = pygame.sprite.Group()

f_players_group = pygame.sprite.Group()
s_players_group = pygame.sprite.Group()
duplicate_group = pygame.sprite.Group()

door_group_1 = pygame.sprite.Group()
door_group_2 = pygame.sprite.Group()

key_drawing_group_1 = pygame.sprite.Group()
key_drawing_group_2 = pygame.sprite.Group()
key_interatc_group_1 = pygame.sprite.Group()
key_interatc_group_2 = pygame.sprite.Group()

borders = pygame.sprite.Group()

time1 = 0
time2 = dt.datetime.now()
delta = dt.timedelta()


# Функция, которая запускает финальный экран.
def end_game():
    global first_player_duplicate, second_player_duplicate
    global text_x, text1_y, text2_y, time1, time2, delta, key1, key2
    pygame.mouse.set_visible(True)
    f_players_group.empty()
    s_players_group.empty()
    duplicate_group.empty()
    player1_tiles_group.empty()
    player1_box_group.empty()
    player2_tiles_group.empty()
    player2_box_group.empty()
    door_group_1.empty()
    door_group_2.empty()
    time1 = dt.datetime.now()
    delta = time1 - time2
    time2 = time1
    first_player_duplicate = None
    second_player_duplicate = None
    key_drawing_group_1.empty()
    key_drawing_group_2.empty()
    key_interatc_group_1.empty()
    key_interatc_group_2.empty()
    key1 = 0
    key2 = 0
    screen.fill('black')
    font = pygame.font.Font(None, 80)
    text1 = font.render("Выйти в меню", True, (0, 255, 0))
    text2 = font.render('Выйти из игры', True, (0, 255, 0))
    f = open('data/record.txt').readline().strip()
    font = pygame.font.Font(None, 80)
    if 5000 - delta.seconds > int(f):
        text4 = font.render(f'NEW RECORD!!!', True, (255, 0, 0))
        t = open('data/record.txt', 'w')
        t.write(str(5000 - delta.seconds))
    else:
        text4 = font.render(f'Best Score: {f}', True, (255, 0, 0))
    text3 = font.render(f"score:{5000 - delta.seconds}", True, (255, 0, 0))
    text5 = font.render("YOU WIN!!!", True, (255, 0, 0))
    screen.blit(text3, (width // 2 - text3.get_width() // 2, height // 10 * 4))
    screen.blit(text4, (width // 2 - text4.get_width() // 2, height // 10 * 5))
    text_x = text2.get_width()
    text1_y = text1.get_height()
    text2_y = text2.get_height()
    screen.blit(text1, (width // 2 - text1.get_width() // 2, height // 10 * 8))
    screen.blit(text2, (width // 2 - text2.get_width() // 2, height // 10 * 9))
    screen.blit(text5, (width // 2 - text5.get_width() // 2, height // 10))
    pygame.draw.rect(screen, (255, 215, 0), (width // 2 - text2.get_width() // 2 - 10, height // 10 * 8 - 10,
                                             text2.get_width() + 20, text2.get_height() + 20), 10)
    pygame.draw.rect(screen, (255, 215, 0), (width // 2 - text2.get_width() // 2 - 10, height // 10 * 9 - 10,
                                             text2.get_width() + 20, text2.get_height() + 20), 10)


# Функция, которая запускает основной экран.
def start_game():
    global width, height, player, tile_images, tile_width, tile_height, screen
    global gaming_pole_width, gaming_pole_height, left_x, right_x, everyone_y, first_player, second_player
    global player_image_1, player_animation_1, player_image_2, player_animation_2, move_duplicate
    global final1, final2
    global text_x, text1_y, text2_y
    pygame.init()

    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    player = None
    player_image_1 = load_image('player.png', -1)
    player_animation_1 = load_image('player2.png', -1)
    player_image_2 = load_image('player1.1.png', -1)
    player_animation_2 = load_image('player1.2.png', -1)

    tile_images = {
        'wall': load_image('brick.png'),
        'empty': load_image('path.png'),
        'north_door': load_image('door_opened.png'),
        'east_door': load_image('door_opened_east.png'),
        'west_door': load_image('door_opened_west.png'),
        'south_door': load_image('door_opened_south.png'),
        'north_door2': load_image('door2_opened.png'),
        'east_door2': load_image('door2_opened_east.png'),
        'west_door2': load_image('door2_opened_west.png'),
        'south_door2': load_image('door2_opened_south.png'),
        'key1': load_image('key1.png'),
        'key2': load_image('key2.png')}

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
                if first_player.staying_in_door and second_player.staying_in_door:
                    x, y = pygame.mouse.get_pos()
                    if width // 2 - text_x // 2 - 10 < x < width // 2 - text_x // 2 - 10 + text_x + 20:
                        if height // 10 * 8 - 10 < y < height // 10 * 8 - 10 + text2_y:
                            running = False
                            n.showFullScreen()
                        elif height // 10 * 9 - 10 < y < height // 10 * 9 - 10 + text2_y:
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
                        first_player.interaction()
                    if event.key == pygame.K_SLASH:
                        second_player.interaction()
                    if event.key == pygame.K_w:
                        if first_player_duplicate is not None:
                            first_player_duplicate.move_up(50)
                        first_player.move_up(50)
                    if event.key == pygame.K_a:
                        if first_player_duplicate is not None:
                            first_player_duplicate.move_l(50)
                        first_player.move_l(50)
                    if event.key == pygame.K_s:
                        if first_player_duplicate is not None:
                            first_player_duplicate.move_down(50)
                        first_player.move_down(50)
                    if event.key == pygame.K_d:
                        if first_player_duplicate is not None:
                            first_player_duplicate.move_r(50)
                        first_player.move_r(50)
                    if event.key == pygame.K_LEFT:
                        if second_player_duplicate is not None:
                            second_player_duplicate.move_l(50)
                        second_player.move_l(50)
                    if event.key == pygame.K_DOWN:
                        if second_player_duplicate is not None:
                            second_player_duplicate.move_down(50)
                        second_player.move_down(50)
                    if event.key == pygame.K_UP:
                        if second_player_duplicate is not None:
                            second_player_duplicate.move_up(50)
                        second_player.move_up(50)
                    if event.key == pygame.K_RIGHT:
                        if second_player_duplicate is not None:
                            second_player_duplicate.move_r(50)
                        second_player.move_r(50)
        if not pause:
            t = (t + 1) % 5
            if t == 0:
                first_player.update()
                second_player.update()
                if first_player_duplicate is not None:
                    first_player_duplicate.update()
                    second_player_duplicate.update()
        player1_tiles_group.draw(screen)
        player1_box_group.draw(screen)

        player2_tiles_group.draw(screen)
        player2_box_group.draw(screen)

        key_interatc_group_1.draw(screen)
        key_interatc_group_2.draw(screen)
        key_drawing_group_1.draw(screen)
        key_drawing_group_2.draw(screen)

        f_players_group.draw(screen)
        s_players_group.draw(screen)
        duplicate_group.draw(screen)

        if pause:
            fpause()

        pygame.display.flip()
        clock.tick(FPS)
        if not running:
            screen.fill('black')
            f_players_group.empty()
            s_players_group.empty()
            player1_tiles_group.empty()
            player1_box_group.empty()
            player2_tiles_group.empty()
            player2_box_group.empty()
            duplicate_group.empty()
            door_group_1.empty()
            door_group_2.empty()
    pygame.quit()
    if n.isVisible():
        pass
    else:
        sys.exit()


# начало программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Main()
    n.showFullScreen()
    sys.exit(app.exec())
