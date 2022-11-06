
#packages
import pygame
import sys
import math

#initialisation
pygame.init()

#consonants
screen_height = 480
screen_width = screen_height * 2
map_size = 8
tile_size = int((screen_width/2)/map_size)
max_depth = int(map_size * tile_size)
fov = math.pi / 3 
half_fov = fov / 2
casted_rays = 120
step_angle = fov / casted_rays
scale = (screen_width / 2) / casted_rays


#variable
player_x = (screen_width / 2) / 2
player_y = (screen_width / 2) / 2
player_angle = math.pi

#map
gamemap = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '#      #'
    '#  ##  #'
    '#   #  #'
    '########'
)

#game window
win = pygame.display.set_mode((screen_width,screen_height))

#caption
pygame.display.set_caption('Raycasting')

#timer init
clock = pygame.time.Clock()

#draw map
def draw_map():
    for row in range(8):
        for col in range(8):
            square = row * map_size + col
            pygame.draw.rect(
                win,
                (200, 200, 200) if gamemap[square] == '#' else (100, 100, 100),
                (col * tile_size, row*tile_size, tile_size - 2, tile_size - 2)
            )
    #draw player on 2d        
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)

    #draw player direction
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle) * 30, 
                                        player_y + math.cos(player_angle) * 30), 3)
    #draw player FOV (-)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle - half_fov) * 30, 
                                        player_y + math.cos(player_angle - half_fov) * 30), 3)
    # draw player FOV (+)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle + half_fov) * 30, 
                                        player_y + math.cos(player_angle + half_fov) * 30), 3)

# Raycasting ALgorithm
def cast_rays():
    #defining the left most angle of the fov
    start_angle = player_angle - half_fov
    
    #casted rays loop
    for rays in range(casted_rays):
        # cast ray step by step
        for depth in range(max_depth ):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            
            col = int(target_x / tile_size)
            row = int(target_y / tile_size)
            square = row * map_size + col
            

            if gamemap[square] == '#':
                pygame.draw.rect(win, (0, 255, 0), (col * tile_size,
                                                    row * tile_size,
                                                    tile_size - 2,
                                                    tile_size - 2 ))
                #draw casted ray
                pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y))

                #wall shading
                colour = 255 / (1 + depth * depth * 0.0001)

                #fix fish eye effect
                depth *= math.cos(player_angle - start_angle)
                 
                #  calculate wall height
                wall_height = 21000 / (depth + 0.0001)

                #i forgot to comment
                if  wall_height  > screen_height: wall_height = screen_height

                #draw 3d walls
                pygame.draw .rect(win, (colour, colour, colour), (
                    screen_height + rays  * scale,
                    (screen_height / 2) - wall_height / 2,
                    scale, wall_height))
                
                break


        #increment angle by a single step
        start_angle += step_angle

forward = True

#Game loop
while True:
    #exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

    col = int(player_x / tile_size)
    row = int(player_y / tile_size)
    square = row * map_size + col
            
    # i cant go through walls
    if gamemap[square] == '#':
        if forward:
            player_x -= math.sin(player_angle) * 3
            player_y -= math.cos(player_angle) * 3
        else:
            player_x += math.sin(player_angle) * 3
            player_y += math.cos(player_angle) * 3

    #update 2d background
    pygame.draw.rect(win, (100, 100, 100), (480, screen_height / 2 , screen_height, screen_height))
    pygame.draw.rect(win, (200, 200, 200), (480, - screen_height / 2 , screen_height, screen_height))

    # update 3d background

    
    #calling functions
    draw_map()
    cast_rays()

    #recieve user input
    keys = pygame.key.get_pressed()

    #user input handling
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += math.sin(player_angle) * 3
        player_y += math.cos(player_angle) * 3
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= math.sin(player_angle) * 3
        player_y -= math.cos(player_angle) * 3

  

    #set fps
    clock.tick(30)
    
    #display fps
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont(None, 30)
    fps_surface = font.render(fps, False, (255, 255, 255))
    win.blit(fps_surface, (480, 0))

      #update display
    pygame.display.flip()
