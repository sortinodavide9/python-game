import pygame
right = "images/animals/right.png"
left = "images/animals/left.png"
class Animal():
    def __init__(self,player):
        self.rect = pygame.Rect(player.rect.x+1200,750,30,62)
        self.image = pygame.image.load(right)
        self.animationFrame = 0
        self.timerDestruction = 0
    def updateAnimation(self):
        if( self.animationFrame == 0):
            self.image = pygame.image.load(left)
            self.animationFrame = 1   
        else:
            self.animationFrame = 0
            self.image = pygame.image.load(right)

        
        
        