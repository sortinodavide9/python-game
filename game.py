import pygame, sys, random, noise
from pygame import *
from player import Player #Classi
from animals import Animal #Classi
#FINESTRA:
pygame.init()
pygame.font.init()
WINDOW_SIZE = (1200,600)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
clock = pygame.time.Clock()#timer FPS
#IMMAGINI:
backgroundImage = pygame.image.load("images/bg.jpg")
backgroundImage = pygame.transform.scale(backgroundImage,WINDOW_SIZE)
playerAnimationRight = [pygame.image.load("images/R1.png"),pygame.image.load("images/R2.png"),pygame.image.load("images/R3.png"),pygame.image.load("images/R4.png")]
playerAnimationLeft = [pygame.image.load("images/L1.png"),pygame.image.load("images/L2.png"),pygame.image.load("images/L3.png"),pygame.image.load("images/L4.png")]
playerStandingImage = pygame.image.load("images/standing.png")
projectileDirection = ""
animalsList = []
#IMMAGINI BLOCCHI:
dirtImage = pygame.image.load("images/blocks/dirt.png")
grassImage = pygame.image.load("images/blocks/grass.png")
plantImage = pygame.image.load("images/blocks/plant.png").convert()
plantImage.set_colorkey((255,255,255))

#Variabili:
scroll = [0, 0]#camera
CHUNK_SIZE = 8
game_map = {}
tile_index = {1:grassImage,
              2:dirtImage,
              3:plantImage
              }
tileRects = []
def init():
    global player,projectileList,solidObjects,platformWidth
    #Variabili:
    player = Player()#Oggetto player
    projectileList = []
    #Oggetti solidi:
    solidObjects = []
    solidObjects.append(pygame.Rect(0,590,600,33))#base
    solidObjects.append(pygame.Rect(222,555,600,33))#base
    solidObjects.append(pygame.Rect(422,485,60,63))#base
    solidObjects.append(pygame.Rect(483,485,60,63))#base
    #altre piattaforme:
    xx = 0
    cou = 1
    for n in range(10):
        if(xx == 0):
            solidObjects.append(pygame.Rect(0,590-(cou*140),100,33))#base
            cou += 1
            xx = 1
        else:
            solidObjects.append(pygame.Rect(200,590-(cou*130),100,33))#base
            cou += 1
            xx = 0
    #Animali:
    
def pollEvents():
    global projectileList, projectileDirection
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_SPACE:
               
                player.isJumping = True
                
            elif event.key == 97:#lettera a -> aggiunge proiettile alla lista
                
                if len(projectileList) < 1:
                    projectileList.append([pygame.Rect(player.rect.x+9,player.rect.y+9,playerAnimationRight[0].get_width(),playerAnimationRight[0].get_height()), projectileDirection])
            elif(event.key == 114):#lettera r 
                init()

            elif event.key == K_RIGHT:
                player.directionRight = True
            elif event.key == K_LEFT:
                player.directionLeft= True
                
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.directionRight = False
                
            elif event.key == K_LEFT:
                player.directionLeft = False
                
def update():
    global platformWidth, scroll
    #movimento player:
    if(player.directionRight or player.directionLeft): #movimento player
        if(player.directionRight):
            player.rect.x += 8
        elif(player.directionLeft):
            player.rect.x -= 8
    #Update animazione player:
        player.animationFrame += 0.1 
        if(player.animationFrame >= 4):
            player.animationFrame = 0
    #Jump del player:
    if (player.isJumping):
        player.rect.y -= player.vel_y*2
        player.vel_y -= 1 
        if player.vel_y < -11:
            player.isJumping = False
            player.vel_y = 11
    #Collisioni Player:    
    collisions = collisionsTest()
    if(len(collisions) == 0 and not player.isJumping):#caduta del player se non tocca nulla
        player.rect.y += 20#velocità caduta player
    for rect in collisions:
        if player.rect.right >=  rect.left and player.rect.right < rect.left + 10:#player a destra dell' oggetto
            player.rect.right = rect.left -3
            continue;
        elif player.rect.left <  rect.right  and player.rect.left > rect.right -10:#player a sinistra dell'oggetto
            player.rect.left = rect.right +3
            continue;
        if player.rect.top <= rect.bottom and player.rect.top >= rect.bottom - 44:#player sotto oggetto
            if(player.isJumping):
                player.rect.top = rect.bottom +3
                player.vel_y = 0
            else:
                player.rect.top = rect.bottom +3    
        elif player.rect.bottom >= rect.top and player.rect.bottom <= rect.top + 44:#player sopra oggetto
            player.rect.bottom = rect.top + 1 
    #collisioni tra player e blocchi
    playerBlockCollisions = playerBlockCollisionsTest()
    for blockRect in playerBlockCollisions:
        player.rect.bottom = blockRect.top
 

    #Camera:
    scroll[0] += (player.rect.x - scroll[0] - 300) / 20
    scroll[1] += (player.rect.y - scroll[1] - 430) / 10
       
    #Collisioni tra Animali e blocchi:
    animalBlockCollisions = animalBlockCollisionsTest()
    for collision in animalBlockCollisions:
        collision[1].bottom = collision[0].top
        #animalRect -----------blockRect
    #Collisioni Player animali:
    playerAnimalCollision = playerAnimalCollisionsTest()
    for collision in playerAnimalCollision:
        print("bu")
    #Spawn animali:
    if( random.randint(1,100) == 80 and len(animalsList) < 4):
        cow = Animal(player)
        animalsList.append(cow)
    #Update animazioni animali:
    if( random.randint(1,111) == 3 and len(animalsList) > 0):
        for animal in animalsList:
            animal.updateAnimation()
    #distruzione animale:
    if(len(animalsList) > 0):
        count = 0
        for animal in animalsList:
            animal.timerDestruction += 0.1
            if(animal.timerDestruction > 111):
                del animal
                animalsList.pop(count)
            count += 1

                    
def draw():
    global scroll,CHUNK_SIZE,game_map,tile_index
    #Draw player:
    if(player.directionRight):#disegno se il player si sta muovendo verso destra
        screen.blit(playerAnimationRight[int(player.animationFrame)],(player.rect.x - scroll[0], player.rect.y - scroll[1]))
    elif(player.directionLeft):#disegno se il player si sta muovendo verso sinistra
        screen.blit(playerAnimationLeft[int(player.animationFrame)],(player.rect.x - scroll[0]-20,player.rect.y - scroll[1]))
    if(not player.directionRight and not player.directionLeft):#disegno player da fermo
        screen.blit(playerStandingImage,(player.rect.x - scroll[0]-17,player.rect.y - scroll[1]))
        pygame.draw.rect(screen,(255,0,0),(player.rect.x - scroll[0],player.rect.y - scroll[1],player.rect.w,player.rect.h))
    #Draw solidObjects:
    for solidObject in solidObjects:
        pygame.draw.rect(screen,(255,0,0),(solidObject.x - scroll[0], solidObject.y - scroll[1], solidObject.w, solidObject.h))
    #Draw texts:
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render('Premi R per ricaricare  '+ str(int(clock.get_fps())), False, (0,0,0))
    screen.blit(textsurface,(233,0))
    #Draw map:
    tileRects.clear()
    for y in range(4):
        for x in range(5):
            targetX = x -1 + int(scroll[0] / (CHUNK_SIZE * 64))
            targetY = y -1 + int(scroll[1] / (CHUNK_SIZE * 64))
            targetChunk = str(targetX) + ";" + str(targetY)
            if targetChunk not in game_map:
                game_map[targetChunk] = generate_chunk(targetX, targetY)
            for tile in game_map[targetChunk]:
                screen.blit(tile_index[tile[1]],(tile[0][0]*64-scroll[0],tile[0][1]*64-scroll[1]))                 
                if tile[1] in [1]:
                    tileRects.append(pygame.Rect(tile[0][0]*64,tile[0][1]*64,64,64))    
                  
    #Draw Animals:
    for animal in animalsList:
        screen.blit(animal.image,(animal.rect.x-scroll[0],animal.rect.y-scroll[1]))                    
   
    

    #Refresh:
    pygame.display.update()
    clock.tick(60)
    
def collisionsTest():
    global player, solidObjects
    collisions = []
    for solidObject in solidObjects:
        if(player.rect.colliderect(solidObject)):
            collisions.append(solidObject)  
    return collisions

 
def playerBlockCollisionsTest():
    global player
    collisions = [] 
    for tile in tileRects:
        if(player.rect.colliderect(tile)):  
            collisions.append(tile)

    return collisions

def animalBlockCollisionsTest():
    collisions = []
    for tile in tileRects:
        for animal in animalsList:
            if tile.colliderect(animal):
                collisions.append([tile, animal.rect])
    return collisions
def playerAnimalCollisionsTest():
    collisions = []
    for animal in animalsList:
        if animal.rect.colliderect(player.rect):
                collisions.append(animal)
    return collisions
def generate_chunk(x,y):
    global CHUNK_SIZE
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999)*5)
            if target_y > 2 - height:
                tile_type = 2 # dirt
            elif target_y == 2 - height:
                tile_type = 1 # grass
            elif target_y == 2 - height - 1:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant
            if tile_type != 0:
                chunk_data.append([[target_x,target_y+10],tile_type])
    return chunk_data