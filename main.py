import pygame
import random
import math

from pygame import mixer
from pygame.locals import *


#inialize the pygame
pygame.init()

#create a screen
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('img/bg.jpg')

#background music
# mixer.music.load('sound/background.wav')
# mixer.music.play(-1)


#Tittle/caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('img/ufo.png')
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load('img/png/001-space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6;

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('img/png/002-alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(60, 300))
    enemyX_change.append(0.4)
    enemyY_change.append(40)



#Bullet

# ready - you cant see the bullet on the screen
# fire - the bullet is currently moving

bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY =480 
bulletX_change = 0
bulletY_change = 4 
bullet_state = "ready"

# Score 

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over font
over_font = pygame.font.Font('freesansbold.ttf', 64)




 
def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))



def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x , y, i):
    screen.blit(enemyImg[i], (x, y))
    # screen.blit(enemyImg1, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))



def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False



#GAME LOOP
running = True;
while running:
    #RGB
    screen.fill((0, 0, 0))
    #Background image
    screen.blit(background, (0,0))
    pygame.draw.line(screen,(128, 9, 9),(0,475), (800,475), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        #if keystroke is pressed check if its left or right   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_SPACE: 
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sound/laser.wav')
                    bullet_sound.play()
                    #get the current x coordunate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    #PLAYER MOVEMENT
    playerX += playerX_change

    # Adding Boundaries for our player so it dosent go out of screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    #ENEMY MOVEMENT
    for i in range(num_of_enemies):

        #GAME OVER
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        # Adding Boundaries for our enemy so it dosent go out of screen
        # enemy_boundary(enemyX, enemyX_change) 
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4 
            enemyY[i] += enemyY_change[i]

        #COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('sound/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1 
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(60, 300)
        
        enemy(enemyX[i], enemyY[i], i)

        




    #BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480 
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change 


    



    player(playerX, playerY)
    show_score(textX, textY)
    enemy(enemyX[i], enemyY[i], i )
    pygame.display.update()


