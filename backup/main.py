from game import pollEvents,update,draw,init #import funzioni di game
from game import screen,backgroundImage#import variabili di game

init()
while True:
    screen.blit(backgroundImage,(0,0))
    pollEvents() 
    update()
    draw()  