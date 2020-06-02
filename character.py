import os
import pygame
from itertools import cycle

class Character:
    def __init__(self, images, size, base):

        self.width = size
        self.height = size

        self.images = images

        self.currentImages = self.images[0]

        self.currentImage = 0
        self.currentPlatform = base
        self.direction = 'right'
        self.x = 440
        self.jumpAddition = 0
        self.speed = 6
        self.air = 11
        self.down = False
        self.score = 0

    def jump(self):
        if self.air < 11:
            self.jumpAddition = int((-(self.currentPlatform.chosenHeight / 100) * self.air ** 2 + self.currentPlatform.chosenHeight) * -10)
            self.air += 1

    def checkX(self, coords):
        for i in coords:
            if i[0] - self.width * 0.75 < self.x < i[1] - self.width * 0.4:
                return True
        return False
        
    
    def findPlatform(self, platforms):
        for platform in platforms[::-1]:
            xAxis = self.checkX(platform.x)
            if platform.y == self.currentPlatform.y + self.jumpAddition and xAxis and self.air > 0:
                self.currentPlatform.air = self.air
                self.currentPlatform = platform
                self.jumpAddition = 0
                self.air = 11
                break
    
    def checkStillOn(self, platforms):
        xAxis = self.checkX(self.currentPlatform.x)
        if not xAxis and self.air == 11:
            self.down = True
    
    def checkDead(self, death):
        return self.currentPlatform.y + self.jumpAddition > death.y

    def right(self, width):
        if self.speed < 6:
            self.speed += 1
        self.currentImages = self.images[0]
        self.move(width)
    
    def left(self, width):
        if self.speed > -6:
            self.speed -= 1
        self.currentImages = self.images[0]
        self.move(width)
    
    def move(self, width):
        if 0 < self.x + self.speed and self.x + self.speed + self.width < width:
            self.x += self.speed
    
    def turn(self, newDirection):
        if self.direction != newDirection:
            self.direction = newDirection
            for index in range(len(self.images)):
                self.images[index] = [pygame.transform.flip(image, True, False) for image in self.images[index]]
    
    def coinCheck(self, tokens):
        for token in tokens:
            if token.checkCollect(self):
                tokens.remove(token)
                self.score += 1000
        return tokens

    def image(self):
        if self.air != 11:
            self.currentImages = self.images[2]
        self.currentImage += 1
        if self.currentImage >= len(self.currentImages):
            self.currentImage = 0
        return self.currentImages[self.currentImage]
