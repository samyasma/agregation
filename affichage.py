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

from cellule import *
import pygame
from pygame.locals import *
from random import randint

############# Quelques fonctions utiles #############

def separe(ligne):
	ligne=ligne.strip("\n")
	liste=ligne.split(",") # enleve un eventuel \n et/ou des espaces a la fin de la ligne
	return(liste)

def position_initiale():
	listeBoules = []
	for k in range(N):
		boule_x = randint(20,400) 
		boule_y = randint(20,650) 
		nom = "X"+str(k)
		couleur = "boule_rouge.png"
		position = (boule_x,boule_y)
		boule = Boule(nom,position,couleur)
		listeBoules.append(boule)
	return(listeBoules)
	
def position_initiale_fichier():
	""" On récupère dans le fichier infos_boules.txt les positions initiales de chaque boules, et on crée toutes les boules sur ces positions """
	nbCell = 0
	f = open("infos_boules.txt")
	listeBoules = []
	for ligne in f:
		nbCell += 1
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

# titre de la fenetre
pygame.display.set_caption("Agregation de cellules")

# recuperation du fond qui est ...., que l'on met dans une variable nommée fond
fond = pygame.image.load("billard.png")

# creation et initialisation des cellules
listeBoules = position_initiale()

listeN = [] #liste des populations au cours du temps

# boucle de gestion des événements et d'affichage (dont on ne sort que si l'on ferme la fenêtre)
onContinue = True
horloge = pygame.time.Clock()
while onContinue:
# Gestion des événements (on parcourt tous les événements, et si un évènement est de type QUIT, alors on ne continue plus)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			onContinue = False

	# on colle le fond au coin superieur gauche de la fenetre
	ecran.blit(fond,(0,0)) 
		
	# affichage des boules	
	for boule in listeBoules:
		boule.affiche(ecran)
	
	# mise a jour de la grille
	grille = Grille(listeBoules)
	# print(t)
	
	# division et mort des cellules (en tant qu'evenements independants)
	listeBoules = division_et_mort(listeBoules)
	print("tps = ",len(listeN))
	
	# calcul et mise a jour des positions des cellules
	listeBoules = nouvelles_positions(listeBoules,grille)
	
	# recuperation du nouveau nombre total d'individus
	listeN.append(len(listeBoules))
	
	# mise a jour de l'affichage
	pygame.display.flip()
	
	#end for 2
#end for 1