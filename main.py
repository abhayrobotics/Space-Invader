import pygame
import random
import math
from pygame import mixer
import time
#  initialse the pygame
pygame.init()

# create the Screen
screen = pygame.display.set_mode((800, 600))

# TITLE AND LOGO
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('gallery/icon3.png')
pygame.display.set_icon(icon)

# Background
backgroundImg = pygame.image.load('gallery/background2.png')

# Background Sound
mixer.music.load('audio/music.mp3')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('gallery/player.png')
playerx = 370
playery = 480
playerX_change = 0

# Bullet
bulletImg = pygame.image.load('gallery/bullet.png')
bulletx = 370
bullety = 480
bulletY_change = 0
bullet_state = "ready"

# Enemy
no_of_enemies = 7
enemyImg = []
enemyx = []
enemyy = []
enemyX_change = []
enemyY_change = []

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('gallery/enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(60, 150))
    enemyX_change.append(-3)
    enemyY_change.append(30)

# Score
score = 0
# font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('font/Chocolate Valentine.otf', 45)
textX = 620
textY = 20


def show_score(x, y):
    score_object = font.render("Score: " + str(score), True, (255, 0, 0))
    screen.blit(score_object, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def randEnemy(x, y):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if distance < 32:
        return True
    else:
        return False


# GAME LOOP
running = True
while running:

    # RGB value
    screen.fill((0, 0, 0))

    # background img
    screen.blit(backgroundImg, (0, 0))
    # movement -y  ie going above
    # playery -=0.1
    # Event
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        #  check when keystore is pressed
        if event.type == pygame.KEYDOWN:
            # print("A Keystroke is Pressed", playerx)
            if event.key == pygame.K_LEFT:
                # print("Left")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = +5
                # print("Right")
            # Firing bullet
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletx = playerx + 16
                    bullety = playery + 5
                    bulletY_change = -10
                    bullet_sound = mixer.Sound('audio/bullet.wav')
                    bullet_sound.play()
                    bullet_state = "fire"

        #  check when keystore is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke is released")
                playerX_change = 0  # when released no movement

    # When bullet exits the  screen , then only you can fire
    if bullety <= 0:
        bullet_state = "ready"

    # if exits from window take back inside screen
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    #    bullet will be shown only when its in fire state
    if bullet_state is "fire":
        bullet(bulletx, bullety)


    for i in range(no_of_enemies):

        # if  Enemy exits from window take back inside screen
        if enemyx[i] <= 0:
            # enemyx[i] = 0
            enemyy[i] = enemyy[i] + enemyY_change[i]
            enemyX_change[i] += 3

        # if enemyy[i] <=0
        if enemyx[i] >= 736:
            # enemyx[i] = 736
            enemyy[i] = enemyy[i] + enemyY_change[i]
            enemyX_change[i] -= 3

        # enemy movement
        enemyx[i] += enemyX_change[i]

        # Collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 480
            bulletY_change = 0
            bullet_state = "ready"
            score += 1
            print(f"Score {score}")
            explosion_sound = mixer.Sound('audio/point.wav')
            explosion_sound.play()
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(60, 150)

        randEnemy(enemyx[i], enemyy[i])

    # game over
    for y in enemyy:
        if y >= 480-64:

            font2 = pygame.font.Font('font/Chocolate Valentine.otf', 200)
            game_over = font2.render("GAME OVER",True,(0,0,0))
            screen.blit(game_over,(0,100))
            running = "game over"


    # player movement
    playerx += playerX_change

    # bullet movement
    bullety += bulletY_change

    player(playerx, playery)
    show_score(textX, textY)
    # updating the game , mostly the last line
    pygame.display.update()
    # screen will show GAME OVER FOR 2 sec before program end
    if running == "game over":
        time.sleep(3)
        running = False