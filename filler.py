import random
import sys
import copy
import os
import pygame
from pygame.locals import *

# номера цветов для игры
COLORS = {0: 'black',
          1: 'red',
          2: 'green',
          3: 'blue',
          4: 'yellow',
          5: 'orange',
          6: 'magenta',
          7: 'cyan',
          8: 'gray',
          }

# цвет текста
TEXTCOLOR = 'white'
TEXTSHADOWCOLOR = 'gray'
# характеристики уровней: ширина, высота, размер квадрата, количество цветов,
# вероятность случайного хода соперника
LEVELS = {1: (11, 11, 50, 5, 60),
          2: (11, 11, 50, 6, 55),
          3: (15, 15, 36, 5, 50),
          4: (15, 15, 36, 6, 45),
          5: (23, 23, 24, 6, 40),
          6: (23, 23, 24, 7, 35),
          7: (31, 31, 18, 6, 30),
          8: (31, 31, 18, 7, 20),
          9: (35, 35, 15, 7, 10),
          10: (35, 35, 15, 8, 5)
          }


class Board:
    """ Класс для представления игрового поля
        Парамер инициализатора - уровень игры, по умолчанию 1
    """

    def __init__(self, level=1):
        """ Метод инициализации игрового поля """
        width, height, cell_size, colors, prob = LEVELS[10 if level >= 10 else level]
        # уровень
        self.level = level
        # вероятность случайного хода
        self.prob = prob
        # количество цветов
        self.colors = colors
        # ширина поля
        self.width = width
        # высота поля
        self.height = height
        # размер клетки
        self.cell_size = cell_size
        # собственно поле
        self.board = [[0] * width for _ in range(height)]
        # координаты поля
        self.top = 10
        self.left = (size[0] - width * self.cell_size) // 2
        # очки человека
        self.human = 0
        # очки компьютера
        self.computer = 0
        # глобальный счетчик очков для рекурсии
        self.counter = 0
        # победные очки
        self.win_score = width * height // 2

    def random_fill(self):
        """ случайное заполнение поля """
        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i] = random.randint(1, self.colors)
        # делаем разные цвета углов для игроков
        while self.board[self.width - 1][self.height - 1] == self.board[0][0]:
            self.board[self.width - 1][self.height - 1] = random.randint(1, self.colors)

    def render(self, board, alpha=255):
        """ отображение поля возможно с прозрачностью """
        # для прозрачности делаем холст в памяти
        tempSurf = pygame.Surface(screen.get_size())
        tempSurf = tempSurf.convert_alpha()
        tempSurf.fill((0, 0, 0, 0))

        for i in range(self.width):
            for j in range(self.height):
                x = self.left + self.cell_size * i
                y = self.top + self.cell_size * j
                r, g, b, _ = pygame.Color(COLORS[board[j][i]])
                pygame.draw.rect(tempSurf,
                                 (r, g, b, alpha),
                                 (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(tempSurf,
                                 pygame.Color(pygame.Color('white')),
                                 (x, y, self.cell_size, self.cell_size), 1)

        # pygame.draw.rect(tempSurf, pygame.Color('black'), (left-1, top-1, boxSize * boardWidth + 1, boxSize * boardHeight + 1), 1)
        screen.blit(tempSurf, (0, 0))

    def make_human_move(self, newcolor, animationSpeed=25):
        """ метод делает ход человека newcolor """
        # если нельзя сделать ход - выходим
        if newcolor in self.get_impossible_colors():
            return

        # запоминаем старое поле
        origBoard = copy.deepcopy(self.board)
        # делаем ход
        self.flood_fill(self.board, self.board[0][0], newcolor, 0, 0)

        # анимация, отображающая ход
        for transparency in range(0, 255, animationSpeed):
            self.render(origBoard)
            self.render(self.board, transparency)
            pygame.display.update()
            clock.tick(fps)

        # делаем ход компьютера
        self.make_AI_move()

    def make_AI_move(self, animationSpeed=25):
        """ метод делает ход за компьютер"""
        # возможные цвета
        possible_colors = list(set(range(1, self.colors + 1)) -
                               set(self.get_impossible_colors())
                               )
        # находим самый лучший ход
        scores = []
        for col in possible_colors:
            countBoard = copy.deepcopy(self.board)
            self.flood_fill(countBoard, self.board[self.width - 1][self.height - 1],
                            col, self.width - 1, self.height - 1)
            self.counter = 0
            self.flood_fill(countBoard, col, 0, self.width - 1, self.height - 1)
            scores.append((self.counter, col))
        newcolor = max(scores)[1]

        # c определенной вероятностью делаем случайный ход
        if random.randint(1, 100) <= self.prob:
            newcolor = random.choice(possible_colors)

        # делаем ход
        origBoard = copy.deepcopy(self.board)
        self.flood_fill(self.board, self.board[self.width - 1][self.height - 1],
                        newcolor, self.width - 1, self.height - 1)

        # анимируем ход компьютера
        for transparency in range(0, 255, animationSpeed):
            self.render(origBoard)
            self.render(self.board, transparency)
            pygame.display.update()
            clock.tick(fps)

    def flood_fill(self, board, oldColor, newColor, x, y):
        """ метод реализует рекурсивный алгоритм заливки
            board - поле,
            oldColor - исходный цвет,
            newColor - новый цвет,
            x, y - стартовая точка
        """
        # если цвет не подходит - выходим
        if oldColor == newColor or board[x][y] != oldColor:
            return

        board[x][y] = newColor  # изменить цвет
        self.counter += 1

        # рекурсивно вызываем для всех соседей
        if x > 0:
            self.flood_fill(board, oldColor, newColor, x - 1, y)
        if x < self.width - 1:
            self.flood_fill(board, oldColor, newColor, x + 1, y)
        if y > 0:
            self.flood_fill(board, oldColor, newColor, x, y - 1)
        if y < self.height - 1:
            self.flood_fill(board, oldColor, newColor, x, y + 1)

    def draw_status(self):
        """ метод отображает статус игры: очки и уровень """

        # считаем очки игрока
        countBoard = copy.deepcopy(self.board)
        self.counter = 0
        self.flood_fill(countBoard, self.board[0][0], 0, 0, 0)
        self.human = self.counter

        # считаем очки компьютера
        self.counter = 0
        self.flood_fill(countBoard,
                        self.board[self.width - 1][self.height - 1],
                        0,
                        self.width - 1, self.height - 1)
        self.computer = self.counter

        # отображаем очки игрока
        show_message(20, 20, f'Игрок: {self.human}', basicfont)
        if not (human_img is None):
            screen.blit(human_img, (20, 60))

        # отображаем очки компьютера
        show_message(size[0] - 150, 20, f'Робот: {self.computer}', basicfont)
        if not (robot_img is None):
            screen.blit(robot_img, (size[0] - 150, 60))

        # отображаем уровень
        show_message(20, size[1] - 100, f'Уровень {self.level}', basicfont)

        # отображаем очки игрока
        show_message(20, size[1] - 70, f'Очки {score + self.human * self.level}',
                     basicfont)

    def check_win(self):
        """ метод проверяет окончание уровня """
        # игрок победил
        if self.human > self.win_score:
            show_text(f'Победа {self.human}:{self.computer}', middlefont)
            return 1
        # игрок проиграл
        elif self.computer > self.win_score:
            show_text(f'Проигрыш {self.human}:{self.computer}', middlefont)
            return -1
        else:
            return 0

    def get_impossible_colors(self):
        """ метод возвращает цвета, невозможные для выбора на текущем ходу """
        impossible_colors = [self.board[0][0],
                             self.board[self.width - 1][self.height - 1]]
        return impossible_colors


class Palette:
    """ Класс для представления палитры
        Парамер инициализатора - количество цветов
    """

    def __init__(self, width=5):
        """ Метод инициализации палитры"""
        self.width = width
        self.height = 1
        self.board = list(range(1, width + 1))
        self.top = 600
        self.cell_size = 60
        self.left = (size[0] - width * self.cell_size) // 2
        self.current = 0

    def render(self):
        """ Метод отображения палитры """
        i = 0
        impossible_colors = board.get_impossible_colors()
        for j in range(self.width):
            x = self.left + self.cell_size * j
            y = self.top
            if j + 1 in impossible_colors:
                # невозможный цвет
                pygame.draw.rect(screen,
                                 pygame.Color(COLORS[self.board[j]]),
                                 (x + 5, y + self.cell_size // 3,
                                  self.cell_size - 10, self.cell_size // 3))
            else:
                # возможный цвет
                pygame.draw.rect(screen,
                                 pygame.Color(COLORS[self.board[j]]),
                                 (x, y, self.cell_size, self.cell_size))
            if j == self.current:
                # выбранный цвет
                pygame.draw.rect(screen,
                                 pygame.Color(pygame.Color('white')),
                                 (x, y, self.cell_size, self.cell_size), 5)
            else:
                # невыбранный цвет
                pygame.draw.rect(screen,
                                 pygame.Color(pygame.Color('white')),
                                 (x, y, self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        """ Метод обрабатывает нажатие кнопки мыши"""
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, mouse_pos):
        """ Метод возвращает координаты клетки, где нажата кнопка мыши"""
        x, y = mouse_pos[0] - self.left, mouse_pos[1] - self.top
        i, j = (x + self.cell_size - 1) // self.cell_size, (y + self.cell_size - 1) // self.cell_size
        if self.check(i - 1, j - 1):
            return i - 1, j - 1
        return None

    def on_click(self, cell_coords):
        """ Метод делает действие при нажатии кнопки мыши"""
        x, y = cell_coords
        board.make_human_move(x + 1)

    def check(self, x, y):
        """ Метод проверяет валидность координат клетки """
        return 0 <= x < self.width and 0 <= y < self.height


def terminate():
    """ Функция прерывает игру """
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


def check_keys():
    """ Функция проверяет кнопки на экране с надписью """
    for event in pygame.event.get(QUIT):
        terminate()

    for event in pygame.event.get(MOUSEBUTTONDOWN):
        return True

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        if event.key == K_ESCAPE:
            terminate()
        return event.key
    return None


def make_text(text, font, color=TEXTCOLOR):
    """ Функция создает холст с текстом и возвращает его и область """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def show_message(x, y, text="", font=None, color=TEXTCOLOR):
    """ Функция отображает сообщение в нужной точке """
    surf, rect = make_text(text, font, color)
    rect.topleft = (x, y)
    screen.blit(surf, rect)


def show_text(text, font):
    """ Функция показывает текст в середине экрана """
    # Рисует тень
    titleSurf, titleRect = make_text(text, font, pygame.Color(TEXTSHADOWCOLOR))
    titleRect.center = (size[0] // 2 + 2, size[1] // 2 + 2)
    screen.blit(titleSurf, titleRect)

    # Рисует текст
    titleSurf, titleRect = make_text(text, font, TEXTCOLOR)
    titleRect.center = (size[0] // 2 - 2, size[1] // 2 - 2)
    screen.blit(titleSurf, titleRect)

    # Рисует надпись нажмите любую клавишу
    pressKeySurf, pressKeyRect = make_text('ESC - выход, любая клавиша - продолжить', basicfont, TEXTCOLOR)
    pressKeyRect.center = (size[0] // 2, size[1] // 2 + 100)
    screen.blit(pressKeySurf, pressKeyRect)

    pygame.event.clear()
    while check_keys() == None:
        pygame.display.update()
        clock.tick(fps)


def load_image(name, colorkey=None):
    """ Функция загружает изображение """
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


def load_records():
    """ Функция загружает таблицу рекордов """
    try:
        f = open('data/records.csv', 'r', encoding="utf-8")
    except:
        f = open('data/records.csv', 'wt', encoding="utf-8")
        f.close()
        f = open('data/records.csv', 'r', encoding="utf-8")
    records = []
    for s in f.readlines():
        s = s.strip()
        name, level, score = s.split(";")
        records.append((name, level, score))
    f.close()
    records.sort(key=lambda x: int(x[2]), reverse=True)
    records = records[:10]
    return records


def save_records(records):
    """ Функция сохраняет таблицу рекордов """
    f = open('data/records.csv', 'wt', encoding="utf-8")
    for x, y, z in records:
        f.write(f"{x};{y};{z}\n")
    f.close()


def show_records(records):
    """ Функция выводит таблицу рекордов """
    show_message(50, 20, "Лучшие результаты", middlefont, 'green')
    show_message(30, 120, "N", recordfont, 'yellow')
    show_message(100, 120, "Игрок", recordfont, 'yellow')
    show_message(550, 120, "Уровень", recordfont, 'yellow')
    show_message(750, 120, "Очки", recordfont, 'yellow')
    for i in range(len(records)):
        show_message(30, 175 + 40 * i, f"{i + 1}", recordfont)
        show_message(100, 175 + 40 * i, f"{records[i][0][:25]}", recordfont)
        show_message(680, 175 + 40 * i, f"{int(records[i][1]):2d}", recordfont)
        show_message(750, 175 + 40 * i, f"{int(records[i][2]):5d}", recordfont)


def game_over(level, score):
    """ Функция в конце игры показывает экран с таблицей рекордов
    и обновляет ее
    """
    # если файл не существует, то выходим
    records = load_records()

    # иницализируем поле ввода имени игрока
    input_box = pygame.Rect(300, 600, 150, 32)
    color = pygame.Color('dodgerblue2')
    text = 'Имя игрока'
    active = True
    done = False
    pygame.event.clear()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not active:
                    done = True
            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        # добавляем запись в таблицу рекордов
                        records.append((text, level, score))
                        records.sort(key=lambda x: int(x[2]), reverse=True)
                        records = records[:10]
                        save_records(records)
                        active = False
                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                else:
                    if event.key == K_ESCAPE:
                        terminate()
                    done = True

        screen.fill((0, 0, 0))
        show_records(records)
        if active:
            # отображаем поле ввода имени игрока
            show_message(150, 605, "Ваше имя:", basicfont)
            txt_surface = basicfont.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.width = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
        else:
            show_message(150, 600, 'ESC - выход, любая клавиша - продолжить', basicfont)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    # инициализация
    pygame.init()
    pygame.display.set_caption('Битва за цвет')
    size = width, height = 900, 700
    clock = pygame.time.Clock()
    fps = 30

    # установка шрифтов
    basicfont = pygame.font.Font('data/freesansbold.ttf', 24)
    recordfont = pygame.font.Font('data/freesansbold.ttf', 40)
    middlefont = pygame.font.Font('data/freesansbold.ttf', 80)
    bigfont = pygame.font.Font('data/freesansbold.ttf', 120)
    screen = pygame.display.set_mode(size)

    # загрузка и масштабирование картинок
    try:
        human_img = load_image("human.png", colorkey=None)
        human_img = pygame.transform.scale(human_img, (130, 130))
        robot_img = load_image("robot.png", colorkey=None)
        robot_img = pygame.transform.scale(robot_img, (123, 123))
    except:
        human_img = None
        robot_img = None

    # заставка
    show_text('Битва за цвет', bigfont)

    # создаем поле, заполняем его, создаем палитру
    score = 0
    board = Board()
    board.random_fill()
    palette = Palette()

    # звпускаем музыку
    try:
        pygame.mixer.music.load('data/pesenka.mid')
        pygame.mixer.music.play(-1, 0.0)
    except:
        pass

    running = True
    pygame.event.clear()
    while running:
        # проверка на конец уровня
        win = board.check_win()
        if win:
            score += board.human * board.level
            if win > 0:
                # переход на следующий уровень
                level = board.level + 1
            else:
                # сохранение результата
                game_over(board.level, score)
                # возврат на начало игры
                level = 1
                score = 0
            # создаем поле, заполняем его, создаем палитру
            board = Board(level)
            board.random_fill()
            palette = Palette(LEVELS[level][3])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # выбран цвет в палитре
                palette.get_click(event.pos)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LEFT:
                    # меняем цвет в палитре
                    palette.current = (palette.current - 1) % palette.width
                elif event.key == K_RIGHT:
                    # меняем цвет в палитре
                    palette.current = (palette.current + 1) % palette.width
                elif event.key == K_RETURN or event.key == K_SPACE:
                    # выбран цвет в палитре
                    board.make_human_move(palette.current + 1)

        screen.fill((0, 0, 0))
        # рисуем поле
        board.render(board.board)
        # рисуем надписи
        board.draw_status()
        # рисуем палитру
        palette.render()
        pygame.display.update()
        clock.tick(fps)

    pygame.mixer.music.stop()
    pygame.quit()