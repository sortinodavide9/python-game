import pygame,sys
from pygame import *
from player import Player #Classi
#FINESTRA:
pygame.init()
pygame.font.init()
WINDOW_SIZE = (600,600)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
clock = pygame.time.Clock()#timer FPS
#IMMAGINI:
projectileImage = pygame.image.load("images/arrow.png")
backgroundImage = pygame.image.load("images/bg.jpg")
backgroundImage = pygame.transform.scale(backgroundImage,WINDOW_SIZE)
playerAnimationRight = [pygame.image.load("images/R1.png"),pygame.image.load("images/R2.png"),pygame.image.load("images/R3.png"),pygame.image.load("images/R4.png")]
playerAnimationLeft = [pygame.image.load("images/L1.png"),pygame.image.load("images/L2.png"),pygame.image.load("images/L3.png"),pygame.image.load("images/L4.png")]
playerStandingImage = pygame.image.load("images/standing.png")
projectileDirection = ""
#Variabili:
scroll = [0, 0]
def init():
    global player,projectileList,solidObjects,platformWidth,startingJumpY
    #Variabili:
    player = Player()#Oggetto player
    projectileList = []
    #Oggetti solidi:
    solidObjects = []
    solidObjects.append(pygame.Rect(0,333,400,33))#Piattaforma
    solidObjects.append(pygame.Rect(0,133,300,33))#Piattaforma
    solidObjects.append(pygame.Rect(0,533,300,33))#Piattaforma
    solidObjects.append(pygame.Rect(1144,111,300,33))#Piattaforma
    #Variabili 
    startingJumpY = 0#y dove viene riportato il player quando sbatte
    platformWidth = 600
def pollEvents():
    global projectileList, projectileDirection,startingJumpY
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_SPACE:
                startingJumpY = player.rect.y
                
                player.isJumping = True
                
            elif event.key == 97:#lettera a -> aggiunge proiettile alla lista
                
                if len(projectileList) < 1:
                    projectileList.append([pygame.Rect(player.rect.x+9,player.rect.y+9,playerAnimationRight[0].get_width(),playerAnimationRight[0].get_height()), projectileDirection])
            elif(event.key == 114):#lettera r 
                init()

            elif event.key == K_RIGHT:
                projectileDirection = "right"
                player.directionRight = True
            elif event.key == K_LEFT:
                projectileDirection = "left"
                player.directionLeft= True
                
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.directionRight = False
                
            elif event.key == K_LEFT:
                player.directionLeft = False
                
def update():
    global startingJumpY, platformWidth, scroll
    if(player.directionRight or player.directionLeft): #movimento player
        if(player.directionRight):
            player.rect.x += 5
        elif(player.directionLeft):
            player.rect.x -= 5
        #update animation player
        player.animationFrame += 0.1 
        if(player.animationFrame >= 4):
            player.animationFrame = 0
    count = 0#iteratore di projectileList
    #Jump del player:
    if (player.isJumping):
        player.rect.y -= player.vel_y*2
        player.vel_y -= 1
        
        if player.vel_y < -15:
            player.isJumping = False
            player.vel_y = 15
            
    #Collisioni (todo):

    #Camera movement:
    scroll[0] += (player.rect.x - scroll[0] - 300) / 20
    scroll[1] += (player.rect.y - scroll[1] - 430) / 10

            

def draw():
    global scroll
    
    #Draw player:
    if(player.directionRight):#disegno se il player si sta muovendo verso destra
        screen.blit(playerAnimationRight[int(player.animationFrame)],(player.rect.x - scroll[0], player.rect.y - scroll[1]))
    elif(player.directionLeft):#disegno se il player si sta muovendo verso sinistra
        screen.blit(playerAnimationLeft[int(player.animationFrame)],(player.rect.x - scroll[0],player.rect.y - scroll[1]))
    if(not player.directionRight and not player.directionLeft):#disegno player da fermo
        screen.blit(playerStandingImage,(player.rect.x - scroll[0],player.rect.y - scroll[1]))
    
    #Draw solidObjects:
    for solidObject in solidObjects:
        pygame.draw.rect(screen,(255,0,0),(solidObject.x - scroll[0], solidObject.y - scroll[1], solidObject.w, solidObject.h))
    #Draw texts:
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render('Premi R per ricaricare, A per sparare', False, (0,0,0))
    screen.blit(textsurface,(233,0))
    
    pygame.display.update()
    clock.tick(60)

    