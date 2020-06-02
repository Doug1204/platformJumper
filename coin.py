
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.currentImage = 0

    def checkCollect(self, man):
        xCheck = self.x < man.x <= self.x + self.width or self.x < man.x + man.width <= self.x + self.width or (man.x < self.x and man.x + man.width > self.x + self.width)
        manY = man.currentPlatform.y + man.jumpAddition - man.height
        yCheck = self.y < manY < self.y + self.height or self.y < manY + man.height < self.y + self.height or (manY < self.y and manY + man.height > self.y + self.height)
        return xCheck and yCheck
    
    def animate(self):
        self.currentImage += 1
        if self.currentImage > 29:
            self.currentImage = 0
        self.y += 1 if self.currentImage > 14 else -1
        