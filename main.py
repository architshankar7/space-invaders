import pygame
import random
import math

#insert ability to game over, difficult levels based on thresholds, collision between enemy and player
#initializes pygame
pygame.init()

#initializes color schemes
white = (255, 255, 255)
black = (0, 0, 0)

#background
background = pygame.image.load("Space Invaders Background.jpeg")

#creates game screen
screen = pygame.display.set_mode((800, 600))

#Title and icon of game
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Space Invaders Icon.png")
pygame.display.set_icon(icon)

#Player starting location and image
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("Alien Spaceship.png"))
    enemyX.append(random.randint(1, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(50)

#Bullet
#If ready, bullet is not on screen, otherwise not ready
bulletImg = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = 480
bulletY_change = 10
bulletState = "ready"

#score
score = 0
font = pygame.font.Font("freesansbold.ttf", 16)
scoreX = 10
scoreY = 10

#lives
lives = 3
livesX = 730
livesY = 10


def show_score(score, white, x, y):
    score = font.render("Score: " + str(score), True, white)
    screen.blit(score, (x, y))


def show_lives(lives, white, x, y):
    lives = font.render("Lives: " + str(lives), True, white)
    screen.blit(lives, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 25, y - 10))


def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2)) + (math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


#game loop, while game is running
running = True
while running:
    # RGB, in order of numbers listed
    screen.fill(black)
    #background insert
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        #User chooses to quit game
        if event.type == pygame.QUIT:
            running = False
        #if key is pressed check whether it is left or right or space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if bulletState is "ready":
                if event.key == pygame.K_SPACE:
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    #show change in spaceship location
    playerX += playerX_change

    #reset player position if traveling outside bounds
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0

    #bullet movement
    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY < 0:
            bulletY = 480
            bulletState = "ready"

    #enemy movement
    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = (enemyX_change[i]) * -1
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = (enemyX_change[i]) * -1

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bulletState = "ready"
            score += 1
            enemyX[i] = random.randint(1, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #inserts player location onto screen
    player(playerX, playerY)

    #shows score and lives
    show_score(score, white, scoreX, scoreY)
    show_lives(lives, white, livesX, livesY)
    #updates game window display
    pygame.display.update()

    # SET GAME SPEED
    fps = 60
    clock = pygame.time.Clock()
    clock.tick(fps)