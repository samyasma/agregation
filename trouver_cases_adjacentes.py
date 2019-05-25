from pylab import *

N_X = 4 #indice i ou j maximal

T = array([[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,16]])
(i,j) = where(T==10)[0][0],where(T==10)[1][0]

L_adjacents = []
for k in range(1,17):
    L_adjacents.append([])
    i_c,j_c = where(T==k)[0][0]+1,where(T==k)[1][0]+1
    L_adjacents[k-1].append((i_c,j_c))
    for k1 in range(len(T)):#[0;3]
        for k2 in range(len(T)):
            i,j = k1+1,k2+1
            ai = i_c-1
            bi = i_c+1
            aj = j_c-1
            bj = j_c+1
            if((ai<=i<=bi)and(aj<=j<=bj))and(0<i<=N_X)and(0<j<=N_X)and((i,j)!=(i_c,j_c)):
                # print(k)
                L_adjacents[k-1].append((i,j))

L_adjacents_unD = []
i = 0
for elem in L_adjacents:
    L_adjacents_unD.append([])
    for couplet in elem:
        ix = couplet[0]
        iy = couplet[1]
        k = ix + (iy-1)*N_X
        L_adjacents_unD[i].append(k)
    i += 1

L_adjacents_unD = array(L_adjacents_unD)
print(L_adjacents_unD)
# pour chaque ligne, le premier element est celui dont on cherche les adjacents, et les autres sont les cases adjacentes a cet element
print(L_adjacents_unD[3])#je veux les adjacents de k, il faut ecrire k-1 a cause du premier indice python a 0
