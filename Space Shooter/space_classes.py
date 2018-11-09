#############################################
# Classes for the space shooter, by Darren Ytsma

import pygame, math , random
from pygame_functions import *
###############################
## initialize pygame and create window

pygame.init()
windowSurface = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()    ## For syncing the FPS

BLACK = (25, 25, 25)

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
    
    def shoot(self,enemy_bullets_sprites_list):
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
    def shoot(self,player_bullets_sprites_list):
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


            
#############################################
# Instance of objects
# Create player, and load background

player = Player(pygame.image.load("Ship.jpg"),[410,450],30,30)
background = pygame.image.load("space.bmp")
background=background.convert()


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

    def update(self,player):
        if self.pow_type=="fire_rate":
            player.shoot_delay-=50
        elif self.pow_type=="ship_speed":
            player.speed+=1


###############################################
# Load power ups

fire_rate = pygame.image.load("Fire_rate.bmp").convert()
ship_speed = pygame.image.load("ship speed.bmp").convert()
power = {"fire_rate":fire_rate,"ship_speed":ship_speed}
