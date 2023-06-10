import pygame, sys
from pygame.constants import *

# Constants
WINDOWSIZE = (512, 400)
TILESIZE = 16
ROWS = COLS = 32

def save_map(path):
    with open(path + '.txt', 'w') as f:
        for row in map:
            for col in row:
                f.write(col)
            f.write('\n')

pygame.init()

screen = pygame.display.set_mode(WINDOWSIZE)
display = pygame.Surface((256, 200))

clock = pygame.time.Clock()

# Load images
grass = pygame.image.load('images/tiles/grassBlock.png')
dirt = pygame.image.load('images/tiles/dirtBlock.png')
water = pygame.image.load('images/tiles/waterBlock.png')
player = pygame.image.load('images/man/Man.png')

# Map stuff
map = [['0' for i in range(COLS)] for i in range(ROWS)]
tiletype = '1'
inttile = 1
maxtiles = 3

# Scrolling Vars
scroll = [1, 1]
scrolling = [0, 0]

while True:
    display.fill('lightblue')

    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == '1':
                display.blit(grass, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))
            if tile == '2':
                display.blit(dirt, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))
            if tile == '3':
                display.blit(water, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))
            if tile == '4':
                display.blit(player, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))

    if tiletype == '1':
        display.blit(grass, (0, 0))
    if tiletype == '2':
        display.blit(dirt, (0, 0))
    if tiletype == '3':
        display.blit(water, (0, 0))
    if tiletype == '4':
        display.blit(player, (0, 0))

    pos = pygame.mouse.get_pos()
    x = (pos[0]+(scroll[0]*2)) // (TILESIZE*2)
    y = (pos[1]+(scroll[1]*2)) // (TILESIZE*2)

    if pygame.mouse.get_pressed()[0]:
        if 0 < x < 32 and 0 < y < 32:
            if map[y][x] != tiletype:
                map[y][x] = tiletype
    elif pygame.mouse.get_pressed()[2]:
        map[y][x] = '0'
    
    if 0 < scroll[0]:
        if scroll[0] <= ROWS*TILESIZE-200:
            scroll[0] += scrolling[0]
        else:
            scroll[0] = ROWS*TILESIZE-200
    else:
        scroll[0] = 1
    if 0 <= scroll[1]:
        if scroll[1] <= COLS*TILESIZE-200:
            scroll[1] += scrolling[1]
        else:
            scroll[1] = COLS*TILESIZE-200
    else:
        scroll[1] = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                save_map('my_map')
            if event.key == K_LEFT:
                inttile -= 1
                tiletype = str(inttile)
            if event.key == K_RIGHT:
                inttile += 1
                tiletype = str(inttile)
            if event.key == K_w:
                scrolling[1] = -1
            if event.key == K_a:
                scrolling[0] = -1
            if event.key == K_s:
                scrolling[1] = 1
            if event.key == K_d:
                scrolling[0] = 1

        if event.type == KEYUP:
            if event.key == K_w or event.key == K_s:
                scrolling[1] = 0
            if event.key == K_a or event.key == K_d:
                scrolling[0] = 0
    
    surf = pygame.transform.scale(display, WINDOWSIZE)
    screen.blit(surf, (0, 0))

    pygame.display.update()
    clock.tick(60)
