import pygame
import pygame.locals
from itertools import cycle
import os
from random import choice, randint

import character
import platform
import coin
import enemy
import menu
import gameOver

#without a hundred smells of blood

pygame.init()
pygame.display.set_caption('Game')

displayWidth = 900
displayHeight = 600
characterSize = 100
tileSize = (displayWidth // 24, displayHeight // 12)
coinSize = (displayWidth // 18, displayHeight // 12)

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

red = (255, 0, 0)
black = (0, 0, 0)


def build(man, platforms, platformImages, tokens, tokenImages, death, bg):

    gameDisplay.blit(bg, (0, 0))

    menu.display(f'Score: {man.score}', 0, 0, 25)
    
    for platform in platforms:
        for i in platform.x.keys():

            gameDisplay.blit(platformImages[platform.x[i][0]], (i[0], platform.y))

            for distance in range(1, (i[1] - i[0]) // platform.width - 1):

                gameDisplay.blit(platformImages[platform.x[i][1]], (i[0] + (platform.width * distance), platform.y))

            gameDisplay.blit(platformImages[platform.x[i][2]], (i[0] + (platform.width * (distance + 1)), platform.y))


    for token in tokens:
        gameDisplay.blit(tokenImages[token.currentImage], (token.x, token.y))

    gameDisplay.blit(death.image, (0, death.y))


def moveDown(platforms):
    for platform in platforms:
        platform.y += 1

def eliminate(man, platforms, tokens):
    for platformMade in platforms:

        if platformMade.y > displayHeight * 1.5:

            platforms.remove(platformMade)
            platforms.append(platform.Platform(platforms[-1], displayWidth, displayHeight, man.score))

            tokens = addToken(platforms[-1], tokens)
    
    for token in tokens:
        if token.y > displayHeight * 1.5:
            tokens.remove(token)

    return platforms, tokens

def adjustY(man, oldMan, platforms, tokens, death):

    deltaY = oldMan - man.currentPlatform.y - man.jumpAddition

    for platform in platforms:
        platform.y += deltaY

    for token in tokens:
        token.y += deltaY

    death.y += deltaY
    death.move(displayHeight + 200, man)

    if deltaY > 0:
        man.score += deltaY

def addToken(platform, tokens):

    if not randint(0, 2) or not tokens:

        rng = choice(list(platform.x.keys()))
        tokens.append(coin.Coin(randint(rng[0]+25, rng[1]-100), platform.y - 60))

    return tokens
    
def movement(man, movementDue, speed, platforms):

    keyinput = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    xAxis = man.checkX(man.currentPlatform.x)

    if keyinput[pygame.K_UP] and man.air == 11 and xAxis:
        man.air = -10
    
    if keyinput[pygame.K_DOWN] and man.air == 11:
        man.down = True

    if keyinput[pygame.K_LEFT]:
        man.left(displayWidth)
        man.turn('left')

    elif keyinput[pygame.K_RIGHT]:
        man.right(displayWidth)
        man.turn('right')

    else:
        man.currentImages = man.images[1]
        if movementDue == speed:
            man.speed = 0

def gameLoop(characterImages, tileImages, tokenImages, bg):
    
    playing = True
    platforms = []
    tokens = []

    platforms.append(platform.Platform(None, displayWidth, displayHeight, 0))

    for _ in range(8):
        platforms.append(platform.Platform(platforms[-1], displayWidth, displayHeight, 0))
        tokens = addToken(platforms[-1], tokens)

    man = character.Character(characterImages, characterSize, platforms[0])
    death = enemy.Death(displayHeight, displayWidth, 400)

    speed = 3
    movementDue = 0
    changeInManY = 0

    while playing:
        
        if movementDue >= speed:

            changeInManY = man.currentPlatform.y + man.jumpAddition

            build(man, platforms, tileImages, tokens, tokenImages, death, bg)

            for token in tokens:
                token.animate()
            
            if man.checkDead(death):
                playing = False
            
            if man.down:

                index = platforms.index(man.currentPlatform) - 1

                if index >= 0:
                    man.currentPlatform = platforms[index]
                    man.air = man.currentPlatform.air
                else:
                    playing = False
                
                man.down = False
            

            man.jump()

            man.findPlatform(platforms)
            man.checkStillOn(platforms)

            tokens = man.coinCheck(tokens)

            platforms, tokens = eliminate(man, platforms, tokens)

            adjustY(man, changeInManY, platforms, tokens, death)

            gameDisplay.blit(man.image(), (man.x, man.currentPlatform.y - man.height + man.jumpAddition))

            movementDue = 0
        
        movement(man, movementDue, speed, platforms)
        
        movementDue += 1

        pygame.display.update()
        clock.tick(60)
    
    return man

default = None

while __name__ == '__main__':
    customization, default = menu.mainMenu(default)
    os.system('cls')
    mainCharacter = gameLoop(*customization)
    gameOver.end(customization[3], mainCharacter)
    