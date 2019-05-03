# -*- coding: utf-8 -*-
#
# Fichier : cellule.py
# Date : février 2019 
# Auteurs : Dang-Vu Laurent
# 
# Contient le squelette de la classe grille qui modélise une grille et le squelette de la classe Boule
# qui modélise des cellules
#
#===========================================


############# Quelques modules utiles #############

import pygame
from pylab import sqrt,dist,vdot,dot,floor,array,randn
from sympy import var,diff,integrate,sqrt,log

############# Quelques constantes utiles #############

# taille de la fenêtre d'affichage pour pyGame
LARGEUR = 370
LONGUEUR = 600

RAYON = 17	# rayon des boules, en pixel
RAYON_A = 4*RAYON # rayon d'attraction des cellules
DELTA_T = 0.35	# intervalle de temps entre deux rafraîchissement de la position
DELTA_X = 125 #Yboite : longueur d'une boite
DELTA_Y = 200 #Xboite : largeur d'une boite
EPSILON = 0.09	# constante en dessous de laquelle la vitesse devient nulle
N_X = int(LARGEUR/DELTA_X) #nombre de boites "en horizontal"
N_Y = int(LONGUEUR/DELTA_Y) #nombre de boites "en vertical"
X_MIN = 0
Y_MIN = 0
X_MAX = LARGEUR
Y_MAX = LONGUEUR

# largeur des bandes
BORD = 25

#Autres fonctions
var('r')

# def f_indicatrice_rayonA(x):
# 	print(x)
# 	print("ind")
# 	if(x <= 300.0):
# 		return(1)
# 	else:
# 		return(0)

def derivee_lennard_jones_pot(r):#derivee du potentiel de Lennard-Jones
	derlennardJones = 100000000*((384*(RAYON**6)/r**13)+(6/r**7)) #*f_indicatrice_rayonA(r)
	return(derlennardJones)

	
############# Classe Grille #############
class Grille:
	""" Classe qui definit une grille numerique.
	Une grille sera definie par :
		- un tableau des boites par lesquelles elle divise l'espace
	"""	

	def __init__(self,L_boules):
		""" Constructeur d'une Grille.
		Paramètres :
			L_boules : liste contenant les cellules, qu'on doit caser chacune dans une boite de l'espace
		"""
		# print("construction grille")
		# boite
		self.grille = []
		
		#on cree une grille vide de dimensions DELTA_X*DELTA_Y
		for k in range(N_X):
			for j in range(N_Y):
				self.grille.append([])
		# print("grille vide")
		
		#on place chaque cellule dans la bonne boite : celle qui la contient
		# print(L_boules)
		for elt in L_boules:
			# print(str(elt))
			Xi_x,Xi_y = elt.x,elt.y
			ix = int(floor((Xi_x-X_MIN)/DELTA_X))+1
			iy = int(floor((Xi_y-Y_MIN)/DELTA_Y))+1
			# print(ix,iy)
			k = ix + (iy-1)*N_X  #on calcule k, le numero de la boite qui la contient
			# print(k)
			self.grille[k-1].append(elt) #on ajoute la cellule ds la bonne boite, k-1 car on commence a 0 (pas 1)
			
		
	def __str__(self):
		""" Renvoie un tableau de boites (contenant les positions des cellules dans leur sein) qui représente la grille  """
		s = "["
		for boite in self.grille:
			s += "["
			for cell in boite:
				s += str(cell)+","
			s += "]"
		s += "] grille avec"+" "+str(len(self.grille))+" cases"
		return(s)
	
############# Classe Boule #############

class Boule:
	""" Classe qui définit une cellule.
	Une boule sera définie par :
		- ses coordonnées (x, y)
		- une image pour une représentation graphique, dimensionnée suivant le rayon
	"""

	def __init__(self,nom, position, nomFichierImage):
		""" Constructeur d'une Boule.
		Paramètres :
			- position : tuple des coordonnées initiales du centre de la boule
			- nomFichierImage : nom du fichier de l'image utilisée pour l'afficher
		"""
		# coordonnées du centre de la boule
		self.nom = nom
		self.x, self.y = position[0], position[1]

		# l'image de la boule
		# ...			(chargement de l'image , transparence du fond, redimensionnement)
		surface = pygame.image.load(nomFichierImage)
		self.image = pygame.transform.scale(surface,(2*RAYON,2*RAYON))


	def __str__(self):
		""" Renvoie une chaine de caractère décrivant la Cellule (nom et position) """
		a = str(self.x)
		b = str(self.y)
		tuple = (a,b)
		desc = self.nom+str(tuple)
		return(desc)			


	def affiche(self,ecran):
		""" Affiche une Boule sur l'écran.
		Paramètres :
			- ecran : l'écran sur lequel la Boule doit s'afficher
		"""
		# Attention, le vecteur position utilisé pour l'affichage est un translaté du vecteur position stocké en attribut
		# print(self.image)
		# print((self.x,self.y))
		ecran.blit(self.image,(self.x,self.y))
		return()			

	def trouverVoisins(self,g):#g est la grille divisant l'espace (i.e. la grille)
		''' donne la liste des voisins d'une cellule, g : grille '''
		ix = int(floor((self.x-X_MIN)/DELTA_X))+1
		iy = int(floor((self.y-Y_MIN)/DELTA_Y))+1
		k_Xi = ix + (iy-1)*N_X  #on calcule k, le numero de la boite qui la contient
		L_cell_peut_etre_voisines = [] 
		L_cell_voisines = []
		# print("k_Xi :",(k_Xi))
		
		#on ajoute dans une liste toutes les cellules qui peuvent etre voisines 
		# print("voisins eventuels au debut :",L_pe_voisins)
		# print("g =",str(g))
		# print(g.grille[k_Xi])
		# L_pe_voisins += g.grille[k_Xi]
		for i in range(1,6):#parcourir les boites adjacentes a la boite k
			if(i != 2):
				if(k_Xi-i >= 0):
					L_cell_peut_etre_voisines += g.grille[k_Xi-i]
				if(k_Xi+i <= N_X*N_Y):
					L_cell_peut_etre_voisines += g.grille[k_Xi+i]
				
		#pour chaque cellule dans la liste, on teste si elle est voisine
		for cell in L_cell_peut_etre_voisines:
			if self.distance(cell)<=RAYON_A:
				L_cell_voisines.append(cell)
				
		return(L_cell_voisines)
	
	
	def nouvelle_position(self,L_voisins):
		''' calcule la position suivante d'une cellule, L_voisins : liste des cellules voisines '''
		# print(self)
		nextPosition = array([0,0])#prochaine position de la cellule Xi 
		nb_cell_voisines = len(L_voisins)#nombre de cellules voisines
		for k in range(nb_cell_voisines):
			voisin = L_voisins[k]
			distance_self_voisin = self.distance(voisin)#distance entre Xi et Xj
			if(distance_self_voisin != 0):#exclut le cas ou Xi = Xj
				nextPosition = nextPosition + (derivee_lennard_jones_pot(distance_self_voisin)/distance_self_voisin)*array([float(self.x-voisin.x),float(self.y-voisin.y)])
		position = array([self.x,self.y])
		vecteur_aleatoire = randn(2)
		D = 0.282
		bruit = sqrt(2*D*DELTA_T)*vecteur_aleatoire
		nextPosition = position - DELTA_T*nextPosition #+bruit
		# print("next =",nextPosition)
		return(nextPosition)#retourne un vecteur		

	def nouvelle_position_sans_grille(self,L_voisins):
		''' calcule la position suivante d'une cellule, L_voisins : liste des cellules voisines '''
		# print(self)
		nextPosition = array([0,0])#prochaine position de la cellule Xi 
		nb_cell_voisines = len(L_voisins)#nombre de cellules voisines
		for k in range(nb_cell_voisines):
			voisin = L_voisins[k]
			distance_self_voisin = self.distance(voisin)#distance entre Xi et Xj
			if(distance_self_voisin != 0):#exclut le cas ou Xi = Xj
				nextPosition = nextPosition + (derivee_lennard_jones_pot(r).subs(r,distance_self_voisin)/distance_self_voisin)*array([float(self.x-voisin.x),float(self.y-voisin.y)])
		position = array([self.x,self.y])
		vecteur_aleatoire = randn(2)
		D = 10000
		bruit = sqrt(2*D*DELTA_T)*vecteur_aleatoire
		nextPosition = position - DELTA_T*nextPosition+bruit
		# print("next =",nextPosition)
		return(nextPosition)#retourne un vecteur

	def rebond(self):
		""" Permet de gérer le rebond des particules sur les bandes de la table """
		if self.x >= LARGEUR-BORD-2*RAYON:
			self.vx = -self.vx
		elif self.y >= LONGUEUR-BORD-2*RAYON:
			self.vy = -self.vy
		elif self.x <= BORD:
			self.vx = -self.vx
		elif self.y <= BORD:
			self.vy = -self.vy

	def distance(self,b):
		distance = sqrt((b.x-self.x)**2+(b.y-self.y)**2)
		return(distance)			

def nouvelles_positions(L_positions,g):
	''' calcule les positions suivantes de toutes les cellules, L_positions : liste des positions actuelles des cellules, g : la girlle '''
	L_nouvelles_positions = []#liste temporaire des nouvelles positions 
	for cell in L_positions:#on parcourt toutes les boules
		# print("cell =",str(cell))
		L_voisins = cell.trouverVoisins(g)#on determine les voisins de la boule
		L_nouvelles_positions.append(cell.nouvelle_position(L_voisins))#a partir de sa liste de voisins, on calcule la nouvelle position
	for k in range(len(L_positions)):#on actualise la liste de position avec les nouvelles positions
		L_positions[k].x,L_positions[k].y = L_nouvelles_positions[k]
	# afficher_liste_boules(L_nouvelles_positions)
	return(L_positions)
	
def nouvelles_positions_sans_grille(L_positions,g):
	print("newpos")
	L_nouvelles_positions = []#liste temporaire des nouvelles positions 
	for cell in L_positions:#on parcourt toutes les boules
		# print("cell =",str(cell))
		L_nouvelles_positions.append(cell.nouvelle_position_sans_grille(L_voisins))#a partir de sa liste de voisins, on calcule la nouvelle position
	for k in range(len(L_positions)):#on actualise la liste de position avec les nouvelles positions
		L_positions[k].x,L_positions[k].y = L_nouvelles_positions[k]
	# afficher_liste_boules(L_nouvelles_positions)
	return(L_positions)

def afficher_liste_boules(L_boules):
	print("[",end='')
	for cell in L_boules:
		print(str(cell)+",",end='')
	print("]",end='')
	s = " liste avec "+str(len(L_boules))+" cases\n"
	print(s,end='')
# 
# X1 = Boule("X1",(1,1),"boule_blanche.png") 
# X2 = Boule("X2",(3,2),"boule_blanche.png") 
# X3 = Boule("X3",(1,3),"boule_blanche.png")  
# L_pos = [X1,X2,X3]
# g = Grille(L_pos)
# # 
# print("L_pos avant = ",end='')
# afficher_liste_boules(L_pos) 
# L_pos = nouvelles_positions(L_pos,g)
# print("L_pos apres = ",end='')
# afficher_liste_boules(L_pos)
# g = Grille(L_pos)
# print("grille =")
# print(str(g))



# Lv_X1 = X1.voisins(g)
# print("Lv_X1 = ",end='')
# # afficher_liste_boules(Lv_X1)