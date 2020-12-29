import pygame
class Player():
    def __init__(self):
        self.rect = pygame.Rect(333,600-62,30,62)
        self.directionRight = False
        self.directionLeft = False
        self.animationFrame = 0
        self.isJumping = False
        self.vel_y = 10