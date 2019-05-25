RAYON = 17
from pylab import *
from sympy import var
from affichage import *

def potentiel(r):
    return((r-2*RAYON)**2)

##################TRACE DU POTENTIEL###################
x = linspace(-0.3,69)
plot(x,potentiel(x),label="V(r) = (r-2*R)**2")
plt.title("Potentiel en fonction de la distance entre deux cellules",fontsize=25)
plt.xlabel('Distance r entre deux cellules (leurs centres)', fontsize=24)
plt.ylabel('Valeur du potentiel', fontsize=24)
legend(loc='upper center')
show()


##################TRACE DU NOMBRE D'INDIVIDUS###################
pop = listeN[0:len(listeN)]
t = arange(0,len(listeN),1)
plt.figure(figsize=(15,15))
plot(t,pop) #pas de label, de formule pour N comme on part de donnees empiriques
plt.title("Nombre total de cellules en fonction du temps en présence de mort et de division",fontsize=22)
plt.xlabel('Temps', fontsize=24)
plt.ylabel("Nombre total de cellules", fontsize=24)
# legend(loc='upper center')
show()










# print("distance")

# distance = a.dist(b)
# print(distance)

# position = (0,0)
# vitesse = (5,8)
# boule = Boule(position,vitesse,"boule_blanche.png")
# s = str(boule)
# print(s)

# listeDesBoules = position_initiale()

