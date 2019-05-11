from mod_cell import *
import pygame
from matplotlib.pyplot import *



N = 8
h = 0.0005
sys = Systeme(N)
sys.initialiser()
pygame.init()
taille = 500
screen = pygame.display.set_mode([taille,taille])
echelle = taille*1.0/sys.L
clock = pygame.time.Clock()
done = False
ec = numpy.zeros(0)
iter = 5000
while not done and iter > 0:
    iter -= 1
    clock.tick(30)
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    sys.dessiner_disques(screen,echelle,(255,0,0))
    sys.euler(h)
    pygame.display.flip()
pygame.quit()