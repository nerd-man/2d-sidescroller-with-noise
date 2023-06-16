import pygame,sys
from pygame.constants import *
import random
import noise

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

def generate_chunks(x, y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999) * 5)
            # Dirt
            if target_y > 8 - height:
                tile_type = 2
            # Grass
            elif target_y == 8 - height:
                tile_type = 1
            # Water
            elif 7 < target_y < 8 - height > 8:
                tile_type = 4
            # Tall grass
            elif target_y == 8 - height - 1:
                if random.randint(1, 5) == 1:
                    tile_type = 3
            
            # if tile_type != 0:
            chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

def draw_text(text, color, pos):
    stuff = font.render(text, True, color)
    display.blit(stuff, pos)
font = pygame.font.SysFont('comicsansms', 20)

WINDOWSIZE = (600, 400)
HALFWINDOW = 150

CHUNK_SIZE = 8

clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOWSIZE)
display = pygame.Surface((300, 200))

grey = pygame.image.load('images/man/Manrep2.png').convert()
pwidth, pheight = grey.get_width(), grey.get_height()
player_rect = pygame.Rect(0, 0, pwidth, pheight)
#grey = swap(grey, '#fbe939', '#ff0000')
grey.set_colorkey((0, 0, 0))

bg_objects = [[0.5, [120, 100, 90, 300]], [0.25, [150, 130, 70, 230]], [0.125, [170, 130, 100, 50]]]

grass = pygame.image.load('images/tiles/grassBlock.png')
dirt = pygame.image.load('images/tiles/dirtBlock.png')
dirtb = pygame.image.load('images/tiles/dirtBack.png')
tallgrass = pygame.image.load('images/tiles/tallGrass.png')
water = pygame.image.load('images/tiles/Water.png')
leaves = pygame.image.load('images/tiles/leafBlock.png')
wood = pygame.image.load('images/tiles/woodBlock2.png')

tile_index = {
    1:grass,
    2:dirt,
    3:tallgrass,
    4:water,
    5:leaves,
    6:wood
}

selected_tile = 1

TILESIZE = 16

tree_mapping =[
    [0,5,5,5,0],
    [5,5,5,5,5],
    [5,5,5,5,5],
    [0,5,4,5,5],
    [0,0,4,0,0],
    [0,0,4,0,0]
]

moving_left = False
moving_right = False
playery_momentum = 0

true_scroll = [0, 0]

map = {}

while True:
    display.fill((60, 170, 200))

    true_scroll[0] += (player_rect.centerx-true_scroll[0]-HALFWINDOW)/15
    true_scroll[1] += (player_rect.centery-true_scroll[1]-100)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (21, 50, 12), pygame.Rect(0, 100, 300, 100))

    for bg_object in bg_objects:
        obj_rect = pygame.Rect(bg_object[1][0]-scroll[0]*bg_object[0], bg_object[1][1]-scroll[1]*bg_object[0], bg_object[1][2], bg_object[1][3])
        if bg_object[0] == 0.5:
            pygame.draw.rect(display, (35, 100, 24), obj_rect)
        if bg_object[0] == 0.25:
            pygame.draw.rect(display, (56, 144, 32), obj_rect)
        if bg_object[0] == 0.125:
            pygame.draw.rect(display, (200, 215, 230), obj_rect)

    display.blit(grey, (player_rect.x-scroll[0], player_rect.y-scroll[1]))


    mx, my = pygame.mouse.get_pos()
    mx, my = ((mx+scroll[0]*2)//(TILESIZE*2)), (my+scroll[1]*2)//(TILESIZE*2)
    cx, cy = mx // CHUNK_SIZE, my // CHUNK_SIZE
    # draw_text(f'{mx}, {my}', 'black', (0, 0))
    # draw_text(f'{cx}, {cy}', 'black', (0, 20))
    tile_rects = []
    #render tiles
    for y in range(4):
        for x in range(4):
            target_x = x -1  + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y -1 + int(scroll[1]/(CHUNK_SIZE*16))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in map:
                map[target_chunk] = generate_chunks(target_x, target_y)
            for tile in map[target_chunk]:
                if tile[1] != 0:
                    display.blit(tile_index[tile[1]], (tile[0][0]*16-scroll[0], tile[0][1]*16-scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))
    
        for pos, tile in enumerate(map[f'{cx};{cy}']):
            if tile[0] == [mx, my]:
                if pygame.mouse.get_pressed()[0]:
                    map[f'{cx};{cy}'][pos] = tile[0], selected_tile
                elif pygame.mouse.get_pressed()[2]:
                    map[f'{cx};{cy}'][pos] = tile[0], 0
        if pygame.mouse.get_pressed(5)[4]:
            if selected_tile < len(tile_index):
                selected_tile += 1

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
    if collisions['right']:
        playery_momentum = -5

    surf = pygame.transform.scale(display, WINDOWSIZE)
    screen.blit(surf, (0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_a:
                moving_left = True
            elif event.key == K_d:
                moving_right = True
            elif event.key == K_SPACE:
                if collisions['bottom']:
                    playery_momentum = -5
            elif event.key == K_r:
                player_rect.bottomleft = (0, 0)
            
            elif event.key == K_t:
                moving_right = True

            elif event.key == K_LEFT:
                if selected_tile > 1:
                    selected_tile -= 1   
            elif event.key == K_RIGHT:
                if selected_tile < len(tile_index):
                    selected_tile += 1
        
        elif event.type == KEYUP:
            if event.key == K_a:
                moving_left = False
            
            if event.key == K_d:
                moving_right = False

    pygame.display.update()
    clock.tick(60)
