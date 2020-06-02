import pygame
import os
import json
from random import choice

import menu

pygame.init()
pygame.display.set_caption('Game')

displayWidth = 900
displayHeight = 600
characterSize = 100

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

red = (255, 0, 0)
black = (0, 0, 0)

def buildEnd(bg, character, name, quote):

    gameDisplay.blit(bg, (0, 0))

    gameDisplay.blit(character.image(), (displayWidth * 0.1, displayHeight * 0.7))

    pygame.draw.rect(gameDisplay, red, [displayWidth * 0.2, displayHeight * 0.05, displayWidth * 0.6, displayHeight * 0.5])

    menu.display('GAME OVER', displayWidth * 0.25, displayHeight * 0.1, 100)

    xQuotes = displayWidth / 2  - (len(quote) * 14 / 2)

    menu.display(quote, xQuotes, displayHeight * 0.28, 40)
    menu.display(f'Your score was {character.score}', displayWidth * 0.37, displayHeight * 0.35, 35)

    menu.display('Enter Name:', displayWidth * 0.4, displayHeight * 0.45, 30)
    menu.display(name, displayWidth * 0.55, displayHeight * 0.45, 30)

def getText(name):

    enter = False

    event = pygame.event.poll()
    keys = pygame.key.get_pressed()

    if event.type == pygame.KEYDOWN:
        key = pygame.key.name(event.key)

        if len(key) == 1:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                name += key.upper()
            else:
                name += key
        elif key == pygame.K_SPACE:
            name += ' '
        elif key == "backspace":
            name = name[:-1]
        elif event.key == pygame.K_RETURN:
            enter = True
    
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

    if len(name) >= 11:
        name = name[:-1]

    return [name, enter]


def end(bg, character):

    name = ('', False)

    character.currentImages = character.images[1]
    character.air = 11
    character.turn('right')

    quotes = ['Congrats!!!!!', 'Well, at least you tried', 'Ha lol', 'Still a failure, I see', 'How old are you? 5?']
    quote = choice(quotes)

    gettingName = True

    while gettingName:
    
        buildEnd(bg, character, name[0], quote)

        name = getText(name[0])

        if name[1] and name[0].isalpha():

            name[0] = name[0].capitalize()

            with open('scores.json') as f:
                data = json.load(f)
            
            names = [user["name"] for user in data]

            while name[0] in names:

                nums = 0
                for char in name[0]:
                    if char.isdigit():
                        nums += 1

                if nums:
                    number = name[0][-nums:]
                    name[0] = name[0].replace(number, str(int(number) + 1))
                else:
                    name[0] += '_2'

            data.append({"name": name[0], "score": character.score})
            
            data = sorted(data, key=lambda x: -x['score'])

            with open('scores.json', 'w') as outfile:
                json.dump(data, outfile)
            
            gettingName = False

        pygame.display.update()
        clock.tick(60)


