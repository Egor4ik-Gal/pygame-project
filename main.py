import sys

import pygame
import os
from random import randrange, shuffle, choice

flag = True             # задаем переменные, загружаю картинки
flag_minigames1 = False
flag_minigames2 = False
flag_minigames3 = False
flag_minigames2_2 = False
size2 = w, h = 650, 350
screen = pygame.display.set_mode(size2)
clock = pygame.time.Clock()
fps = 60
speed = 20
bg0 = pygame.image.load(r'data\first_screen.png')
bg0_1 = pygame.image.load(r'data\authors.png')
bg = pygame.image.load(r'data\room1.png')
bg2 = pygame.image.load(r'data\room2sav3.png')
bg3 = pygame.image.load(r'data\room3sav3.png')
pr1 = pygame.image.load(r'data\pers1.png')
pr2 = pygame.image.load(r'data\pers1.1.png')
pr3 = pygame.image.load(r'data\pers1.2.png')
pr4 = pygame.image.load(r'data\pers1.22.png')
bg0_butt1 = pygame.image.load(r'data\firstbutt.png')
bg0_butt2 = pygame.image.load(r'data\secondbutt.png')
bg0_butt3 = pygame.image.load(r'data\back.png')
thing1 = pygame.image.load(r'data\cup.png')
thing2 = pygame.image.load(r'data\TV.png')
thing2_2 = pygame.image.load(r'data\vali.png')
thing3 = pygame.image.load(r'data\micro.png')
pr2.set_colorkey((255, 255, 255))

person = pygame.sprite.Sprite()
person.image = pr1
person.rect = person.image.get_rect()
person.rect.x = 0
person.rect.y = h - 205


##############################


def load_image(name, colorkey=None):      # функция для загрузки картинок
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:   # создается класс Board для клетчатого поля, ниже несколько мини-игр наследуются от него
    def __init__(self, screen):
        self.width = 10
        self.height = 10
        self.board = [[0] * 10 for _ in range(10)]
        self.left = 175
        self.top = 40
        self.cell_size = 30
        self.render(screen)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        print(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return self.on_click(cell)
        # else:
        #     print(cell)

    def render(self, screen):
        colors = [pygame.Color("black"), pygame.Color("white")]
        for y in range(self.height):
            for x in range(self.width):
                # pygame.draw.rect(screen, colors[self.board[y][x]], (
                #     x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                #     self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)


class Ball(pygame.sprite.Sprite):  # класс Ball для создания спрайтов в мини-игре CatchingBalls
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = 150 + randrange(315)
        self.rect.y = 0


class CatchingBalls:  #
    def __init__(self, screen, v=None):
        global flag_minigames1, flag_minigames2, flag_minigames3, room, flag_minigames2_2
        self.screen = screen
        pygame.draw.rect(screen, (255, 255, 255), (150, 0, 350, 350))
        pygame.draw.rect(screen, (200, 170, 100), (150, 400, 480, 80))
        font = pygame.font.Font(None, 30)
        text = font.render("Поймайте 30 шариков!", True, (0, 0, 0))
        text_x = 110
        text_y = 10
        screen.blit(text, (text_x, text_y))

        self.all_sprites = pygame.sprite.Group()
        self.basket = pygame.sprite.Sprite()
        self.basket.image = load_image("basket.png")
        self.basket.rect = self.basket.image.get_rect()
        self.all_sprites.add(self.basket)

        self.basket.rect.x = 150
        self.basket.rect.y = 250

        self.hard1 = pygame.sprite.Sprite()
        self.hard1.image = load_image("health.png")
        self.hard1.rect = self.basket.image.get_rect()
        self.all_sprites.add(self.hard1)

        self.hard1.rect.x = 465
        self.hard1.rect.y = 10

        self.hard2 = pygame.sprite.Sprite()
        self.hard2.image = load_image("health.png")
        self.hard2.rect = self.basket.image.get_rect()
        self.all_sprites.add(self.hard2)

        self.hard2.rect.x = 435
        self.hard2.rect.y = 10

        self.hard3 = pygame.sprite.Sprite()
        self.hard3.image = load_image("health.png")
        self.hard3.rect = self.basket.image.get_rect()
        self.all_sprites.add(self.hard3)

        self.hard3.rect.x = 405
        self.hard3.rect.y = 10

        self.all_sprites.draw(screen)

        # pygame.display.flip()
        # self.playing()
        if self.playing():
            font = pygame.font.Font(None, 40)
            text = font.render("Вы победили!!!", True, (100, 255, 100))
            text_x = 210
            text_y = 150
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20))
            screen.blit(text, (text_x, text_y))
            if room == 1:
                flag_minigames1 = True
            elif room == 2 and v == 0:
                flag_minigames2 = True
            elif room == 2 and v == 1:
                flag_minigames2_2 = True
            elif room == 3:
                flag_minigames3 = True
            running3()

        else:
            font = pygame.font.Font(None, 40)
            text = font.render("Вы проиграли!!!", True, (255, 0, 0))
            text_x = 210
            text_y = 150
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20))
            screen.blit(text, (text_x, text_y))
            running3()

    def playing(self):
        running = True

        CREATINGBALLS = pygame.USEREVENT + 1
        FALL = pygame.USEREVENT + 2
        pygame.time.set_timer(CREATINGBALLS, 900)
        count_of_fallen_balls = 0
        count_of_catched_balls = 0
        count = 0
        list_of_balls = []
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == CREATINGBALLS:
                    list_of_balls.append(Ball(self.all_sprites))
                    count += 1
                    if count == 33:
                        pygame.time.set_timer(CREATINGBALLS, 0)
                if event.type == FALL:
                    for i in range(len(list_of_balls)):
                        list_of_balls[i].rect.y += 1
                        if list_of_balls[i].rect.y == 310:
                            count_of_fallen_balls += 1
                            list_of_balls[i].kill()
                            list_of_balls.remove(list_of_balls[i])
                            if count_of_fallen_balls == 1:
                                self.hard3.kill()
                            if count_of_fallen_balls == 2:
                                self.hard2.kill()
                            if count_of_fallen_balls == 3:
                                self.hard1.kill()
                            break
                        if list_of_balls[i].rect.center[1] in range(270, 310) and \
                                list_of_balls[i].rect.center[0] in range(self.basket.rect.x, self.basket.rect.x + 100):
                            list_of_balls[i].kill()
                            count_of_catched_balls += 1
                            list_of_balls.remove(list_of_balls[i])
                            break
                if count == 1:
                    pygame.time.set_timer(FALL, 4)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.basket.rect.x > 145:
                    self.basket.rect.x -= 1
                    clock.tick(300)
            if keys[pygame.K_RIGHT]:
                if self.basket.rect.x < 435:
                    self.basket.rect.x += 1
                    clock.tick(300)
            pygame.draw.rect(self.screen, (255, 255, 255), (150, 0, 350, 350))
            pygame.draw.rect(self.screen, (200, 170, 100), (150, 300, 350, 60))
            font = pygame.font.Font(None, 30)
            text = font.render("Поймайте 30 шариков!", True, (0, 0, 0))
            text_x = 155
            text_y = 10
            self.screen.blit(text, (text_x, text_y))

            stroka = f'Вы поймали {count_of_catched_balls}/30'
            text2 = font.render(stroka, True, (0, 0, 0))
            text2_x = 155
            text2_y = 35
            self.screen.blit(text2, (text2_x, text2_y))
            self.all_sprites.draw(self.screen)
            # clock.tick(fps)
            pygame.display.flip()

            if count_of_fallen_balls >= 3:
                return False
            if count_of_catched_balls == 30:
                return True
        pygame.quit()


class SearchEmoji(Board):  # класс мини-игры SearchEmoji
    def __init__(self, screen, v=None):
        global flag_minigames1, flag_minigames2, flag_minigames3, room, flag_minigames2_2

        # на экран выводятся все надписи
        self.screen = screen
        pygame.draw.rect(screen, (100, 100, 100), (150, 0, 350, 350))
        self.n = randrange(1, 31)
        self.desired_emoji = load_image(f'emoji{self.n}.png')
        screen.blit(self.desired_emoji, (250, 6))
        self.desired_emoji_coords = (randrange(10), randrange(10))
        super().__init__(screen)
        font = pygame.font.Font(None, 30)
        text = font.render("Найдите:", True, (0, 0, 0))
        text_x = 155
        text_y = 10
        screen.blit(text, (text_x, text_y))
        self.time = 19
        text2 = font.render(str(self.time), True, (0, 0, 0))
        text2_x = 380
        text2_y = 10
        screen.blit(text2, (text2_x, text2_y))

        self.all_sprites = pygame.sprite.Group()

        # создаются спрайты показывающие количество "жизней"
        self.hard1 = pygame.sprite.Sprite()
        self.hard1.image = load_image("health.png")
        self.hard1.rect = self.hard1.image.get_rect()
        self.all_sprites.add(self.hard1)

        self.hard1.rect.x = 465
        self.hard1.rect.y = 6

        self.hard2 = pygame.sprite.Sprite()
        self.hard2.image = load_image("health.png")
        self.hard2.rect = self.hard2.image.get_rect()
        self.all_sprites.add(self.hard2)

        self.hard2.rect.x = 435
        self.hard2.rect.y = 6

        self.hard3 = pygame.sprite.Sprite()
        self.hard3.image = load_image("health.png")
        self.hard3.rect = self.hard3.image.get_rect()
        self.all_sprites.add(self.hard3)

        self.hard3.rect.x = 405
        self.hard3.rect.y = 6

        self.all_sprites.draw(screen)

        if self.playing(): # запускается игровой цикл мини-игры и проверяется выиграл пользователь или проиграл
            if room == 1:  # при победе проверяется в какой комнате была вызвана мини-игра и меняет флаг на True
                flag_minigames1 = True
            elif room == 2 and v == 0:  # переменная v - необязательная
                flag_minigames2 = True  # она нужна для различия двух мини-игр в одной комнате
            elif room == 2 and v == 1:
                flag_minigames2_2 = True
            elif room == 3:
                flag_minigames3 = True
            running3()  # запускает основной цикл

        else:
            minigames.append(1)  # при проигрыше возвращает мини-игру в список и запускает главный цикл
            running3()


    def playing(self):
        running = True

        # создается событие время истекло и запускается таймер
        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)

        # создается событие изменяющее оставшееся время на экране
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        a = 'playing'
        count_of_wrong_click = 0

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.get_click(event.pos): # проверка нажатия пользователя
                        a = 'win'
                    else:
                        # за неверный ответ отнимаетя одна "жизнь"
                        count_of_wrong_click += 1
                        if count_of_wrong_click == 1:
                            self.hard3.kill()
                        if count_of_wrong_click == 2:
                            self.hard2.kill()
                        if count_of_wrong_click == 3:
                            self.hard1.kill()
                if event.type == TIMERUNOUT: # проверка на истечение времени
                    a = 'defeat'
                if event.type == TIMER:
                    # уменьшение оставшегося времени выведенного на экране
                    self.time -= 1
            if a == 'win':
                # при победе возврвщается True
                return True
            if a == 'defeat' or count_of_wrong_click >= 3:
                # при поражерии возвращается False
                return False

            # всё рисуется на экране
            pygame.draw.rect(self.screen, (100, 100, 100), (150, 0, 350, 350))
            self.screen.blit(self.desired_emoji, (250, 6))
            font = pygame.font.Font(None, 30)
            text = font.render("Найдите:", True, (0, 0, 0))
            text_x = 155
            text_y = 10
            self.screen.blit(text, (text_x, text_y))
            text2 = font.render(str(self.time), True, (0, 0, 0))
            text2_x = 380
            text2_y = 10
            self.screen.blit(text2, (text2_x, text2_y))
            self.render(self.screen)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def render(self, screen): # функция отвечает за рисование всех смайликов на экране
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == 0: # клетка поля еще не заполнена
                    if (x, y) == self.desired_emoji_coords: # координаты совпадают с координатами искомого смайлика
                        # присвоение клетке номера смайлика и рисование смайлика на экране
                        self.board[x][y] = self.n
                        self.screen.blit(self.desired_emoji,
                                         (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                          self.cell_size, self.cell_size))
                    else:
                        # выбор случайного смайлика и его рисование на экране, присвоение клетке его ноиера
                        n = randrange(1, 31)
                        while n == self.n:
                            n = randrange(1, 31)
                        emoji = load_image(f'emoji{n}.png')
                        self.board[x][y] = n
                        self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                                 self.cell_size, self.cell_size))
                else:
                    # рисование смайлика на экране
                    emoji = load_image(f'emoji{self.board[x][y]}.png')
                    self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                             self.cell_size, self.cell_size))

    def on_click(self, cell):
        # проверка на правильный ответ и возвращение True/False
        if cell == self.desired_emoji_coords:
            return True
        else:
            return False


class SearchCouples(Board): # класс мини игры SearchCouples
    def __init__(self, screen, v=None):
        global flag_minigames1, flag_minigames2, flag_minigames3, room, flag_minigames2_2

        # на экран выводятся все надписи
        self.screen = screen
        pygame.draw.rect(screen, (100, 100, 100), (150, 0, 350, 350))
        self.is_first = True
        self.is_clicked = False
        self.curr_n = None
        self.curr_coords = None
        super().__init__(screen)
        font = pygame.font.Font(None, 30)
        text = font.render("Найдите пары", True, (0, 0, 0))
        text_x = 155
        text_y = 10
        screen.blit(text, (text_x, text_y))
        self.time = 99
        text2 = font.render(str(self.time), True, (0, 0, 0))
        text2_x = 380
        text2_y = 10
        screen.blit(text2, (text2_x, text2_y))

        # создаются спрайты показывающие количество "жизней"
        self.all_sprites = pygame.sprite.Group()

        self.hard1 = pygame.sprite.Sprite()
        self.hard1.image = load_image("health.png")
        self.hard1.rect = self.hard1.image.get_rect()
        self.all_sprites.add(self.hard1)

        self.hard1.rect.x = 465
        self.hard1.rect.y = 6

        self.hard2 = pygame.sprite.Sprite()
        self.hard2.image = load_image("health.png")
        self.hard2.rect = self.hard2.image.get_rect()
        self.all_sprites.add(self.hard2)

        self.hard2.rect.x = 435
        self.hard2.rect.y = 6

        self.hard3 = pygame.sprite.Sprite()
        self.hard3.image = load_image("health.png")
        self.hard3.rect = self.hard3.image.get_rect()
        self.all_sprites.add(self.hard3)

        self.hard3.rect.x = 405
        self.hard3.rect.y = 6

        self.all_sprites.draw(screen)

        if self.playing(): # запускается игровой цикл мини-игры и проверяется выиграл пользователь или проиграл
            if room == 1:  # при победе проверяется в какой комнате была вызвана мини-игра и меняет флаг на True
                flag_minigames1 = True
            elif room == 2 and v == 0:  # переменная v - необязательная
                flag_minigames2 = True  # она нужна для различия двух мини-игр в одной комнате
            elif room == 2 and v == 1:
                flag_minigames2_2 = True
            elif room == 3:
                flag_minigames3 = True
            running3()  # запускает основной цикл

        else:
            minigames.append(1)  # при проигрыше возвращает мини-игру в список и запускает главный цикл
            running3()

    def playing(self):
        running = True
        # создается событие время истекло и запускается таймер
        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)

        # создается событие изменяющее оставшееся время на экране
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        self.count_of_wrong_click = 0
        a = 'playing'

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_click(event.pos) # обработка нажатия

                    # проверка на то, все ли пары найдены
                    check = True
                    for y in range(self.height):
                        for x in range(self.width):
                            if self.board[x][y] != -1:
                                check = False
                                break
                    if check:
                        a = 'win'
                if event.type == TIMERUNOUT: # проверка на истечение времени
                    a = 'defeat'
                if event.type == TIMER:
                    # уменьшение оставшегося времени выведенного на экране
                    self.time -= 1
            if self.count_of_wrong_click == 1:
                self.hard3.kill()
            if self.count_of_wrong_click == 2:
                self.hard2.kill()
            if self.count_of_wrong_click == 3:
                self.hard1.kill()

            if a == 'win':
                # при победе возврвщается True
                return True
            if a == 'defeat' or count_of_wrong_click >= 3:
                # при поражерии возвращается False
                return False

            # всё рисуется на экране
            pygame.draw.rect(self.screen, (100, 100, 100), (150, 0, 350, 350))
            font = pygame.font.Font(None, 30)
            text = font.render("Найдите пары", True, (0, 0, 0))
            text_x = 155
            text_y = 10
            self.screen.blit(text, (text_x, text_y))
            text2 = font.render(str(self.time), True, (0, 0, 0))
            text2_x = 380
            text2_y = 10
            self.screen.blit(text2, (text2_x, text2_y))
            self.render(self.screen)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def render(self, screen):
        if self.is_first: # в первый запуск функции всем клеткаи поля присваиваются случайные номера смайликов
            self.is_first = False
            for n in range(1, 26):
                for _ in range(4):
                    x, y = randrange(self.width), randrange(self.height)
                    while self.board[x][y] != 0:
                        x, y = randrange(self.width), randrange(self.height)
                    self.board[x][y] = n
                    emoji = load_image(f'emoji{n}.png')
                    self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                             self.cell_size, self.cell_size))

        if self.is_clicked: # если пользователь нажал на смайлик, появляется обводка
            pygame.draw.rect(screen, pygame.Color('white'), (
                self.curr_coords[0] * self.cell_size + self.left, self.curr_coords[1] * self.cell_size + self.top,
                self.cell_size, self.cell_size))

        # рисование всех смайликов
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == -1:
                    continue
                else:
                    emoji = load_image(f'emoji{self.board[x][y]}.png')
                    self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                             self.cell_size, self.cell_size))

    def on_click(self, cell): # обработка нажатия
        if self.board[cell[0]][cell[1]] == -1: # нажатие на пустую клетку игнорируется
            return
        if self.is_clicked:
            # если пользователь уже нажал на один смайл проверяется насовпадение смайликов
            if cell == self.curr_coords:
                self.is_clicked = False
                self.curr_coords = None
                self.curr_n = None
            else:
                if self.curr_n == self.board[cell[0]][cell[1]]:
                    self.board[cell[0]][cell[1]] = -1
                    self.board[self.curr_coords[0]][self.curr_coords[1]] = -1
                    self.is_clicked = False
                    self.curr_coords = None
                    self.curr_n = None
                else:
                    self.count_of_wrong_click += 1
        else:
            # пользователь ещё не нажимал на смайл, смайл запоминается для последующей проверки
            self.is_clicked = True
            self.curr_coords = cell
            self.curr_n = self.board[cell[0]][cell[1]]


class ConnectingWires:
    def __init__(self, screen, v=None):
        global flag_minigames1, flag_minigames2, flag_minigames3, room, flag_minigames2_2
        self.screen = screen
        pygame.draw.rect(screen, (100, 100, 100), (150, 0, 350, 350))

        # каждому проводу рандомно присваивается свой цвет
        self.colors = [pygame.Color("red"), pygame.Color("orange"), pygame.Color("green"),
                       pygame.Color("blue"), pygame.Color("yellow"), pygame.Color("purple")]

        shuffle(self.colors)
        self.left_wires_coords = {
            (150, 60, 60, 20): self.colors[0],
            (150, 110, 60, 20): self.colors[1],
            (150, 160, 60, 20): self.colors[2],
            (150, 210, 60, 20): self.colors[3],
            (150, 260, 60, 20): self.colors[4],
            (150, 310, 60, 20): self.colors[5]
        }

        shuffle(self.colors)
        self.right_wires_coords = {
            (440, 60, 60, 20): self.colors[0],
            (440, 110, 60, 20): self.colors[1],
            (440, 160, 60, 20): self.colors[2],
            (440, 210, 60, 20): self.colors[3],
            (440, 260, 60, 20): self.colors[4],
            (440, 310, 60, 20): self.colors[5]
        }

        # надписи выводятся на экран
        self.time = 19
        text2 = font.render(str(self.time), True, (0, 0, 0))
        text2_x = 380
        text2_y = 10
        screen.blit(text2, (text2_x, text2_y))

        # создаются спрайты показывающие количество "жизней"
        self.all_sprites = pygame.sprite.Group()

        self.hard1 = pygame.sprite.Sprite()
        self.hard1.image = load_image("health.png")
        self.hard1.rect = self.hard1.image.get_rect()
        self.all_sprites.add(self.hard1)

        self.hard1.rect.x = 465
        self.hard1.rect.y = 6

        self.hard2 = pygame.sprite.Sprite()
        self.hard2.image = load_image("health.png")
        self.hard2.rect = self.hard2.image.get_rect()
        self.all_sprites.add(self.hard2)

        self.hard2.rect.x = 435
        self.hard2.rect.y = 6

        self.hard3 = pygame.sprite.Sprite()
        self.hard3.image = load_image("health.png")
        self.hard3.rect = self.hard3.image.get_rect()
        self.all_sprites.add(self.hard3)

        self.hard3.rect.x = 405
        self.hard3.rect.y = 6

        self.all_sprites.draw(screen)

        if self.playing(): # запускается игровой цикл мини-игры и проверяется выиграл пользователь или проиграл
            if room == 1:  # при победе проверяется в какой комнате была вызвана мини-игра и меняет флаг на True
                flag_minigames1 = True
            elif room == 2 and v == 0:  # переменная v - необязательная
                flag_minigames2 = True  # она нужна для различия двух мини-игр в одной комнате
            elif room == 2 and v == 1:
                flag_minigames2_2 = True
            elif room == 3:
                flag_minigames3 = True
            running3()  # запускает основной цикл

        else:
            minigames.append(1)  # при проигрыше возвращает мини-игру в список и запускает главный цикл
            running3()


    def get_color(self, pos):
        # возвращение цвета выбранного провода
        x, y = pos
        if y in range(60, 81):
            if x in range(150, 210):
                return self.left_wires_coords[(150, 60, 60, 20)]
            elif x in range(440, 500):
                return self.right_wires_coords[(440, 60, 60, 20)]
        elif y in range(110, 131):
            if x in range(150, 210):
                return self.left_wires_coords[(150, 110, 60, 20)]
            elif x in range(440, 500):
                return self.right_wires_coords[(440, 110, 60, 20)]
        elif y in range(160, 181):
            if x in range(150, 210):
                return self.left_wires_coords[(150, 160, 60, 20)]
            elif x in range(440, 500):
                return self.right_wires_coords[(440, 160, 60, 20)]
        elif y in range(210, 231):
            if x in range(150, 210):
                return self.left_wires_coords[(150, 210, 60, 20)]
            elif x in range(440, 500):
                return self.right_wires_coords[(440, 210, 60, 20)]
        elif y in range(260, 281):
            if x in range(150, 210):
                return self.left_wires_coords[(150, 260, 60, 20)]
            elif x in range(440, 500):
                return self.right_wires_coords[(440, 260, 60, 20)]
        elif y in range(310, 331):
            if x in range(150, 210):
                return self.left_wires_coords[(150, 310, 60, 20)]
            elif x in range(440, 500):
                return self.right_wires_coords[(440, 310, 60, 20)]
        return False

    def get_coords(self, pos):
        # возвращение координат провода
        x, y = pos
        if y in range(60, 81):
            if x in range(150,  210):
                return (150, 60, 60, 20)
            elif x in range(440, 500):
                return (440, 60, 60, 20)
        elif y in range(110, 131):
            if x in range(150, 210):
                return (150, 110, 60, 20)
            elif x in range(440, 500):
                return (440, 110, 60, 20)
        elif y in range(160, 181):
            if x in range(150, 210):
                return (150, 160, 60, 20)
            elif x in range(440, 500):
                return (440, 160, 60, 20)
        elif y in range(210, 231):
            if x in range(150, 210):
                return (150, 210, 60, 20)
            elif x in range(440, 500):
                return (440, 210, 60, 20)
        elif y in range(260, 281):
            if x in range(150, 210):
                return (150, 260, 60, 20)
            elif x in range(440, 500):
                return (440, 260, 60, 20)
        elif y in range(310, 331):
            if x in range(150, 210):
                return (150, 310, 60, 20)
            elif x in range(440, 500):
                return (440, 310, 60, 20)
        return False

    def playing(self):
        running = True

        # создается событие время истекло и запускается таймер
        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)

        # создается событие изменяющее оставшееся время на экране
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        a = 'playing'
        click = False
        color = None
        count_of_wrong_click = 0
        count_of_connected_wires = 0
        starts_and_ends = [] # список начал, концов, цветов соединенный прводов; нужен для рисования на экране

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if click: # когда провод уже выбран, проверяется на совпадение цветв пары
                        if self.get_color(event.pos) == color:
                            click = False
                            if coords_for_rect == self.get_coords(event.pos):
                                pass
                            else:
                                count_of_connected_wires += 1
                                if coords_for_rect[0] < self.get_coords(event.pos)[0]:
                                    b = ((210, coords_for_rect[1] + 9), (440, self.get_coords(event.pos)[1] + 9),
                                         self.get_color(event.pos))
                                    starts_and_ends.append(b)
                                else:
                                    b = ((210, self.get_coords(event.pos)[1] + 9), (440, coords_for_rect[1] + 9),
                                         self.get_color(event.pos))
                                    starts_and_ends.append(b)
                        else:
                            count_of_wrong_click += 1
                            if count_of_wrong_click == 1:
                                self.hard3.kill()
                            if count_of_wrong_click == 2:
                                self.hard2.kill()
                            if count_of_wrong_click == 3:
                                self.hard1.kill()
                    else: # провод на который нажили запоминается
                        click = True
                        coords_for_rect = self.get_coords(event.pos)
                        color = self.get_color(event.pos)
                if event.type == TIMERUNOUT:
                    a = 'defeat'
                if event.type == TIMER:
                    self.time -= 1

            # рисование всего на экране
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (100, 100, 100), (150, 0, 350, 350))
            for coords in self.left_wires_coords.keys():
                pygame.draw.rect(self.screen, self.left_wires_coords[coords], coords)
            for coords in self.right_wires_coords.keys():
                pygame.draw.rect(self.screen, self.right_wires_coords[coords], coords)
            if click:
                pygame.draw.rect(self.screen, pygame.Color('white'), coords_for_rect, 2)
            for elem in starts_and_ends:
                pygame.draw.line(self.screen, elem[2], elem[0], elem[1], width=20)
            font = pygame.font.Font(None, 30)
            text = font.render("Соедините", True, (0, 0, 0))
            text_x = 155
            text_y = 8
            self.screen.blit(text, (text_x, text_y))
            text1 = font.render("соответствующие цвета", True, (0, 0, 0))
            text_x1 = 155
            text_y1 = 30
            self.screen.blit(text1, (text_x1, text_y1))
            text2 = font.render(str(self.time), True, (0, 0, 0))
            text2_x = 470
            text2_y = 32
            self.screen.blit(text2, (text2_x, text2_y))
            self.all_sprites.draw(self.screen)
            if count_of_connected_wires == 6:
                return True
            if a == 'defeat' or count_of_wrong_click >= 3:
                return False
            pygame.display.flip()
        pygame.quit()


class Summas(Board):
    def __init__(self, screen, v=None):
        global flag_minigames1, flag_minigames2, flag_minigames3, room, flag_minigames2_2
        self.screen = screen
        pygame.draw.rect(screen, (100, 100, 100), (150, 0, 350, 350))
        self.is_first = True
        self.is_clicked = False
        self.curr_n = None
        self.curr_coords = None
        super().__init__(screen)

        # вывод всех надписей на экран
        font = pygame.font.Font(None, 20)
        text = font.render("Найдите пары чисел,", True, (0, 0, 0))
        text_x = 155
        text_y = 6
        screen.blit(text, (text_x, text_y))
        text1 = font.render("где сума равна 101", True, (0, 0, 0))
        text_x1 = 155
        text_y1 = 10
        screen.blit(text1, (text_x1, text_y1))
        self.time = 499
        text2 = font.render(str(self.time), True, (0, 0, 0))
        text2_x = 380
        text2_y = 10
        screen.blit(text2, (text2_x, text2_y))

        # создаются спрайты показывающие количество "жизней"
        self.all_sprites = pygame.sprite.Group()

        self.hard1 = pygame.sprite.Sprite()
        self.hard1.image = load_image("health.png")
        self.hard1.rect = self.hard1.image.get_rect()
        self.all_sprites.add(self.hard1)

        self.hard1.rect.x = 465
        self.hard1.rect.y = 6

        self.hard2 = pygame.sprite.Sprite()
        self.hard2.image = load_image("health.png")
        self.hard2.rect = self.hard2.image.get_rect()
        self.all_sprites.add(self.hard2)

        self.hard2.rect.x = 435
        self.hard2.rect.y = 6

        self.hard3 = pygame.sprite.Sprite()
        self.hard3.image = load_image("health.png")
        self.hard3.rect = self.hard3.image.get_rect()
        self.all_sprites.add(self.hard3)

        self.hard3.rect.x = 405
        self.hard3.rect.y = 6

        self.all_sprites.draw(screen)

        if self.playing():  # запускается игровой цикл мини-игры и проверяется выиграл пользователь или проиграл
            if room == 1:  # при победе проверяется в какой комнате была вызвана мини-игра и меняет флаг на True
                flag_minigames1 = True
            elif room == 2 and v == 0:  # переменная v - необязательная
                flag_minigames2 = True  # она нужна для различия двух мини-игр в одной комнате
            elif room == 2 and v == 1:
                flag_minigames2_2 = True
            elif room == 3:
                flag_minigames3 = True
            running3()  # запускает основной цикл

        else:
            minigames.append(1)  # при проигрыше возвращает мини-игру в список и запускает главный цикл
            running3()

    def playing(self):
        running = True

        # создается событие время истекло и запускается таймер
        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)

        # создается событие изменяющее оставшееся время на экране
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        self.count_of_wrong_click = 0

        a = 'playing'

        while running:
            # аналогично мини-игре SearchCouples, только вместо пар смайликов пары чисел
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_click(event.pos)
                    check = True
                    for y in range(self.height):
                        for x in range(self.width):
                            if self.board[x][y] != -1:
                                check = False
                                break
                    if check:
                        a = 'win'
                if event.type == TIMERUNOUT:
                    a = 'defeat'
                if event.type == TIMER:
                    self.time -= 1
            if self.count_of_wrong_click == 1:
                self.hard3.kill()
            if self.count_of_wrong_click == 2:
                self.hard2.kill()
            if self.count_of_wrong_click == 3:
                self.hard1.kill()
            if a == 'win':
                return True
            if a == 'defeat' or self.count_of_wrong_click >= 3:
                return False
            pygame.draw.rect(self.screen, (100, 100, 100), (150, 0, 350, 350))
            font = pygame.font.Font(None, 25)
            text = font.render("Найдите пары чисел,", True, (0, 0, 0))
            text_x = 155
            text_y = 6
            self.screen.blit(text, (text_x, text_y))
            text1 = font.render("где сума равна 101", True, (0, 0, 0))
            text_x1 = 155
            text_y1 = 21
            self.screen.blit(text1, (text_x1, text_y1))
            text2 = font.render(str(self.time), True, (0, 0, 0))
            text2_x = 380
            text2_y = 10
            self.screen.blit(text2, (text2_x, text2_y))
            self.render(self.screen)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def render(self, screen):
        if self.is_first: # в первый запуск функции всем клеткам присваиваются свои числа
            self.is_first = False
            numbers = list(range(1, 101))
            for y in range(self.height):
                for x in range(self.width):
                    n = numbers.index(choice(numbers))
                    self.board[x][y] = numbers.pop(n)

        if self.is_clicked: # выбранная клетка выделяется белым
            pygame.draw.rect(screen, pygame.Color('white'), (
                self.curr_coords[0] * self.cell_size + self.left, self.curr_coords[1] * self.cell_size + self.top,
                self.cell_size, self.cell_size))

        # рисование чисел и поля на экране
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == -1:
                    continue
                else:
                    pygame.draw.rect(screen, pygame.Color("white"), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size), 1)
                    font = pygame.font.Font(None, 25)
                    text = font.render(str(self.board[x][y]), True, (0, 0, 0))
                    if self.board[x][y] == 100:
                        text_x = x * self.cell_size + self.left + 1
                    elif self.board[x][y] < 10:
                        text_x = x * self.cell_size + self.left + 12
                    else:
                        text_x = x * self.cell_size + self.left + 6
                    text_y = y * self.cell_size + self.top + 6
                    self.screen.blit(text, (text_x, text_y))

    def on_click(self, cell):
        # обработка нажатия аналогична мини-игре SearchCouples, только проверяется сумма выбранных чисел
        if self.board[cell[0]][cell[1]] == -1:
            return
        if self.is_clicked:
            if cell == self.curr_coords:
                self.is_clicked = False
                self.curr_coords = None
                self.curr_n = None
            else:
                if self.curr_n + self.board[cell[0]][cell[1]] == 101:
                    self.board[cell[0]][cell[1]] = -1
                    self.board[self.curr_coords[0]][self.curr_coords[1]] = -1
                    self.is_clicked = False
                    self.curr_coords = None
                    self.curr_n = None
                else:
                    self.count_of_wrong_click += 1
        else:
            self.is_clicked = True
            self.curr_coords = cell
            self.curr_n = self.board[cell[0]][cell[1]]


minigames = [0, 1, 2, 3]  # список с числом мини-игр


def running(screen, v=None):  # функция, отвечающая за перемешивания списка и запуска мини-игр
    global minigames
    pygame.display.set_caption('Игра')  # меняем заголовок окна
    shuffle(minigames)  # меняем последовательность в списке
    a = minigames.pop()  # берем элемент из списка, одновременно удалем число
    if a == 0:  # вызываем игру в зависимости от числа
        Summas(screen, v)
    elif a == 1:
        SearchEmoji(screen, v)
    elif a == 2:
        SearchCouples(screen, v)
    elif a == 3:
        ConnectingWires(screen, v)

#########################################


class Thing(pygame.sprite.Sprite):  # специальный класс, для всех спрайтов в комнатах и лобби
    def __init__(self, number):  # при инициализации спрайта передаем число, по нему у спрайта ставиться нужная каринка
        super(Thing, self).__init__()  # и задаются координаты
        self.number = number
        if number == 1:
            self.image = thing1
            self.rect = self.image.get_rect()
            self.rect.x = 226
            self.rect.y = 116
        elif number == 2:
            self.image = thing2
            self.rect = self.image.get_rect()
            self.rect.x = 306
            self.rect.y = 149
        elif number == 3:
            self.image = thing3
            self.rect = self.image.get_rect()
            self.rect.x = 315
            self.rect.y = 163
        elif number == 4:
            self.image = thing2_2
            self.rect = self.image.get_rect()
            self.rect.x = 469
            self.rect.y = 232
        elif number == 5:
            self.image = bg0_butt1
            self.rect = self.image.get_rect()
            self.rect.x = 421
            self.rect.y = 135
        elif number == 6:
            self.image = bg0_butt2
            self.rect = self.image.get_rect()
            self.rect.x = 421
            self.rect.y = 176
        elif number == 7:
            self.image = bg0_butt3
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 0

    def update(self, *args):  # метод update нужен для реализации нажатия на спрайт
        if self.number == 1:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos) and 215 < person.rect.x < 300 and room == 1:
                running(screen)
        elif self.number == 2:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos) and 215 < person.rect.x < 340 and room == 2:
                running(screen, 0)
        elif self.number == 3:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos) and 300 < person.rect.x < 350 and room == 3:
                running(screen)
        elif self.number == 4:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos) and 430 < person.rect.x < 500 and room == 2:
                running(screen, 1)
        elif self.number == 5:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos):
                running3()
        elif self.number == 6:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos):
                running4()
        elif self.number == 7:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos):
                running2()


cup = Thing(1)  # создаем спрайты для комнат и групппы спрайтов
tv = Thing(2)
micro = Thing(3)
valli = Thing(4)
butt1 = Thing(5)
butt2 = Thing(6)
butt3 = Thing(7)
all_sprites_room1 = pygame.sprite.Group()
all_sprites_room2 = pygame.sprite.Group()
all_sprites_room3 = pygame.sprite.Group()
all_sprites_screen1 = pygame.sprite.Group()
all_sprites_screen2 = pygame.sprite.Group()
all_sprites_room1.add(cup, person)
all_sprites_room2.add(tv, valli, person)
all_sprites_room3.add(micro, person)
all_sprites_screen1.add(butt1, butt2)
all_sprites_screen2.add(butt3)

room = 1  # переменна отвечающая за комнату, с которой начинается игра


def running3():  # функция running3 - основной цикл игры
    global room
    pygame.init()
    running2 = True
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
            if room == 1:  # выбор фона, названия окна
                pygame.display.set_caption('room1')
                screen.blit(bg, (0, 0))
                if flag_minigames1 is True:  # флаг мини-игры, если True, то удаляется спрайт
                    all_sprites_room1.remove(cup)
                all_sprites_room1.draw(screen)
                all_sprites_room1.update(event)
            elif room == 2:
                pygame.display.set_caption('room2')
                screen.blit(bg2, (0, 0))
                if flag_minigames2 is True:
                    all_sprites_room2.remove(tv)
                if flag_minigames2_2 is True:
                    all_sprites_room2.remove(valli)
                all_sprites_room2.draw(screen)
                all_sprites_room2.update(event)
            elif room == 3:
                pygame.display.set_caption('room3')
                screen.blit(bg3, (0, 0))
                if flag_minigames3 is True:
                    all_sprites_room3.remove(micro)
                all_sprites_room3.draw(screen)
                all_sprites_room3.update(event)
            if event.type == pygame.KEYDOWN:  # обработка нажатия клавиш
                if room == 1 and event.key == 101 and person.rect.x >= 515 and flag_minigames1 is True:  # переход между комнатами
                    room = 2
                    person.rect.x = 0
                elif room == 2 and event.key == 101 and person.rect.x <= 115:
                    room = 1
                    person.rect.x = 515
                elif flag_minigames2 and event.key == 101 and person.rect.x >= 515 and flag_minigames2_2:
                    room = 3
                    person.rect.x = 0
                elif room == 3 and event.key == 101 and person.rect.x <= 115:
                    room = 2
                    person.rect.x = 515
                elif flag_minigames3 and event.key == 101 and person.rect.x >= 515:  # конечная заставка
                    pass
            clock.tick(fps)  # обработка внутриигрового времени
        keys = pygame.key.get_pressed()  # реализация ходьбы персонажа зажатием клавиши
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if person.rect.x != 0:
                person.rect.x -= speed
            person.image = pers(flag, 'l')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if person.rect.x + 78 <= w:
                person.rect.x += speed
            person.image = pers(flag, 'r')
        if room == 1:  # реализация диалогового окна внизу экрана
            screen.blit(bg, (0, 0))
            all_sprites_room1.draw(screen)
            pygame.draw.rect(screen, (255, 255, 255), (8, 308, 635, 35))
            if flag_minigames1 is True:  # текст меняется по прохождению мини-игр
                stroka = 'Мой дорогой кубок. Сколько воспоминаний нахлынуло... Я получил его на соревнованиях по пляжному волейболу.'
                font = pygame.font.Font(None, 15)
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 310
                screen.blit(text, (text_x, text_y))
                stroka = 'Сразу лето вспомнилось. Тепло... Хочу под одеяло! Всё бы отдал, чтобы сейчас обратно лечь спать.'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 320
                screen.blit(text, (text_x, text_y))
                stroka = 'Но всё-таки надо собираться в школу!'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 330
                screen.blit(text, (text_x, text_y))
                stroka = 'Подсказка: "Пройдите в следующую комнату. Подойдите к двери и нажмите E"'
                text = font.render(stroka, True, (80, 80, 80))
                text_x = 220
                text_y = 330
                screen.blit(text, (text_x, text_y))
            else:
                stroka = 'Я проснулся от звука будильника. Как обычно хочется спать. В комнате как-то холодно.' \
                         ' Вот бы обратно под одеяло лечь.'
                font = pygame.font.Font(None, 15)
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 310
                screen.blit(text, (text_x, text_y))
                stroka = 'Мне снился странный сон. ' \
                         'Там я потерял свой кубок и спрашивал у всех людей на улице, не видели ли они его.'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 320
                screen.blit(text, (text_x, text_y))
                stroka = 'Кстати где кубок сейчас?'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 330
                screen.blit(text, (text_x, text_y))
                stroka = 'Подсказка: "Найдите кубок. Подойдите к нему и нажмите"'
                text = font.render(stroka, True, (80, 80, 80))
                text_x = 320
                text_y = 330
                screen.blit(text, (text_x, text_y))
        elif room == 2:
            screen.blit(bg2, (0, 0))
            all_sprites_room2.draw(screen)
            pygame.draw.rect(screen, (255, 255, 255), (8, 308, 635, 35))
            if flag_minigames2 is True:
                if flag_minigames2_2 is True:
                    stroka = '*Урчание живота*'
                    font = pygame.font.Font(None, 15)
                    text = font.render(stroka, True, (0, 0, 0))
                    text_x = 10
                    text_y = 310
                    screen.blit(text, (text_x, text_y))
                    stroka = 'Я, кажется, совершенно забыл о том, что мне в школу надо собираться . Пойду завтракать.'
                    text = font.render(stroka, True, (0, 0, 0))
                    text_x = 10
                    text_y = 320
                    screen.blit(text, (text_x, text_y))
                    stroka = 'Подсказка: "Пройдите в следующую комнату. Подойдите к двери и нажмите E'
                    text = font.render(stroka, True, (80, 80, 80))
                    text_x = 10
                    text_y = 330
                    screen.blit(text, (text_x, text_y))
                else:
                    stroka = 'Новости: ~Сегодня в Москве аномальный снегопад. Ночью выпала месячная норма осадков.~'
                    font = pygame.font.Font(None, 15)
                    text = font.render(stroka, True, (0, 0, 0))
                    text_x = 10
                    text_y = 310
                    screen.blit(text, (text_x, text_y))
                    stroka = 'Много снега это классно, но точно не для ЖКХ. Может с друзьями снеговика слепить? Мой робот Валли совершенно.'
                    text = font.render(stroka, True, (0, 0, 0))
                    text_x = 10
                    text_y = 320
                    screen.blit(text, (text_x, text_y))
                    stroka = 'зыпылился. Пожалуй надо стереть пыть.'
                    text = font.render(stroka, True, (0, 0, 0))
                    text_x = 10
                    text_y = 330
                    screen.blit(text, (text_x, text_y))
                    stroka = 'Подсказка: "Почистите робота. Подойдите к нему и нажмите"'
                    text = font.render(stroka, True, (80, 80, 80))
                    text_x = 320
                    text_y = 330
                    screen.blit(text, (text_x, text_y))
            else:
                stroka = 'Может новости включить. Что за странные мысли, я их последний раз месяца 2 назад смотрел.'
                font = pygame.font.Font(None, 15)
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 310
                screen.blit(text, (text_x, text_y))
                stroka = 'Хотя надо же быть немного в курсе событий. Пожалуй сегодня посмотрю.'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 320
                screen.blit(text, (text_x, text_y))
                stroka = 'Подсказка: "Включите телевизор. Подойдите к нему и нажмите"'
                text = font.render(stroka, True, (80, 80, 80))
                text_x = 10
                text_y = 330
                screen.blit(text, (text_x, text_y))
        elif room == 3:
            screen.blit(bg3, (0, 0))
            all_sprites_room3.draw(screen)
            pygame.draw.rect(screen, (255, 255, 255), (8, 308, 635, 35))
            if flag_minigames3 is True:
                stroka = 'Наконец-то завтрак. Как же я люблю сырники. Я поел за 10 минут. Совершенно не хотелось торопиться.'
                font = pygame.font.Font(None, 15)
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 310
                screen.blit(text, (text_x, text_y))
                stroka = 'Осталось только взять рюкзак и одеться. Надеюсь сегодня у меня будет хороший день.'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 320
                screen.blit(text, (text_x, text_y))
                stroka = 'Подсказка: "Подойдите к двери и нажмите E"'
                text = font.render(stroka, True, (80, 80, 80))
                text_x = 10
                text_y = 330
                screen.blit(text, (text_x, text_y))
            else:
                stroka = 'Я умылся и почистил зубы. Теперь можно позавтракать. Но времени совсем мало осталось.'
                font = pygame.font.Font(None, 15)
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 310
                screen.blit(text, (text_x, text_y))
                stroka = 'Через 15 минут уже надо из дома выходить. О мама оставила завтрак на столе. Надо подогреть.'
                text = font.render(stroka, True, (0, 0, 0))
                text_x = 10
                text_y = 320
                screen.blit(text, (text_x, text_y))
                stroka = 'Подсказка: "Подогрейте завтрак. Подойдите к микроволновке и нажмите"'
                text = font.render(stroka, True, (80, 80, 80))
                text_x = 10
                text_y = 330
                screen.blit(text, (text_x, text_y))
        clock.tick(fps // 4)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


def running2():  # первый цикл с начальной картинкой
    pygame.init()
    screen.blit(bg0, (0, 0))
    pygame_icon = pygame.image.load(r'data\ava.png')
    pygame.display.set_icon(pygame_icon)  # меняю аватарку игры на лицо персонажа
    pygame.display.set_caption('Лобби')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            clock.tick(fps)
            pygame.display.flip()
            all_sprites_screen1.draw(screen)
            all_sprites_screen1.update(event)  # обработка нажатия на кнопки
    pygame.quit()
    sys.exit()


def running4():  # цикл с каринкой об авторах
    pygame.init()
    screen.blit(bg0_1, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites_screen2.draw(screen)
            all_sprites_screen2.update(event)
            pygame.display.flip()
    pygame.quit()
    sys.exit()


def pers(flag1, rotate):  # вспомогательная функция, которая возвращает картинку персонажа
    global flag  # а так же отвечает за изменение картинки на персонажа с шагом
    if flag1 is True:  # таким образом на экране персонаж "ходит"
        if rotate == 'r':
            flag = False
            return pr3
        else:
            flag = False
            return pr4
    else:
        if rotate == 'r':
            flag = True
            return pr1
        else:
            flag = True
            return pr2


if __name__ == '__main__':  # запуск проекта
    running2()
