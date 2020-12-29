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
scroll = [0, 0]#camera
def init():
    global player,projectileList,solidObjects,platformWidth,startingJumpY
    #Variabili:
    player = Player()#Oggetto player
    projectileList = []
    #Oggetti solidi:
    solidObjects = []
    
    solidObjects.append(pygame.Rect(0,590,600,33))#base
    solidObjects.append(pygame.Rect(-110,500,60,33))#piattaforma1
    solidObjects.append(pygame.Rect(0,360,60,33))#piattaforma1
    
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
    #movimento player:
    if(player.directionRight or player.directionLeft): #movimento player
        if(player.directionRight):
            player.rect.x += 5
        elif(player.directionLeft):
            player.rect.x -= 5
    #Update animazione player:
        player.animationFrame += 0.1 
        if(player.animationFrame >= 4):
            player.animationFrame = 0
    #Jump del player:
    if (player.isJumping):
        player.rect.y -= player.vel_y*2
        player.vel_y -= 1 
        if player.vel_y < -15:
            player.isJumping = False
            player.vel_y = 15
   
    #Collisioni (todo):
    collisions = collisionsTest()
    
    for rect in collisions:
        if player.rect.right >=  rect.left and player.rect.right < rect.left +10:
            print("sinistra")
            player.rect.right = rect.left -3
            continue;
        elif player.rect.left <  rect.right  and player.rect.left > rect.right -10:
            print("destra")
            player.rect.left = rect.right +3
            continue;
        if player.rect.top <= rect.bottom and player.rect.top >= rect.bottom - 44: #player sotto oggetto
            player.rect.top = rect.bottom +3
            print("sotto")
        elif player.rect.bottom >= rect.top and player.rect.bottom <= rect.top + 44: #player sopra oggetto
            player.rect.bottom = rect.top - 3
            print("sopra,","playery->",player.rect.y," rectY->",rect.centery)
            
       
    #Camera:
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
        screen.blit(playerStandingImage,(player.rect.x - scroll[0]-17,player.rect.y - scroll[1]))
        pygame.draw.rect(screen,(255,0,0),(player.rect.x - scroll[0],player.rect.y - scroll[1],player.rect.w,player.rect.h))
    #Draw solidObjects:
    for solidObject in solidObjects:
        pygame.draw.rect(screen,(255,0,0),(solidObject.x - scroll[0], solidObject.y - scroll[1], solidObject.w, solidObject.h))
    #Draw texts:
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render('Premi R per ricaricare', False, (0,0,0))
    screen.blit(textsurface,(233,0))
    
    pygame.display.update()
    clock.tick(60)

def collisionsTest():
    global player, solidObjects
    collisions = []
    for solidObject in solidObjects:
        if(player.rect.colliderect(solidObject)):
            collisions.append(solidObject)
    return collisions