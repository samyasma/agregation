from modcell2D import *
import pygame
from matplotlib.pyplot import *
import time

##############################################AFFICHAGE############################################################

Nx = 20
densite = 0.3
rc = 2.5
h = 0.01
sys = Systeme(Nx,densite,rc)
sys.initialiser(1.0)
pygame.init()
taille = 500
screen = pygame.display.set_mode([taille,taille])
echelle = taille*1.0/sys.L
clock = pygame.time.Clock()
done = False
pression = numpy.zeros(0)
ec = numpy.zeros(0)
energie = numpy.zeros(0)
iter = 5000
t = time.clock()
while not done and iter > 0:
    iter -= 1
    clock.tick(30)
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    sys.dessiner_disques(screen,echelle,(255,0,0))
    sys.integration(h,10)
    sys.calculer_cinetique()
    pression = numpy.append(pression,sys.pression)
    ec = numpy.append(ec,sys.Ecinetique)
    energie = numpy.append(energie,sys.energie)
    pygame.display.flip()
print(time.clock()-t)
#pygame.image.save(screen,"boule_jaune.png")
pygame.quit()