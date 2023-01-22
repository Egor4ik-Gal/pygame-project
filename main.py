import pygame
import os
from random import randrange, choice, shuffle

flag = True
flag_minigames1 = False
flag_minigames2 = False
flag_minigames3 = False
size2 = w, h = 650, 350
screen = pygame.display.set_mode(size2)
clock = pygame.time.Clock()
fps = 60
speed = 113
bg = pygame.image.load(r'data\room1.png')
bg2 = pygame.image.load(r'data\room2sav3.png')
bg3 = pygame.image.load(r'data\room3sav3.png')
pr1 = pygame.image.load(r'data\pers1.png')
pr2 = pygame.image.load(r'data\pers1.1.png')
pr3 = pygame.image.load(r'data\pers1.2.png')
pr4 = pygame.image.load(r'data\pers1.22.png')
thing1 = pygame.image.load(r'data\cup.png')
thing2 = pygame.image.load(r'data\TV.png')
thing3 = pygame.image.load(r'data\micro.png')
pr2.set_colorkey((255, 255, 255))

person = pygame.sprite.Sprite()
person.image = pr1
person.rect = person.image.get_rect()
person.rect.x = 0
person.rect.y = h - 205


##############################


def load_image(name, colorkey=None):
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


class Board:
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


class Ball(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = 150 + randrange(315)
        self.rect.y = 0


class CatchingBalls:
    def __init__(self, screen):
        global flag_minigames1, flag_minigames2, flag_minigames3, room
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
            elif room == 2:
                flag_minigames2 = True
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
        clock = pygame.time.Clock()
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
            pygame.display.flip()
            if count_of_fallen_balls >= 3:
                # running = False
                # running3()
                return False
            if count_of_catched_balls == 30:
                # running = False
                # all_sprites2.remove(object2)
                # running3()
                return True
        pygame.quit()


class SearchEmoji(Board):
    def __init__(self, screen):
        global flag_minigames1, flag_minigames2, flag_minigames3, room
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
            elif room == 2:
                flag_minigames2 = True
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
            # start_ticks = pygame.time.get_ticks()  # пытался сделать таймер с надписью "Вы проиграли!"
            # for event in pygame.event.get():
            #     seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            #     if seconds > 10:
            running3()


    def playing(self):
        running = True
        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)
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
                    if self.get_click(event.pos):
                        a = 'win'
                    else:
                        count_of_wrong_click += 1
                        if count_of_wrong_click == 1:
                            self.hard3.kill()
                        if count_of_wrong_click == 2:
                            self.hard2.kill()
                        if count_of_wrong_click == 3:
                            self.hard1.kill()
                if event.type == TIMERUNOUT:
                    a = 'defeat'
                if event.type == TIMER:
                    self.time -= 1
            if a == 'win':
                return True
            if a == 'defeat' or count_of_wrong_click >= 3:
                return False
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

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                # pygame.draw.rect(screen, colors[self.board[y][x]], (
                #     x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                #     self.cell_size))

                # pygame.draw.rect(screen, pygame.Color("white"), (
                #     x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                #     self.cell_size), 1)
                if self.board[x][y] == 0:
                    if (x, y) == self.desired_emoji_coords:
                        self.board[x][y] = self.n
                        self.screen.blit(self.desired_emoji,
                                         (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                          self.cell_size, self.cell_size))
                    else:
                        n = randrange(1, 31)
                        while n == self.n:
                            n = randrange(1, 31)
                        emoji = load_image(f'emoji{n}.png')
                        self.board[x][y] = n
                        self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                                 self.cell_size, self.cell_size))
                else:
                    emoji = load_image(f'emoji{self.board[x][y]}.png')
                    self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                             self.cell_size, self.cell_size))

    def on_click(self, cell):
        if cell == self.desired_emoji_coords:
            return True
        else:
            return False


class SearchCouples(Board):
    def __init__(self, screen):
        global flag_minigames1, flag_minigames2, flag_minigames3, room
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
            elif room == 2:
                flag_minigames2 = True
            elif room == 3:
                flag_minigames3 = True
            running3()
        else:
            font = pygame.font.Font(None, 40)
            text = font.render("Вы проиграли!!!", True, (100, 255, 100))
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

        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 100000)
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
        if self.is_first:
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

        if self.is_clicked:
            pygame.draw.rect(screen, pygame.Color('white'), (
                self.curr_coords[0] * self.cell_size + self.left, self.curr_coords[1] * self.cell_size + self.top,
                self.cell_size, self.cell_size))

        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == -1:
                    continue
                else:
                    emoji = load_image(f'emoji{self.board[x][y]}.png')
                    self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                             self.cell_size, self.cell_size))

    def on_click(self, cell):
        if self.board[cell[0]][cell[1]] == -1:
            return
        if self.is_clicked:
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
            self.is_clicked = True
            self.curr_coords = cell
            self.curr_n = self.board[cell[0]][cell[1]]


def running(screen):
    # pygame.init()
    # size = 650, 350
    # screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игра')
    a = randrange(3)
    a = 1  # не забыть удалить!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if a == 0:
        CatchingBalls(screen)
    elif a == 1:
        SearchEmoji(screen)
    elif a == 2:
        SearchCouples(screen)
    # pygame.display.flip()
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    # pygame.quit()


#########################################


class Thing(pygame.sprite.Sprite):
    def __init__(self, number):
        super(Thing, self).__init__()
        self.number = number
        if number == 1:
            self.image = thing1
            self.rect = self.image.get_rect()
            self.rect.x = 226
            self.rect.y = 116
        elif number == 2:
            self.image = thing2
            self.rect = self.image.get_rect()
            self.rect.x = 307
            self.rect.y = 150
        elif number == 3:
            self.image = thing3
            self.rect = self.image.get_rect()
            self.rect.x = 316
            self.rect.y = 165


    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                args[0].pos) and 215 < person.rect.x < 340:
            running(screen)


cup = Thing(1)
tv = Thing(2)
micro = Thing(3)
all_sprites_room1 = pygame.sprite.Group()
all_sprites_room2 = pygame.sprite.Group()
all_sprites_room3 = pygame.sprite.Group()
all_sprites_room1.add(cup, person)
all_sprites_room2.add(tv, person)
all_sprites_room3.add(micro, person)
room = 1


def running3():
    global room
    pygame.init()
    screen.blit(pr1, (0, 0))
    running2 = True
    while running2:
        for event in pygame.event.get():
            if room == 1:
                pygame.display.set_caption('room1')
                screen.blit(bg, (0, 0))
                if flag_minigames1 is True:
                    all_sprites_room1.remove(cup)
                all_sprites_room1.draw(screen)
                all_sprites_room1.update(event)
            elif room == 2:
                pygame.display.set_caption('room2')
                screen.blit(bg2, (0, 0))
                if flag_minigames2 is True:
                    all_sprites_room2.remove(tv)
                all_sprites_room2.draw(screen)
                all_sprites_room2.update(event)
            elif room == 3:
                pygame.display.set_caption('room3')
                screen.blit(bg3, (0, 0))
                if flag_minigames3 is True:
                    all_sprites_room3.remove(micro)
                all_sprites_room3.draw(screen)
                all_sprites_room3.update(event)
            if event.type == pygame.QUIT:
                running2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == 100 or event.key == 1073741903:
                    if person.rect.x + 78 + speed <= w:
                        person.rect.x += speed
                    else:
                        person.rect.x = 570
                    person.image = pers(flag, 'r')
                if event.key == 97 or event.key == 1073741904:
                    if person.rect.x - speed >= 1:
                        person.rect.x -= speed
                    else:
                        person.rect.x = 0
                    person.image = pers(flag, 'l')
                if room == 1 and event.key == 101 and person.rect.x >= 515:
                    room = 2
                    person.rect.x = 0
                elif room == 2 and event.key == 101 and person.rect.x <= 115:
                    room = 1
                    person.rect.x = 515
                elif flag_minigames2 and event.key == 101 and person.rect.x >= 515:
                    room = 3
                    person.rect.x = 0
                elif room == 3 and event.key == 101 and person.rect.x <= 115:
                    room = 2
                    person.rect.x = 515
            clock.tick(fps)
            pygame.display.flip()
    pygame.quit()


def pers(flag1, rotate):
    global flag
    if flag1 is True:
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


if __name__ == '__main__':
    running3()
