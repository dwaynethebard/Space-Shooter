# Space Shooter game by Darren Ytsma

import pygame, sys , math , random 
from space_classes import *

###############################
## initialize pygame and create window

pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()    ## For syncing the FPS

####################################
# Define Constants

# Define Colors

RED = (255, 0, 0)
BLUE = (0, 0, 255)

HEIGHT = 600
WIDTH = 800
FPS = 60

# Global variables
#This will be a list that will contain all the sprites we intend to use in our game.
power_sprites_list = pygame.sprite.Group()
player_bullets_sprites_list = pygame.sprite.Group()
enemy_bullets_sprites_list = pygame.sprite.Group()
enemy_ships_sprites_list = pygame.sprite.Group()

time = 0
playing = True
shooting = False
current_score=0
total_score= 0
current_level =1
font = pygame.font.SysFont('Calibri', 25, True, False)



###################################
# Functions

def main_menu():
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            windowSurface.blit(font.render("Press Enter to start",True,RED), [400, 300])
            windowSurface.blit(font.render("Space to fire ",True,RED), [400, 350])
            windowSurface.blit(font.render("A,D to turn ",True,RED), [400, 400])
            windowSurface.blit(font.render("dpad to move ",True,RED), [400, 450])
            
            pygame.display.update()
    return False
def game_over():
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            text = font.render("Game Over",True,RED)
            windowSurface.blit(text, [400, 300])
            
            pygame.display.update()
def level(rate):
    global time ,enemy_bullets , power_ups,total_score
    current_score=0
    while True:
        event_handle()
        
        ## will make the loop run at the same speed all the time
        clock.tick(FPS)
        
        # Draw background and boarder
        windowSurface.blit(background, (0, 0))
        
        # Draw a green polygon onto the surface.
        # arguments draw.polygon(Surface,color,tuple/list of points,(optionally line thickness, fills if not specified)
        pygame.draw.polygon(windowSurface, BLUE, [[50, 50], [750, 50], [750, 550],[50,550],[50,50]],32)

    
        ############################################
        # Enemy Ships
        # Spawn enemy ships. Screen refreshes 60/sec.        
        if time % rate==0:
            # Set random position
            x = random.randrange(70,700)
            y = random.randrange(70,500)
            enemy_ships_sprites_list.add(Enemy(pygame.image.load("enemy ship.png"),[x,y],30,30))

        # Update enemy angle and draw ships
        enemy_ships_sprites_list.update()

        
        ############################################
        # Power Ups
        if time % 500 ==0:
            x = random.randrange(70,700)
            y = random.randrange(70,500)
            power_sprites_list.add(Pow([x,y]))

        power_sprites_list.draw(windowSurface)
        

        ############################################
        # Check for collision

        score_update=pygame.sprite.groupcollide(enemy_ships_sprites_list,player_bullets_sprites_list,True,True)

        for points in score_update:
            current_score+=100
            total_score+=100
            
        acquire_pow=pygame.sprite.spritecollide(player, power_sprites_list, True)

        ###############################################
        # Player Ship
        
        # Update ship powers
        for upgrade in acquire_pow:
            upgrade.update(player)
            
        # Draw the players bullets
        player_bullets_sprites_list.draw(windowSurface)
        player_bullets_sprites_list.update()
        
        # Shooting
        if shooting:
            player.shoot(player_bullets_sprites_list)
        # Draw and update player

        
        player.draw()
        player.update()


        # timer for how often enemy shoots
        if time%60==59:
            for enemy in enemy_ships_sprites_list:
                a = random.randrange(0,20)
                if a%3==0:
                    enemy.shoot(enemy_bullets_sprites_list)
        
        enemy_bullets_sprites_list.draw(windowSurface)
        enemy_bullets_sprites_list.update()

        text = font.render(str(current_level),True,RED)
        windowSurface.blit(font.render("Level",True,RED), [510, 570])
        windowSurface.blit(text, [570, 570])
        windowSurface.blit(font.render("Score",True,RED), [370, 570])
        windowSurface.blit(font.render(str(total_score),True,RED), [440, 570])
        # Draw the window onto the screen.
        pygame.display.update()

        time+=1
        if pygame.sprite.spritecollideany(player,enemy_bullets_sprites_list):
            game_over()
        # Are we at the next level?
        if current_score!=0 and current_score % 1000==0:
            break
    

def event_handle():
    global shooting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
     
        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                player.vel[0]=-player.speed
            elif event.key == pygame.K_RIGHT:
                player.vel[0]=player.speed
            elif event.key == pygame.K_UP:
                player.vel[1]=-player.speed
            elif event.key == pygame.K_DOWN:
                player.vel[1]=player.speed
            elif event.key == pygame.K_d:
                player.turn_speed=-math.pi
            elif event.key == pygame.K_a:
                player.turn_speed=math.pi
            elif event.key == pygame.K_SPACE:
                shooting=True
                
     
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.vel[0]=0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.vel[1]=0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.turn_speed=0
            elif event.key == pygame.K_SPACE:
                shooting=False
                



####################################################
# Game Loop
    
menu = True    
while True:
    event_handle()
    if menu:
        menu=main_menu()
    ####################################################################################
    # Call level 1 , 2 ,3, 4,5 level 5 is endless mode
    # difference between levels are the spawn rate and fireing rate on enemy
    spawn_rate = int(5*3.1** -(0.05*current_level-2.5))
    level(spawn_rate)
    current_level+=1
