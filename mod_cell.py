
import math
import numpy
import random
import pygame
from pylab import sqrt,dist,vdot,dot,floor,array,randn,sqrt,log

D=0
            
class Disque:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.new_pos=numpy.array([0,0])
            
class Case: 
    def __init__(self):
        self.ensemble_disques = set()
        self.decal_x = 0.0
        self.decal_y = 0.0
    def ajouter(self,indice):
        self.ensemble_disques.add(indice)
    def enlever(self,indice):
        self.ensemble_disques.remove(indice)
             
class Grille:
    def __init__(self,Nc,L):
        self.L = L #longueur de la fenetre
        self.Nc = Nc #nombre de case
        self.tableau = []
        for i in range(self.Nc):
            ligne = []
            for j in range(self.Nc):
                ligne.append(Case())
            self.tableau.append(ligne)
    def obtenir_case(self,i,j):
            decal_x = 0.0
            decal_y = 0.0
            if i<0:
                i += self.Nc
                decal_x = -self.L
            elif i>=self.Nc:
                i -= self.Nc
                decal_x = self.L
            if j<0:
                j += self.Nc
                decal_y = -self.L
            elif j>=self.Nc:
                j -= self.Nc
                decal_y = self.L
            case = self.tableau[i][j]
            case.decal_x = decal_x
            case.decal_y = decal_y
            return case
             
class Systeme:
    def __init__(self,Nx):
        self.Nx = Nx #Nombre de sphères par ligne
        self.N = Nx*Nx #nombre de sphères total
        self.rayon = 0.5 #rayon d'une sphère
        self.diam = self.rayon*2
        self.diam2 = self.diam**2
        self.L = 3*Nx  #largeur de la grille
        self.aire = self.L*self.L
        self.demi_L = self.L*0.5
        self.Nc = int(self.L/self.diam) #nbr de au total
        self.lc = self.L/self.Nc #largeurd'une case
        self.grille = Grille(self.Nc,self.L)
        self.liste_disques = []
        for d in range(self.N):
            self.liste_disques.append(Disque(0,0))
        self.energie = 0.0
        self.viriel = 0.0

            
    def init_disque(self,indice,x,y):
        disque = self.liste_disques[indice]
        disque.x = x
        disque.y = y
        i = int(x/self.lc) #
        j = int(y/self.lc) #
        case = self.grille.obtenir_case(i,j) #obtenir la case
        case.ajouter(indice) #ajouter l'indice de la

            
    def initialiser(self):
        dx = self.L/self.Nx #distance entre 
        print("distance initiale = %f"%dx)
        if dx < self.diam:
            raise Exception("Rayon trop grand")
        else:
            dy = dx
            x = dx/2
            y = x
            for k in range(self.N):
                self.init_disque(k,x,y)
                x += dx
                if x > self.L:
                    x = dx/2
                    y += dy
        self.calculer_forces()
           
    def deplacer_disque(self,disque,indice,x1,y1):
        if x1<0:
            x1 += self.L
        elif x1>=self.L:
            x1 -= self.L
        if y1<0:
            y1 += self.L
        elif y1>=self.L:
            y1 -= self.L

        """i = int(disque.x/self.lc)
        j = int(disque.y/self.lc)
        i1 = int(x1/self.lc)
        j1 = int(y1/self.lc)
       	if i!=i1 or j!=j1:
            case = self.grille.obtenir_case(i,j)
            case.enlever(indice)
            case1 = self.grille.obtenir_case(i1,j1)
            case1.ajouter(indice)"""
        disque.x = x1
        disque.y = y1


    def distance(self,a,b):
    	return sqrt((a**2)+(b**2))

    def derivee_lennard_jones_pot(self,r):
        return r-2*self.rayon

    def calculer_forces(self):
        for k in range(self.N):
            disque = self.liste_disques[k]
            nextPosition=numpy.array([0,0])
            for j in range(self.N):
            	disque1= self.liste_disques[j]
            	dx = disque1.x-disque.x
            	dy = disque1.y-disque.y
            	distance= self.distance(dx,dy)
            	if distance !=0 and distance < 12*self.rayon:
            		nextPosition=nextPosition + (self.derivee_lennard_jones_pot(distance)/distance)*numpy.array([float(dx),float(dy)])

            
            self.liste_disques[k].new_pos=nextPosition
            	
        """for i in range(self.Nc):
            for j in range(self.Nc):
                case = self.grille.obtenir_case(i,j)
                for k in range(-1,2):
                    for l in range(-1,2):
                    	if k==0 and l==0:
                    		pass
                    	else:
	                        case1 = self.grille.obtenir_case(i+k,j+l)
	                        nextPosition=numpy.array([0,0])
	                        for indice in case.ensemble_disques:
	                            for indice1 in case1.ensemble_disques:
	                                if indice1 != indice:
	        disque = self.liste_disques[indice]
	        disque1 = self.liste_disques[indice1]
	        dx = disque1.x+case1.decal_x-disque.x
	        dy = disque1.y+case1.decal_y-disque.y
	        distance= self.distance(dx,dy)
	        if distance >0 :
	            nextPosition=nextPosition + (self.derivee_lennard_jones_pot(distance)/distance)*numpy.array([float(dx),float(dy)])"""

        


             
    def euler(self,h):
        self.calculer_forces()
        for k in range(self.N):
        	vect_aléatoire=randn(2)
        	bruit=sqrt(2*D*h)*randn(2)
        	disque = self.liste_disques[k]
        	self.deplacer_disque(disque,k,disque.x+h*disque.new_pos[0]+bruit[0],disque.y+h*disque.new_pos[1]+bruit[1])
        

    """def verlet(self,h):
    	hd2=h/2
    	for k in range(self.N):
        	disque = self.liste_disques[k]
        	disque.vx -= hd2*disque.new_pos[0]
        	disque.vy -= hd2*disque.new_pos[1]
        	self.deplacer_disque(disque,k,disque.x+h*disque.vx,disque.y+h*disque.vy)
    	self.calculer_forces()
    	for k in range(self.N):
        	disque = self.liste_disques[k]
        	disque.vx += hd2*disque.new_pos[0]
        	disque.vy += hd2*disque.new_pos[1]"""
             
    def dessiner_disques(self,screen,echelle,couleur):
        for k in range(self.N):
            disque = self.liste_disques[k]
            pygame.draw.ellipse(screen,couleur,[(disque.x-self.rayon)*echelle,(disque.y-self.rayon)*echelle,self.rayon*2*echelle,self.rayon*2*echelle],2)
  
             