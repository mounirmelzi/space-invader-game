import pygame
import Colors
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Game Constantes
WINDOW_H = 600 # Y = 600
WINDOW_W = 800 # X = 800
PLAYER_SIZE = (64, 64) # Image pixels (X, Y)
ENEMY_SIZE = (64, 64) # Image pixels (X, Y)
BULLET_SIZE = (32, 32) # Image pixels (X, Y)

# Creat the screen
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))

# Background
# the size of the background image should be the same as the window size
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("player.png")
playerX = WINDOW_W//2 - PLAYER_SIZE[0]//2 + 2 # 370
playerY = WINDOW_H - PLAYER_SIZE[1] - 56 # 480
playerX_change = 0
player_dx = 12 # Player Speed

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemyimg.append( pygame.image.load('enemy.png') )
    enemyX.append( random.randint(0, WINDOW_W - ENEMY_SIZE[0]) )
    enemyY.append( random.randint(50, 150) )
    enemyX_change.append( 5 ) # Enemy Speed
    enemyY_change.append( 40 )


# Bullet
# bullet states:
    # ready : you can't see the bullet on the screen
    # fire : the bullet is currently moving 
bulletimg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletX_change = 0 # the bullet doesn't move in the X axis
bulletY_change = 25 # Bullet Speed in the Y axis
bullet_state = 'ready'


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
TEXTX, TEXTY = (10, 10)


# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)



def show_score(x, y):
    score = font.render(f'Score : {score_value}', True, Colors.SILVER, None)
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render('Game Over', True, Colors.RED)
    screen.blit(over_text, (x, y))


def player(x, y):
    # blit = to draw 
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state 
    global PLAYER_SIZE
    global BULLET_SIZE
    bullet_state = 'fire'
    x_val = x + ( PLAYER_SIZE[0] - BULLET_SIZE[0] ) //2    # x_val = x + 16
    y_val = y + ( 5 * BULLET_SIZE[1] ) // 16    # y_val = y + 10
    screen.blit(bulletimg, (x_val, y_val))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = (((enemyx-bulletx)**2) + ((enemyy-bullety)**2)) ** 0.5
    limit = 27
    return (distance < limit)



# Game Loop
running = True
while running:
    # FPS
    pygame.time.Clock().tick(60)
    
    # RGB Colors (red, green, blue)
    screen.fill(Colors.BLACK)
    # Background image
    screen.blit(background, (0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether its right or left
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = - player_dx

            elif event.key == pygame.K_RIGHT:
                playerX_change = player_dx

            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    mixer.Sound('laser.wav').play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # check if keystroke has been released
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0


    # checking for boundaries of spaceship
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX + PLAYER_SIZE[0] > WINDOW_W:
        playerX = WINDOW_W - PLAYER_SIZE[0]

    for i in range(number_of_enemies):

        # Game Over
        if enemyY[i] + ENEMY_SIZE[1] > playerY:
            for j in range(number_of_enemies):
                enemyY[j] = WINDOW_H + ENEMY_SIZE[1] # Mask all enemies from the screen
            game_over_text(WINDOW_W//2 - 20*len('Game Over'), WINDOW_H//2 - 5*len('Game Over'))
            break


        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] + ENEMY_SIZE[0] > WINDOW_W:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            mixer.Sound('explosion.wav').play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, WINDOW_W - ENEMY_SIZE[0])
            enemyY[i] = random.randint(50, 150) 

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY < 0:
        bulletY = playerY
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        

    player(playerX, playerY)
    show_score(TEXTX, TEXTY)
    pygame.display.update()

