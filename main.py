import pygame

pygame.init()
size = w, h = 650, 350
pygame.display.set_caption('room1')
clock = pygame.time.Clock()
fps = 60
speed = 10
bg = pygame.image.load(r'data\room1.png')
pr1 = pygame.image.load(r'data\pers1.png')
pr2 = pygame.image.load(r'data\pers1.1.png')
pr3 = pygame.image.load(r'data\pers1.2.png')
pr4 = pygame.image.load(r'data\pers1.22.png')
pr2.set_colorkey((255, 255, 255))
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
screen.blit(pr1, (0, 0))
person = pygame.sprite.Sprite(all_sprites)
person.image = pr1
person.rect = person.image.get_rect()
person.rect.x = 0
person.rect.y = h - 205


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


running = True
flag = True
while running:
    for event in pygame.event.get():
        screen.blit(bg, (0, 0))
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 100 or event.key == 1073741903:
                if person.rect.x + 78 <= w:
                    person.rect.x += speed
                person.image = pers(flag, 'r')
            if event.key == 97 or event.key == 1073741904:
                if person.rect.x != 0:
                    person.rect.x -= speed
                person.image = pers(flag, 'l')
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
pygame.quit()
