__author__ = 'Marti, Alex, Alvaro'
# -*- coding: utf-8 -*-

#1 -> horitzontal
#2 -> vertical

#Variables -> [float id,int size, string paraula]
#Restrictions -> [id1, pos1, id2, pos 2]
import numpy as np
np.set_printoptions(precision=2)
dt = np.dtype([('id',np.int32,1),('size',np.int32,1),('name', np.str_, 16), ('orientation',np.int32,1)])

fitxer_dic = "diccionari_C.txt"
fitxer_tau = "crossword_CB.txt"
diccionari = np.genfromtxt(fitxer_dic,dtype='str')
tauler = np.loadtxt(fitxer_tau, dtype='|S16', comments='!')
tauler.tostring()

def construirDiccionari(diccionari):
    dicc = {}
    dicc[2] = np.array([])
    dicc[3] = np.array([])
    dicc[4] = np.array([])
    dicc[5] = np.array([])
    dicc[6] = np.array([])
    dicc[7] = np.array([])
    for element in diccionari:
        if len(element) == 2:
            dicc[2] = np.append(dicc[2],[element])
        elif len(element) == 3:
            dicc[3] = np.append(dicc[3],[element])
        elif len(element) == 4:
            dicc[4] = np.append(dicc[4],[element])
        elif len(element) == 5:
            dicc[5] = np.append(dicc[5],[element])
        elif len(element) == 6:
            dicc[6] = np.append(dicc[6],[element])
        elif len(element) == 7:
            dicc[7] = np.append(dicc[7],[element])
    return dicc

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
                    if (y < tauler.shape[1]-1 and int(tauler[y+1,x]) == 0):
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

    variablesReturn = np.array([], dtype=dt)

    for x in range(0,X.shape[0]):
        for y in range(0,X.shape[1]):
            if (X[x,y] > 0 and X[x,y] != indice):
                indice = X[x,y]
                contParaules += 1
                contEspais=1
            elif (X[x,y] == indice):
                contEspais+=1
                if (contEspais > 1):
                    if (y==X.shape[0]-1 or X[x,y+1] == 0):
                        m = np.array([(indice, contEspais,'',1)], dtype=dt)
                        variablesReturn = np.append(variablesReturn, m)

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
                    if (y==Y.shape[0]-1 or Y[y+1,x] == 0):
                        m = np.array([(indice, contEspais,'',2)], dtype=dt)
                        variablesReturn = np.append(variablesReturn, m)

    return variablesReturn

def contarParaules(X,Y):
    contParaules=0
    indice = 0
    for x in range(0,X.shape[0]):
        for y in range(0,X.shape[1]):
            if (X[x,y] > 0 and X[x,y] != indice):
                indice = X[x,y]
                contParaules += 1


    for x in range(0,Y.shape[0]):
        for y in range(0,Y.shape[1]):
            if (Y[y,x] > 0 and Y[y,x] != indice):
                indice = Y[y,x]
                contParaules += 1


    return contParaules

construirVariablesHor(tauler, X)
construirVariablesVer(tauler, Y)
variables = crearVariables(X,Y)

#DEFINICIO DE RESTRICCIONS#
def construccioRestriccions(X,Y):
    contRest = 0
    for x in range (0, X.shape[0]):
        for y in range (0, Y.shape[1]):
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
    return restriccions

print ('Variables', variables)
print ('Restriccions',construccioRestriccions(X,Y))
dicc = construirDiccionari(diccionari)
#print ('diccionari', dicc)

def SatisfaRestriccions(v, LVA, R):
    if not LVA:
        return True
    else:
        for restriccio in R:
            if v[3]==1:
                if restriccio[0]==v[0]:
                    for variable in LVA:
                        if variable[0]==restriccio[2]:
                            if variable[3]==2:
                                if not v[2][restriccio[1]]==variable[2][restriccio[3]]:
                                    return False
            else:
                if restriccio[2]==v[0]:
                    for variable in LVA:
                        if variable[0]==restriccio[0]:
                            if variable[3]==1:
                                if not v[2][restriccio[3]]==variable[2][restriccio[1]]:
                                    return False
        return True

def Backtracking(LVA, LVNA, R, D):
    if LVNA == []:
        return LVA
    var = LVNA[0]
    for paraula in D[var[1]]:
        var[2]=paraula
        sat=SatisfaRestriccions(var, LVA, R)
        if sat == True:
            LVA = np.append(LVA, var)
            print (LVA)
            LVNA = np.delete(LVNA,0)
            res=Backtracking(LVA, LVNA, R, D)
            if res:
                return res
            else:
                mal = np.delete(LVA, 0)
                LVNA = np.insert(LVNA, 0, mal)
        var[2]=''
    return None
llistaBuida = np.array([], dtype=dt)
print (Backtracking(llistaBuida,variables,construccioRestriccions(X,Y),dicc))

if __name__ == "__main__":
    pass
