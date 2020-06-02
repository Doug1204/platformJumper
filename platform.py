import random
import os
import pygame

class Platform:
    def __init__(self, previousPlatform, width, height, manScore):

        self.height = height // 12
        self.width = width // 24

        jumpFormula = {50000:40, 40000:35, 25000:30, 15000:25}
        for num in jumpFormula.keys():
            if manScore >= num:
                self.chosenHeight = jumpFormula[num]
                previousPlatform.chosenHeight = jumpFormula[num]
                break
        else:
            self.chosenHeight = 20
        

        if previousPlatform:
            change = [int((-(self.chosenHeight / 100) * i ** 2 + self.chosenHeight) * -10) + previousPlatform.y for i in range(1, 5)]
            self.y = random.choice(change)
            self.air = change.index(self.y)
        else:
            self.y = height // 10 * 6 - self.height
            self.air = 11
        
        option = random.randint(0, 3)
        if not previousPlatform:
            self.x = {(0, width):(4, 1, 3)}
        elif option == 0:
            self.x = {(0, width // 3):(4, 1, 2), ((width // 3) * 2, width):(0, 1, 3)}
        elif option == 1:
            self.x = {(width // 3, (width // 3) * 2):(5, 6, 7)}
        elif option == 2:
            self.x = {(0, width // 2):(4, 1, 2)}
        elif option == 3:
            self.x = {(width // 2, width):(0, 1, 3)}

