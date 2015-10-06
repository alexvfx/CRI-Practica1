__author__ = 'Marti, Alex, Alvaro'
# -*- coding: utf-8 -*-

#1 -> horitzontal
#2 -> vertical

#Variables -> [float id,int size, string paraula]
#Restrictions -> [id1, pos1, id2, pos 2]
import numpy as np

def construirDiccionari(diccionari):
    dicc = {}
    max = 20
    for x in range(2,max+1):
        dicc[x] = np.array([])
    for element in diccionari:
        dicc[len(element)] = np.append(dicc[len(element)],[element])
    return dicc

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
                adjudicat = False

def construirVariablesVer(tauler,Y):
    for y in range (0, tauler.shape[0]):
        adjudicat = False
        indice = 0
        for x in range (0, tauler.shape[1]):
            try:
                if (int(tauler[x,y]) > 0 and adjudicat==False):
                    if (x < tauler.shape[1]-1 and int(tauler[x+1,y])==0):
                        indice = int(tauler[x,y])
                        adjudicat = True
                if (int(tauler[x,y]) >= 0):
                    Y[x,y] = indice

            except ValueError:
                indice = 0
                adjudicat = False

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

def construirRestriccions(X,Y):

    dtRestr = np.dtype([('id1',np.int32,1),('word1',np.int32,1),('id2',np.int32,1), ('word2',np.int32,1)])
    restriccions = np.array([],dtype=dtRestr)
    contVer = {}
    contHor = {}
    for x in range (0, tauler.shape[0]):
        for y in range (0, tauler.shape[1]):
            if (X[x][y] >0):
                if(X[x][y] not in contHor.keys()):
                    contHor[X[x][y]]=0
                else:
                    contHor[X[x][y]]+=1
            if(Y[x][y] >0):
                if(Y[x][y] not in contVer.keys()):
                    contVer[Y[x][y]]=0
                else:
                    contVer[Y[x][y]]+=1

            if(X[x][y] >0 and Y[x][y] >0):
                m = np.array([(X[x][y],contHor[X[x][y]],Y[x][y],contVer[Y[x][y]])], dtype=dtRestr)
                restriccions = np.append(restriccions, m)
    return restriccions

def SatisfaRestriccions(v, LVA, R):
    if LVA == []:
        return True
    else:
        for restriccio in R:
            if v[3]==1:  #horitzontal
                if restriccio[0]==v[0]:
                    for varAssig in LVA:
                        if varAssig[3]==2:
                            if varAssig[0]==restriccio[2]:
                                if not v[2][restriccio[1]]==varAssig[2][restriccio[3]]:
                                    return False
            else:    #vertical
                if restriccio[2]==v[0]:
                    for varAssig in LVA:
                        if varAssig[3]==1:
                            if varAssig[0]==restriccio[0]:
                                if not v[2][restriccio[3]]==varAssig[2][restriccio[1]]:
                                    return False
        return True

'''ActualitzarDominis(‘(X v),L,R):
Retorna la llista dels dominis per a les variables no assignades
de L considerant les restriccions de R despres d’assignar X amb v, retorna fals si algun
domini actualitzat és buit.
'''
def ActualitzarDominis():
    return True

def Backtracking(LVA, LVNA, R, D):
    if len(LVNA) == 0:
        return LVA
    var = LVNA[0]
    LVNA = np.delete(LVNA,0)
    for paraula in D[var[1]]:
        var[2]=paraula
        if SatisfaRestriccions(var, LVA, R):
            DA = ActualitzarDominis()
            if(DA != False):
                res=Backtracking(np.append(LVA, var), LVNA, R, D)
                if res != 0:
                    return res
        var[2]=''
    return 0

if __name__ == "__main__":
    np.set_printoptions(precision=2)
    dt = np.dtype([('id',np.int32,1),('size',np.int32,1),('name', '|S16', 1), ('orientation',np.int32,1)])

    fitxer_dic = "diccionari_CB.txt"
    fitxer_tau = "crossword_CB.txt"
    diccionari = np.genfromtxt(fitxer_dic,dtype='|S16')
    tauler = np.loadtxt(fitxer_tau, dtype='|S16', comments='!')
    tauler.tostring()

    X = np.zeros(tauler.shape)
    Y = np.zeros(tauler.shape)
    construirVariablesHor(tauler, X)
    construirVariablesVer(tauler, Y)
    print ("tauler")
    print (X,"\n")
    print (Y,"\n")
    variables = crearVariables(X,Y)

    print ("Variables:\n",variables,"\n")
    restriccions = construirRestriccions(X,Y)
    print ("Restriccions:\n",restriccions,"\n")
    dicc = construirDiccionari(diccionari)
    llistaBuida = np.array([], dtype=dt)

    print ("Solucio:\n",Backtracking(llistaBuida,variables,restriccions,dicc))
