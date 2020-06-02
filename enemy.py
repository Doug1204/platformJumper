from random import choice
import os
import pygame

class Death:
    def __init__(self, screenHeight, width, height):
        self.y = screenHeight

        self.image = pygame.image.load(os.path.join(os.getcwd() + '\\enemy', choice(os.listdir(os.path.join(os.getcwd(), 'enemy')))))
        self.image = pygame.transform.scale(self.image, (width, height))
    
    def move(self, cutOff, man):
        if self.y > cutOff:
            self.y = cutOff
        else:
            change = min(15, max(man.score / 2500, 1))
            self.y -= int(change)
