from game import screen, playerRect,pygame,WINDOW_SIZE
from game import projectileList
import random
#VARIABILI:
enemyAnimationLeft = [pygame.image.load("images/L1E.png"),pygame.image.load("images/L2E.png"),pygame.image.load("images/L3E.png"),pygame.image.load("images/L4E.png"),pygame.image.load("images/L5E.png"),pygame.image.load("images/L6E.png"),pygame.image.load("images/L7E.png"),pygame.image.load("images/L8E.png"),pygame.image.load("images/L11E.png")]
enemyAnimationRight = [pygame.image.load("images/R1E.png"),pygame.image.load("images/R2E.png"),pygame.image.load("images/R3E.png"),pygame.image.load("images/R4E.png"),pygame.image.load("images/R5E.png"),pygame.image.load("images/R6E.png"),pygame.image.load("images/R7E.png"),pygame.image.load("images/R8E.png"),pygame.image.load("images/R11E.png")]
enemyList = []#enemy rect, verso del nemico
counter = 0#counter animazione enemy
spawnEnemy = 0
particles = []
def enemies():
    global counter,playerAnimation,spawnEnemy
    spawnEnemy += 0.1
    if(spawnEnemy >= 10):#spawn
        enemyList.append([pygame.Rect(random.randint(0,WINDOW_SIZE[0]),WINDOW_SIZE[1]-55,3,3),playerAnimation[2]])
        spawnEnemy = 0
    temp = 0
    for enemy in enemyList:
        #CHANGE POSITIONS:
        if(enemy[0].x < playerRect.x):#se il nemico è piu indietro del player
            enemy[0].x += 2
            enemy[1] = "right"
        elif(enemy[0].x > playerRect.x):#se il nemico è piu avanti del player
            enemy[0].x -= 2
            enemy[1] = "left"
        #ENEMY PARTICLES:
        if(len(projectileList) > 0  and enemy[0].colliderect(projectileList[0][0])):
            for i in range(19): 
                particles.append([[enemy[0].x, enemy[0].y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
        if(len(enemyList) > 1):
            enemyParticles()
        else:
                particles.clear()
        #ENEMY COLLISIONS:
        if(len(projectileList) > 0):
            if(enemy[0].colliderect(projectileList[0][0])):
                del enemyList[temp]
                del projectileList[0]
        
        #ENEMY ANIMATIONS:
        counter += 0.05
        if(counter >=8):
            counter = 0
        if(enemy[1] == "left"):
            screen.blit(enemyAnimationLeft[int(counter)],(enemy[0].x,enemy[0].y))
        elif(enemy[1] == "right"):
            screen.blit(enemyAnimationRight[int(counter)],(enemy[0].x,enemy[0].y))
        temp += 1
def enemyParticles():
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.1
        pygame.draw.circle(screen, (255, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)