import pygame,sys
from pygame.constants import *

pygame.init()

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top':False, 'bottom':False, 'left':False, 'right':False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def load_map(path):
    with open(path + '.txt', 'r') as f:
        data = f.read().splitlines()
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
        

WINDOWSIZE = (512, 400)
HALFWINDOW = 128

clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOWSIZE)
display = pygame.Surface((256, 200))

grey = pygame.image.load('images/man/Man.png')
pwidth, pheight = grey.get_width(), grey.get_height()
player_rect = pygame.Rect(0, 0, pwidth, pheight)

bg_objects = [[0.5, [120, 100, 90, 300]], [0.25, [150, 130, 70, 230]], [0.125, [170, 130, 100, 50]]]

grass = pygame.image.load('images/tiles/grassBlock.png')
dirt = pygame.image.load('images/tiles/dirtBlock.png')
dirtb = pygame.image.load('images/tiles/dirtBack.png')
water = pygame.image.load('images/tiles/waterBlock.png')

TILESIZE = 16

moving_left = False
moving_right = False
playery_momentum = 0

no_collide = ['0', '3', '4', '5']

true_scroll = [0, 0]

map = load_map('my_map')
for y, row in enumerate(map):
    for x, tile in enumerate(row):
        if tile == '4':
            player_rect.bottomleft = (x*TILESIZE, y*TILESIZE)
            startpos = (x*TILESIZE, y*TILESIZE)

while True:
    display.fill((60, 170, 200))

    true_scroll[0] += (player_rect.centerx-true_scroll[0]-HALFWINDOW)/15
    true_scroll[1] += (player_rect.centery-true_scroll[1]-100)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (21, 50, 12), pygame.Rect(0, 128, 256, 128))

    for bg_object in bg_objects:
        obj_rect = pygame.Rect(bg_object[1][0]-scroll[0]*bg_object[0], bg_object[1][1]-scroll[1]*bg_object[0], bg_object[1][2], bg_object[1][3])
        if bg_object[0] == 0.5:
            pygame.draw.rect(display, (35, 100, 24), obj_rect)
        if bg_object[0] == 0.25:
            pygame.draw.rect(display, (56, 144, 32), obj_rect)
        if bg_object[0] == 0.125:
            pygame.draw.rect(display, (200, 215, 230), obj_rect)
    
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == '5':
                display.blit(dirtb, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))

    display.blit(grey, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    tile_rects = []
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == '1':
                display.blit(grass, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))
            if tile == '2':
                display.blit(dirt, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))
            if tile == '3':
                display.blit(water, (x*TILESIZE-scroll[0], y*TILESIZE-scroll[1]))
            if tile not in no_collide:
                    tile_rects.append(pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE))
    
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] = 2
    if moving_left:
        player_movement[0] = -2
    player_movement[1] += playery_momentum
    playery_momentum += 0.2
    if playery_momentum > 3:
        playery_momentum = 3
    
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        playery_momentum = 1
    if collisions['top']:
        playery_momentum = 0

    surf = pygame.transform.scale(display, WINDOWSIZE)
    screen.blit(surf, (0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_a:
                moving_left = True
            if event.key == K_d:
                moving_right = True
            if event.key == K_SPACE:
                if collisions['bottom']:
                    playery_momentum = -5
            if event.key == K_RETURN:
                map = load_map('my_map')
            if event.key == K_r:
                player_rect.bottomleft = startpos
        
        elif event.type == KEYUP:
            if event.key == K_a:
                moving_left = False
            
            if event.key == K_d:
                moving_right = False

    pygame.display.update()
    clock.tick(60)
