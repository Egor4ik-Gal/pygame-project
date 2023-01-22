import pygame
import os
from random import randrange, shuffle, choice


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
                return False
            if count_of_catched_balls == 30:
                return True


class SearchEmoji(Board):
    def __init__(self, screen):
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

    def playing(self):
        running = True

        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        a = 'playing'
        count_of_wrong_click = 0

        while running:
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

    def playing(self):
        running = True

        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 100000)
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        self.count_of_wrong_click = 0

        a = 'playing'

        while running:
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

class ConnectingWires:
    def __init__(self, screen):
        self.screen = screen
        pygame.draw.rect(screen, (100, 100, 100), (150, 0, 350, 350))

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

    def get_color(self, pos):
        x, y = pos
        if y in range(60, 81):
            if x in range(150,210):
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
        x, y = pos
        if y in range(60, 81):
            if x in range(150,210):
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

        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 20000)
        TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMER, 1000)

        a = 'playing'
        click = False
        color = None
        count_of_wrong_click = 0
        count_of_connected_wires = 0
        starts_and_ends = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if click:
                        if self.get_color(event.pos) == color:
                            click = False
                            if coords_for_rect == self.get_coords(event.pos):
                                pass
                            else:
                                count_of_connected_wires += 1
                                if coords_for_rect[0] < self.get_coords(event.pos)[0]:
                                    b = ((210, coords_for_rect[1] + 10), (440, self.get_coords(event.pos)[1] + 10),
                                         self.get_color(event.pos))
                                    starts_and_ends.append(b)
                                else:
                                    b = ((210, self.get_coords(event.pos)[1] + 10), (440, coords_for_rect[1] + 10),
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
                    else:
                        click = True
                        coords_for_rect = self.get_coords(event.pos)
                        color = self.get_color(event.pos)
                if event.type == TIMERUNOUT:
                    a = 'defeat'
                if event.type == TIMER:
                    self.time -= 1
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


class Summas(Board):
    def __init__(self, screen):
        global flag_minigames1, flag_minigames2, flag_minigames3, room
        self.screen = screen
        pygame.draw.rect(screen, (100, 100, 100), (150, 0, 350, 350))
        self.is_first = True
        self.is_clicked = False
        self.curr_n = None
        self.curr_coords = None
        super().__init__(screen)
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

    def playing(self):
        running = True

        TIMERUNOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMERUNOUT, 500000)
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
        if self.is_first:
            self.is_first = False
            numbers = list(range(1, 101))
            for y in range(self.height):
                for x in range(self.width):
                    n = numbers.index(choice(numbers))
                    self.board[x][y] = numbers.pop(n)
            # for n in range(1, 26):
            #     for _ in range(4):
            #         x, y = randrange(self.width), randrange(self.height)
            #         while self.board[x][y] != 0:
            #             x, y = randrange(self.width), randrange(self.height)
            #         self.board[x][y] = n
            #         emoji = load_image(f'emoji{n}.png')
            #         self.screen.blit(emoji, (x * self.cell_size + self.left, y * self.cell_size + self.top,
            #                                  self.cell_size, self.cell_size))

        if self.is_clicked:
            pygame.draw.rect(screen, pygame.Color('white'), (
                self.curr_coords[0] * self.cell_size + self.left, self.curr_coords[1] * self.cell_size + self.top,
                self.cell_size, self.cell_size))

        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == -1:
                    continue
                else:
                    # self.screen.blit(self.board[x][y], (x * self.cell_size + self.left, y * self.cell_size + self.top,
                    #                          self.cell_size, self.cell_size))
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


def running():
    pygame.init()
    size = 650, 350
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игра')
    a = randrange(4)
    if a == 0:
        Summas(screen)
    elif a == 1:
        SearchEmoji(screen)
    elif a == 2:
        SearchCouples(screen)
    elif a == 3:
        ConnectingWires(screen)
    pygame.display.flip()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
    pygame.quit()


if __name__ == '__main__':
    running()