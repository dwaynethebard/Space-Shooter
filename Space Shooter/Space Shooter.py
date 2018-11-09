# Space Shooter game by Darren Ytsma

import pygame, sys , math , random 


###############################
## initialize pygame and create window
pygame.init()
windowSurface = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()    ## For syncing the FPS

####################################
# Define Constants

# Define Colors
BLACK = (25, 25, 25)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
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
            text = font.render("Press Enter to start",True,RED)
            windowSurface.blit(text, [400, 300])
            
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
            enemy_ships_sprites_list.add(Enemy(pygame.image.load("Ship.jpg"),[x,y],30,30))

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
            upgrade.update()
            
        # Draw the players bullets
        player_bullets_sprites_list.draw(windowSurface)
        player_bullets_sprites_list.update()
        
        # Shooting
        if shooting:
            player.shoot()
        # Draw and update player

        
        player.draw()
        player.update()


        # timer for how often enemy shoots
        if time%60==59:
            for enemy in enemy_ships_sprites_list:
                a = random.randrange(0,20)
                if a%3==0:
                    enemy.shoot()
        
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
    
# Rotate the ships
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


# Calculate the distance between two points
def dist(pos1, pos2):
    a = pos2[1]-pos1[1]
    b = pos2[0]-pos1[0]
    dis = math.sqrt(a**2+b**2)
    return dis

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

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
                

#############################################
# Classes
# The basic Ship class for both player and enemy
class Ship(pygame.sprite.Sprite):
    def __init__(self, image, position,height,width):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (height,width)).convert()
        self.image.set_colorkey(BLACK)
        self.turn = 0
        self.turn_speed = 0
        
        self.rad = height
        self.height = height
        self.width = width
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.vel = [0,0]
        self.center = height/2
    # Draw the ship on the screen    
    def draw(self):
        windowSurface.blit(rot_center(self.image,self.turn), self.rect)
        
# Enemy ships, same as player, but bullets append to different list
# and needs to be always facing the player
class Enemy(Ship):
    # Create a seperate list of bullets for the enemys
    
    def shoot(self):
        enemy_bullets_sprites_list.add(Bullet(self.rect.center,6,self.turn))

    def update(self):
        self.player_angle(player)
        self.draw()
        
        
    def player_angle(self,other):
        x_dist = self.rect.x-other.rect.x
        y_dist = self.rect.y-other.rect.y
        self.turn = math.degrees(math.atan2(x_dist, y_dist))
        
        
        
# Player ship        
class Player(Ship):
    def __init__(self, image, position,height,width):
        super().__init__(image, position,height,width)
        self.shoot_delay = 900
        self.last_shot = pygame.time.get_ticks()
        self.speed = 3
        self.bullet_speed=6
    # Create a seperate list of bullets for the enemys                            
    def shoot(self):
         ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            player_bullets_sprites_list.add(Bullet(self.rect.center,self.bullet_speed,self.turn))
 # Update the position of the ship
    def update(self):
        player.hit_wall()
        self.turn+=self.turn_speed
        self.rect.x+=self.vel[0]
        self.rect.y+=self.vel[1]
        
            
    # Has the ship hit the boarder    
    def hit_wall(self):
        # if you are moving away from the boarder
        if (self.rect.x<=68 and self.vel[0]>0) or (self.rect.x>=704 and self.vel[0]<0):
            pass
        # If you hit the boarder you need to stop moving
        elif self.rect.x<=68 or self.rect.x>=704 :
            self.vel[0]=0
        # if you are moving away from the boarder    
        if (self.rect.y<=72 and self.vel[1]>0) or (self.rect.y>=504 and self.vel[1]<0):
            pass
        # If you hit the boarder you need to stop moving
        elif self.rect.y<=72 or self.rect.y>=504 :
            self.vel[1]=0


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, velocity,angle):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.bmp").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        self.vel = [-velocity*math.sin(math.radians(angle)),-velocity*math.cos(math.radians(-angle))]
        
    def draw(self):
        windowSurface.blit(self.image, self.rect)

    def update(self):
        if (self.rect.y<535 and self.rect.y>65 and self.rect.x<735 and self.rect.x>65)==False:
            self.kill()
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

# Powerup classes            
class Pow(pygame.sprite.Sprite):
    def __init__(self,pos):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Pick a rondom powerup
        self.pow_type=random.choice(["fire_rate","ship_speed"])
        self.image=power[self.pow_type]
        # Get the rectangle of the powerup
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        

    def draw(self):
        windowSurface.blit(self.image,[self.rect.x,self.rect.y])

    def update(self):
        if self.pow_type=="fire_rate":
            player.shoot_delay-=50
        elif self.pow_type=="ship_speed":
            player.speed+=1
            
#############################################
# Instance of objects
# Create player, and load background

player = Player(pygame.image.load("Ship.jpg"),[410,450],30,30)
background = pygame.image.load("space.bmp")
background=background.convert()

###############################################
# Load power ups

fire_rate = pygame.image.load("Fire_rate.bmp").convert()
ship_speed = pygame.image.load("ship speed.bmp").convert()
power = {"fire_rate":fire_rate,"ship_speed":ship_speed}
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
    
