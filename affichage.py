# -*- coding: utf-8 -*-
#
# Fichier : affichage.py
# Date : février 2019 
# Auteurs : Dang-Vu Laurent
# 
# Contient le squelette de la classe grille qui modélise une grille et le squelette de la classe Boule
# qui modélise des cellules
#
#===========================================


############# Quelques modules utiles #############

from cellules import *
import pygame
from pygame.locals import *
from random import randint

############# Quelques fonctions utiles #############
def separe(ligne):
	ligne=ligne.strip("\n")
	liste=ligne.split(",") # enlever un eventuel \n et/ou des espaces a la fin de la ligne
	return(liste)

def position_initiale():
	listeBoules = []
	for k in range(200):
		boule_x = randint(20,450) 
		boule_y = randint(20,750) 
		nom = "X"+str(k)
		couleur = "boule_jaune.png"
		position = (boule_x,boule_y)
		boule = Boule(nom,position,couleur)
		listeBoules.append(boule)
		# afficher_liste_boules(listeBoules)
	return(listeBoules)
	
def position_initiale_fichier():
	""" On récupère dans le fichier infos_boules.txt les positions initiales de chaque boules, et on crée toutes les boules sur ces positions """
	# ...
	f = open("infos_boules.txt")
	listeBoules = []
	for ligne in f:
		bouleListe = separe(ligne)
		boule_x = int(bouleListe[1]) 
		boule_y = int(bouleListe[2])
		nom = bouleListe[0]
		couleur = bouleListe[3]
		position = (boule_x,boule_y)
		boule = Boule(nom,position,couleur)
		listeBoules.append(boule)
	f.close()
	return(listeBoules)							


############# Création du billard, affichage graphique #############

# on initialise pygame
pygame.init()

# on crée une fenêtre que l'on stocke dans une variable nommée ecran. Les dimensions de la fenêtre sont celles stockées dans les variables LARGEUR et LONGUEUR (exprimées en pixels)
ecran = pygame.display.set_mode((500,800))

# on donne un joli titre à la fenêtre
pygame.display.set_caption("Agregation de cellules")

# on récupère le fond qui est l'image du billard avec ses bandes, que l'on met dans une variable nommée fond
fond = pygame.image.load("billard.png")

# création boule(s)
listeBoules = position_initiale()
# for cell in listeBoules:
# 	print(str(cell))

# boucle de gestion des événements et d'affichage (dont on ne sort que si l'on ferme la fenêtre)
onContinue = True
horloge = pygame.time.Clock()
while onContinue:

	# Gestion des événements (on parcourt tous les événements, et si un évènement est de type QUIT, alors on ne continue plus)
	# print("while")
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			onContinue = False
	
	# on colle le fond dans la fenêtre
	ecran.blit(fond,(0,0)) # on colle le fond en position (0,0) qui sont les coordonnées du coin supérieur gauche de la fenêtre...
		
	#affichage des boules	
	for boule in listeBoules:
		# ecran.blit(boule.image,(boule.x-2*RAYON,boule.y-2*RAYON))
		ecran.blit(boule.image,(boule.x,boule.y))

	# mise a jour de la grille, des positions des cellules et affichage graphique boule(s)
	grille = Grille(listeBoules)
	# print("grille :",str(grille))
	# print(0)
	
	# afficher_liste_boules(listeBoules)

	# print(str(g))
	# afficher_liste_boules(newPositions(listeBoules,grille))
	listeBoules = nouvelles_positions(listeBoules,grille)
	# listeBoules[2].distance(listeBoules[4])	
	# print(1)
	# afficher_liste_boules(listeBoules)
	# print("\n")
	# on met à jour l'affichage
	pygame.display.flip()

	# on attend un petit peu, pour ne boucler que 25 fois maxi par seconde
	# ...