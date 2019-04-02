import math
import numpy
import random
import pygame
            
class Disque: #sphères se déplacent sur un plan donc assimilées à des disques
    def __init__(self,x,y,vx,vy):#contient coordonnées du centre, vitesse et accélération
        self.x = x
        self.y = y
        self.vx  = vx
        self.vy = vy
            
class Cellule:#liste de disques, chaque disque associé à un indice
    def __init__(self):
        self.ensemble_disques = set() #initialise une liste de disque
        self.decal_x = 0.0 #décalage lors de l'atteinte de limite
        self.decal_y = 0.0
    def ajouter(self,indice):
        self.ensemble_disques.add(indice) #on ajoute l'indice
    def enlever(self,indice):
        self.ensemble_disques.remove(indice)
             
class Grille:#tableau 2D de cellules Carré
    def __init__(self,Nbc,L):
        self.L = L #L: largeur de la grille 
        self.Nbc = Nbc #Nbc: Nombre de cellule
        self.tableau = []
        for i in range(self.Nbc):
            ligne = []
            for j in range(self.Nbc):
                ligne.append(Cellule())
            self.tableau.append(ligne) # Tableau de tableau de cellule
    def obtenir_cellule(self,i,j):#cette fonction renvoit la cellule comprise dans les bornes de la grille
            decal_x = 0.0
            decal_y = 0.0
            if i<0:
                i += self.Nbc
                decal_x = -self.L
            elif i>=self.Nbc:
                i -= self.Nbc
                decal_x = self.L
            if j<0:
                j += self.Nbc
                decal_y = -self.L
            elif j>=self.Nbc:
                j -= self.Nbc
                decal_y = self.L
            cellule = self.tableau[i][j]
            cellule.decal_x = decal_x
            cellule.decal_y = decal_y
            return cellule
             
class Systeme:
    def __init__(self,Nx,densite,rc,deltaR=0):
        self.Nx = Nx
        self.N = Nx*Nx
        self.densite = densite
        self.deltaR = deltaR
        self.rc = rc
        self.rc2 = rc*rc
        self.rv = rc+deltaR
        self.rv2 = self.rv*self.rv
        self.rayon = 0.5
        self.diam = self.rayon*2
        self.L = math.sqrt(math.pi/densite)*0.5*Nx
        self.aire = self.L*self.L
        self.demi_L = self.L*0.5
        self.Nc = int(self.L/self.rv)
        self.lc = self.L/self.Nc
        self.grille = Grille(self.Nc,self.L)
        self.liste_disques = []
        for d in range(self.N):
            self.liste_disques.append(Disque(0,0,0,0))
        self.energie = 0.0 
        self.viriel = 0.0
        self.Ecinetique = 0.0
        self.Epotentielle = 0.0
        self.pression = 0.0
        self.compteur = 0
        self.som_temp = 0
        self.som_pression = 0
        self.som_temp2 = 0
        self.som_pression2 = 0
             
    def init_disque(self,indice,x,y,vx,vy):
        disque = self.liste_disques[indice]
        disque.x = x
        disque.y = y
        disque.vx = vx
        disque.vy = vy
        i = int(x/self.lc)
        j = int(y/self.lc)
        cellule = self.grille.obtenir_cellule(i,j)
        cellule.ajouter(indice)
             
    def initialiser(self,vitesse):
        dx = self.L*1.0/(self.Nx)
        print("distance initiale = %f"%dx)
        if dx < self.diam:
            raise Exception("densite trop forte")
        else:
            dy = dx
            x = dx/2
            y = x
            px = 0.0
            py = 0.0
            for k in range(self.N):
                a = random.random()*math.pi*2.0
                vx = vitesse*math.cos(a)
                vy = vitesse*math.sin(a)
                px += vx
                py += vy
                self.init_disque(k,x,y,vx,vy)
                x += dx
                if x > self.L:
                    x = dx/2
                    y += dy
            for k in range(self.N):
                disque = self.liste_disques[k]
                disque.vx -= px/self.N
                disque.vy -= py/self.N 
        self.calculer_forces()
        self.construire_liste_voisins()
             
    def deplacer_disque(self,disque,indice,x1,y1):
        if x1<0:
            x1 += self.L
        elif x1>=self.L:
            x1 -= self.L
        if y1<0:
            y1 += self.L
        elif y1>=self.L:
            y1 -= self.L
        i = int(disque.x/self.lc)
        j = int(disque.y/self.lc)
        i1 = int(x1/self.lc)
        j1 = int(y1/self.lc)
        if i!=i1 or j!=j1:
            cellule = self.grille.obtenir_cellule(i,j)
            cellule.enlever(indice)
            cellule1 = self.grille.obtenir_cellule(i1,j1)
            cellule1.ajouter(indice)
        disque.x = x1
        disque.y = y1
           
    def construire_liste_voisins(self):
        self.liste_voisins = []
        self.deplac_max = 0.0
        for i in range(self.Nc):
            for j in range(self.Nc):
                cellule = self.grille.obtenir_cellule(i,j)
                for k in range(-1,2):
                    for l in range(-1,2):
                        cellule1 = self.grille.obtenir_cellule(i+k,j+l)
                        for indice in cellule.ensemble_disques:
                                for indice1 in cellule1.ensemble_disques:
                                    if indice1<indice:
                                        disque = self.liste_disques[indice]
                                        disque1 = self.liste_disques[indice1]
                                        dx = disque1.x+cellule1.decal_x-disque.x
                                        dy = disque1.y+cellule1.decal_y-disque.y
                                        r2 = dx*dx+dy*dy
                                        if r2<= self.rv2:
                                            self.liste_voisins.append([indice1,indice])
           
    def calculer_forces(self):
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.ax = 0.0
            disque.ay = 0.0
        self.Epotentielle = 0.0
        self.viriel = 0.0
        for i in range(self.Nc):
            for j in range(self.Nc):
                cellule = self.grille.obtenir_cellule(i,j)
                for k in range(-1,2):
                    for l in range(-1,2):
                        cellule1 = self.grille.obtenir_cellule(i+k,j+l)
                        for indice in cellule.ensemble_disques:
                                for indice1 in cellule1.ensemble_disques:
                                    if indice1<indice:
                                        disque = self.liste_disques[indice]
                                        disque1 = self.liste_disques[indice1]
                                        dx = disque1.x+cellule1.decal_x-disque.x
                                        dy = disque1.y+cellule1.decal_y-disque.y
                                        r2 = dx*dx+dy*dy
                                        if r2 < self.rc2:
                                            ir2 = 1.0/r2
                                            ir6 = ir2*ir2*ir2
                                            v = 24.0*ir6*(ir6-0.5)
                                            f = 2.0*v*ir2
                                            fx = f*dx
                                            fy = f*dy
                                            disque1.ax += fx
                                            disque1.ay += fy
                                            disque.ax -= fx
                                            disque.ay -= fy
                                            self.Epotentielle += 4.0*ir6*(ir6-1.0)
                                            self.viriel += v

            
    def calculer_forces_avec_liste_voisins(self):
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.ax = 0.0
            disque.ay = 0.0
        self.Epotentielle = 0.0
        self.viriel = 0.0
        for paire in self.liste_voisins:
            disque = self.liste_disques[paire[0]]
            disque1 = self.liste_disques[paire[1]]
            dx = disque1.x-disque.x
            dy = disque1.y-disque.y
            if dx >= self.demi_L:
                dx -= self.L
            elif dx < -self.demi_L:
                dx += self.L
            if dy >= self.demi_L:
                dy -= self.L
            elif dy < -self.demi_L:
                dy += self.L
            r2 = dx*dx+dy*dy
            if r2 < self.rc2:
                ir2 = 1.0/r2
                ir6 = ir2*ir2*ir2
                v = 24.0*ir6*(ir6-0.5)
                f = 2.0*v*ir2
                fx = f*dx
                fy = f*dy
                disque1.ax += fx
                disque1.ay += fy
                disque.ax -= fx
                disque.ay -= fy
                self.Epotentielle += 4.0*ir6*(ir6-1.0)
                self.viriel += v

            
    def calculer_cinetique(self):
        self.Ecinetique = 0.0
        for k in range(self.N):
            disque = self.liste_disques[k]
            self.Ecinetique += 0.5*(disque.vx*disque.vx+disque.vy*disque.vy)
        self.pression = (self.Ecinetique+self.viriel)/self.aire
        self.Ecinetique /= self.N
        self.energie = self.Ecinetique+self.Epotentielle/self.N
        self.som_temp += self.Ecinetique
        self.som_temp2 += self.Ecinetique*self.Ecinetique
        self.som_pression += self.pression
        self.som_pression2 += self.pression*self.pression
        self.compteur += 1
             
    def init_moyennes(self):
        self.compteur = 0
        self.som_temp = 0.0
        self.som_pression = 0.0
        self.som_temp2 = 0.0
        self.som_pression2 = 0.0
             
    def temperature_moyenne(self):
        Tm = self.som_temp/self.compteur
        dTm = math.sqrt(self.som_temp2/self.compteur-Tm*Tm)
        return (Tm,dTm)
    def pression_moyenne(self):
        Pm = self.som_pression/self.compteur
        dPm = math.sqrt(self.som_pression2/self.compteur-Pm*Pm)
        return (Pm,dPm)
             
    def ajuster_vitesses(self,T):
        Tm = self.som_temp/self.compteur
        fac = math.sqrt(T/Tm)
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.vx *= fac
            disque.vy *= fac
             
    def verlet(self,h,hd2):
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.vx += hd2*disque.ax
            disque.vy += hd2*disque.ay
            self.deplacer_disque(disque,k,disque.x+h*disque.vx,disque.y+h*disque.vy)
        self.calculer_forces()
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.vx += hd2*disque.ax
            disque.vy += hd2*disque.ay
            
    def verlet_avec_liste_voisins(self,h,hd2):
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.vx += hd2*disque.ax
            disque.vy += hd2*disque.ay
            self.deplacer_disque(disque,k,disque.x+h*disque.vx,disque.y+h*disque.vy)
        self.calculer_forces_avec_liste_voisins()
        v2max = 0.0
        for k in range(self.N):
            disque = self.liste_disques[k]
            disque.vx += hd2*disque.ax
            disque.vy += hd2*disque.ay
            v2 = disque.vx*disque.vx+disque.vy*disque.vy
            if v2 > v2max:
                v2max = v2
        self.deplac_max += math.sqrt(v2max)*h
        if self.deplac_max*2.0 > self.deltaR:
            self.construire_liste_voisins()
            self.deplac_max = 0.0
            
    def integration(self,h,n):
        hd2 = h/2
        for i in range(n):
            self.verlet(h,hd2)
    def integration_avec_liste_voisins(self,h,n):
        hd2 = h/2
        for i in range(n):
            self.verlet_avec_liste_voisins(h,hd2)
            
    def dessiner_disques(self,screen,echelle,couleur):
        for k in range(self.N):
            disque = self.liste_disques[k]
            pygame.draw.ellipse(screen,couleur,[(disque.x-self.rayon)*echelle,(disque.y-self.rayon)*echelle,self.rayon*2*echelle,self.rayon*2*echelle],2)
            
