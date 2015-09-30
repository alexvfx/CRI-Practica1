__author__ = 'alvaro'
# -*- coding: utf-8 -*-

import numpy as np
np.set_printoptions(precision=2)

fitxer_dic = "diccionari_C.txt"
fitxer_tau = "crossword_CB.txt"
diccionari = np.genfromtxt(fitxer_dic,dtype='str')
tauler = np.loadtxt(fitxer_tau, dtype='|S16', comments='!')
tauler.tostring()

X = np.zeros(tauler.shape)
Y = np.zeros(tauler.shape)

def construirVariablesHor(tauler,X):
    for x in range (0, tauler.shape[0]):
        adjudicat = False
        indice = 0
        for y in range (0, tauler.shape[1]):
            try:
                if (int(tauler[x,y]) > 0 and adjudicat==False):
                    indice = int(tauler[x,y])
                    adjudicat = True
                if (int(tauler[x,y]) >= 0):
                    X[x,y] = indice
            except ValueError:
                indice = 0

def construirVariablesVer(tauler,Y):
    for x in range (0, tauler.shape[0]):
        adjudicat = False
        indice = 0
        for y in range (0, tauler.shape[1]):
            try:
                if (int(tauler[y,x]) > 0 and adjudicat==False):
                    indice = int(tauler[y,x])
                    adjudicat = True
                if (int(tauler[y,x]) >= 0):
                    Y[y,x] = indice
            except ValueError:
                indice = 0

def crearVariables(X,Y):
    contParaules=-1
    contEspais=0
    indice = 0
    variables = np.zeros((9,),dtype=('f4,i4,a10'))
    for x in range(0,X.shape[0]):
        for y in range(0,X.shape[1]):
            if (X[x,y] > 0 and X[x,y] != indice):
                indice = X[x,y]
                contParaules += 1
                contEspais=1
            elif (X[x,y] == indice):
                contEspais+=1
                if (contEspais > 1):
                    variables[contParaules] = (indice,contEspais,'')

    contEspais=0
    for x in range(0,Y.shape[0]):
        for y in range(0,Y.shape[1]):
            if (Y[y,x] > 0 and Y[y,x] != indice):
                indice = Y[y,x]
                contParaules += 1
                contEspais=1
            elif (Y[y,x] == indice):
                contEspais+=1
                if (contEspais > 1):
                    variables[contParaules] = (indice+0.2,contEspais,'')
    return variables

construirVariablesHor(tauler, X)
construirVariablesVer(tauler, Y)
variables = crearVariables(X,Y)


print (X,"\n\n",Y,"\n\n", np.around(variables[8][0], decimals=1),"\n\n", variables,"\n\n")

#DEFINICIO DE RESTRICCIONS#

contRest = 0
for x in range (0, tauler.shape[0]):
    for y in range (0, tauler.shape[1]):
        if (X[x][y] >0):
            if(Y[x][y] >0):
                contRest += 1

restriccions = np.zeros((contRest,),dtype=('f4,i4,f4,i4'))
contRest = 0


contVer = {}
contHor = {}
ver = False
hor = False
for x in range (0, tauler.shape[0]):
    for y in range (0, tauler.shape[1]):
        ver = False
        hor = False
        if (X[x][y] >0):
            hor = True
            if(X[x][y] not in contHor.keys()):
                contHor[X[x][y]]=1
            else:
                contHor[X[x][y]]+=1

        if(Y[x][y] >0):
            ver = True
            if(Y[x][y] not in contVer.keys()):
                contVer[Y[x][y]]=1
            else:
                contVer[Y[x][y]]+=1

        if(hor and ver):
            restriccions[contRest][0] = X[x][y]
            restriccions[contRest][1] = contHor[X[x][y]]
            restriccions[contRest][2] = Y[x][y]
            restriccions[contRest][3] = contVer[Y[x][y]]
            contRest += 1


print ('Restriccions', restriccions)

#Variables -> [float id,int size, string paraula]
#Restrictions -> [id1, pos1, id2, pos 2]



"""
    Funcio Backtracking(LVA,LVNA,R,D)
Si (LVNA és buida) llavors Retornar(LVA) fSi
Var=Cap(LVNA);
Per a cada (valor del Domini(Var, D) que podem assignar a Var) fer
Si (SatisfaRestriccions([Var valor],LVA,R)) llavors
Res=Backtracking(Insertar([Var, valor],LVA),Cua(LVNA),R,D);
Si (Res és una solució completa) llavors
Retornar(Res);
Fsi
Fsi
Fper
Retornar(Falla)
FFuncio
    :return:
 """



def backtracking(lva, lvna, r, d):
  if not lvna:
      print ("llista buida")
      return lva
  else:
      print (lvna)

if __name__ == "__main__":
    pass
