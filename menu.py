import pygame
import os
from random import choice
import json


import main


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

def buildMenu(bg, start, customize, viewPast):

    gameDisplay.blit(bg, (0, 0))

    pygame.draw.rect(gameDisplay, red, start)
    display('Play', start[0] + start[2] // 6, start[1] + start[3] // 3.5, 50)

    pygame.draw.rect(gameDisplay, red, customize)
    display('Customize', customize[0] + customize[2] // 7, customize[1] + customize[3] // 3, 35)

    pygame.draw.rect(gameDisplay, red, viewPast)
    display('High Scores', viewPast[0] + viewPast[2] // 8, viewPast[1] + viewPast[3] // 3, 35)


def loadImages(charcterType, tileType, coinType, backgroundType):

    lst = os.listdir(os.path.join(os.getcwd(), charcterType))

    amount = []
    actions = ('Run', 'Idle', 'Jump')

    for action in ('Run', 'Idle', 'Jump'):
        amount.append(list(map(lambda x: x[:3], lst)).count(action[:3]))
    
    characterImages = []

    for index, action in enumerate(actions):
        load =  [pygame.image.load(os.path.join(os.getcwd(), charcterType + f'\\{action} ({i}).png')) for i in range(1, amount[index] + 1)]
        scale = [pygame.transform.scale(i, (characterSize, characterSize)) for i in load]
        characterImages.append(scale)


    tileImages = [pygame.image.load(os.path.join(os.getcwd() + f'\\tiles\\{tileType}', f'{i}.png')) for i in range(8)]
    tileImages = [pygame.transform.scale(image, (tileSize[0], tileSize[1])) for image in tileImages]

    coinImages = [pygame.image.load(os.path.join(os.getcwd() + f'\\coinImages\\{coinType}', f'{coinType}_{i}.png')) for i in range(1, 31)]
    coinImages = [pygame.transform.scale(image, (coinSize[0], coinSize[1])) for image in coinImages]

    bg = pygame.image.load(os.path.join(os.getcwd(), f'BGs\\{backgroundType}.png'))
    bg = pygame.transform.scale(bg, (displayWidth, displayHeight))

    os.system('cls')

    return characterImages, tileImages, coinImages, bg

def display(text, x, y, font_size):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(str(text), True, black)
    gameDisplay.blit(text,(x, y))

def buttons(start, customize, viewPast):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
    mouse = pygame.mouse.get_pos()
    if start[0] < mouse[0] <= start[0] + start[2] and start[1] < mouse[1] <= start[1] + start[3]:
        if pygame.mouse.get_pressed()[0]:
            return 'play'
    
    if customize[0] < mouse[0] <= customize[0] + customize[2] and customize[1] < mouse[1] <= customize[1] + customize[3]:
        if pygame.mouse.get_pressed()[0]:
            return 'customize'

    if viewPast[0] < mouse[0] <= viewPast[0] + viewPast[2] and viewPast[1] < mouse[1] <= viewPast[1] + viewPast[3]:
        if pygame.mouse.get_pressed()[0]:
            return 'viewPast'

def viewPastButtons(bd):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mouse = pygame.mouse.get_pos()
    return bd[0] < mouse[0] <= bd[0] + bd[2] and bd[1] < mouse[1] <= bd[1] + bd[3] and pygame.mouse.get_pressed()[0]

def viewPast(bgImage):

    back = False

    with open('scores.json') as f:
        data = json.load(f)

    while not back:
    
        gameDisplay.blit(bgImage, (0, 0))

        y = lambda i: i * 80 + 75

        for num in range(5):
            display(data[num]["name"], displayWidth * 0.33, y(num), 45)
            display(data[num]["score"], displayWidth * 0.58, y(num), 45)

        buttonDimensions = [displayWidth * 0.45, displayHeight * 0.8, displayWidth * 0.1, displayHeight * 0.1]
        pygame.draw.rect(gameDisplay, red, buttonDimensions)
        display('Back', buttonDimensions[0] + buttonDimensions[2] * 0.2, buttonDimensions[1] + buttonDimensions[3] * 0.25, 35)
        
        back = viewPastButtons(buttonDimensions)

        pygame.display.update()


def buildCustomize(types, currents, bgImage):

    gameDisplay.blit(bgImage, (0, 0))

    buttonDimension = displayWidth // 18
    white = (255, 255, 255)

    options = ['character', 'tiles', 'coins', 'background']
    for name, current in zip(options, currents):
        y = options.index(name) * 100 + 100
        buttonY = y - 15

        pygame.draw.rect(gameDisplay, red, [displayWidth * 0.45, buttonY, buttonDimension, buttonDimension])
        pygame.draw.rect(gameDisplay, red, [displayWidth * 0.65, buttonY, buttonDimension, buttonDimension])

        points1 = [[displayWidth * 0.46, buttonY + buttonDimension / 2], [displayWidth * 0.44 + buttonDimension, buttonY + displayHeight * 0.01], [displayWidth * 0.44 + buttonDimension, buttonY + buttonDimension - displayHeight * 0.01]]
        pygame.draw.polygon(gameDisplay, white, points1)
        points2 = [[displayWidth * 0.64 + buttonDimension, buttonY + buttonDimension / 2], [displayWidth * 0.66, buttonY + displayHeight * 0.01], [displayWidth * 0.66, buttonY + buttonDimension - displayHeight * 0.01]]
        pygame.draw.polygon(gameDisplay, white, points2)

        
        display(name, displayWidth * 0.25, y, 35)
        display(current, displayWidth * 0.525, y, 35)
    
    pygame.draw.rect(gameDisplay, red, [displayWidth * 0.4, displayHeight * 0.85, buttonDimension * 4, buttonDimension])
    display('Save', displayWidth * 0.47, displayHeight * 0.87, 35)
        

def customizeButtons(types, currents):

    buttonDimension = displayWidth // 18

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    getY = lambda i: i * 100 + 85

    x1 = displayWidth * 0.45
    x2 = displayWidth * 0.65
    
    mouse = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:

        xCheck = displayWidth * 0.4 < mouse[0] <= displayWidth * 0.4 + buttonDimension * 4
        yCheck = displayHeight * 0.85 < mouse[1] <= displayHeight * 0.85 + buttonDimension * 4
        if xCheck and yCheck:
            return currents, True

        for index, t in enumerate(types):
            yCheck = getY(index) < mouse[1] <= getY(index) + buttonDimension
            xCheck = 0
            if x1 < mouse[0] <= x1 + buttonDimension:
                xCheck = -1
            elif x2 < mouse[0] <= x2 + buttonDimension:
                xCheck = 1
            while xCheck and yCheck:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        i = t.index(list(set(currents).intersection(t))[0]) + xCheck
                        if i >= len(t):
                            i = 0
                        currents[index] = t[i]
                        xCheck = 0

    return currents, False

    
def customize(character, tiles, coins, bg, bgImage):

    bgTypes = ['treetop', 'graveyard']
    characterTypes = ['pumpkin', 'dinosaur']
    tileTypes = ['grass', 'snow', 'swamp']
    coinTypes = ['Bronze', 'Silver', 'Gold']
    types = [characterTypes, tileTypes, coinTypes, bgTypes]
    currents = [character, tiles, coins, bg]

    choosing = True

    while choosing:

        buildCustomize(types, currents, bgImage)

        currents, back = customizeButtons(types, currents)

        if back:
            choosing = False

        pygame.display.update()


    return currents
    

def mainMenu(default):

    tileTypes = ['grass', 'snow', 'swamp']
    bgTypes = ['treetop', 'graveyard']
    characterTypes = ['pumpkin', 'dinosaur']
    coinTypes = ['Bronze', 'Silver', 'Gold']

    if not default:
        character, tiles, coins, bg = choice(characterTypes), choice(tileTypes), choice(coinTypes), choice(bgTypes)
    else:
        character, tiles, coins, bg = default

    bgImage = pygame.image.load(os.path.join(os.getcwd(), f'BGs\\{bg}.png'))
    bgImage = pygame.transform.scale(bgImage, (displayWidth, displayHeight))

    finalised = False

    while not finalised:

        largeWidth = displayWidth // 8
        largeHeight = displayHeight // 8

        smallWidth = displayWidth * 0.2
        smallHeight = displayHeight // 8

        startButton = [int(displayWidth * 0.5 - largeWidth / 2), int(displayWidth * 0.1), largeWidth, largeHeight]
        customizeButton = [int(displayWidth * 0.2), int(displayWidth * 0.3), smallWidth, smallHeight]
        viewPastButton = [int(displayWidth * 0.6), int(displayWidth * 0.3), smallWidth, smallHeight]

        buildMenu(bgImage, startButton, customizeButton, viewPastButton)

        output = buttons(startButton, customizeButton, viewPastButton)
        if output == 'play':
            finalised = True
        elif output == 'customize':
            character, tiles, coins, bg = customize(character, tiles, coins, bg, bgImage)

            bgImage = pygame.image.load(os.path.join(os.getcwd(), f'BGs\\{bg}.png'))
            bgImage = pygame.transform.scale(bgImage, (displayWidth, displayHeight))

        elif output == 'viewPast':
            viewPast(bgImage)


        pygame.display.update()
        clock.tick(60)

    return (loadImages(character, tiles, coins, bg)), [character, tiles, coins, bg]
    
if __name__ == '__main__':
    mainMenu(None)