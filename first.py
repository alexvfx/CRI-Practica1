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
        dicc[x] =[]
    for element in diccionari:
        dicc[len(element)].append(element)
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
    #variablesReturn = np.array([], dtype=dt)
    variablesReturn = []
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
                        m = [indice, contEspais,-1,1]
                        variablesReturn.append(m)
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
                        m = [indice, contEspais,-1,2]
                        variablesReturn.append(m)
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

    #dtRestr = np.dtype([('id1',np.int32,1),('word1',np.int32,1),('id2',np.int32,1), ('word2',np.int32,1)])
    #restriccions = np.array([],dtype=dtRestr)

    restriccions = []
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
                #m = np.array([(X[x][y],contHor[X[x][y]],Y[x][y],contVer[Y[x][y]])], dtype=dtRestr)
                m = [X[x][y],contHor[X[x][y]],Y[x][y],contVer[Y[x][y]]]
                restriccions.append(m)
    return restriccions

def construirDA(variables,dicc):
    DA = {}
    for variable in variables:
        llista = []
        for i in range(len(dicc[variable[1]])):
            #llista = np.append(llista,(i))
            llista.append((i))
        DA[(variable[0],variable[3])] = llista
    return DA

def SatisfaRestriccions(v, LVA, R, DA, D):
    if LVA == []:
        return True
    else:
        for restriccio in R:
            if v[3]==1:  #horitzontal
                if restriccio[0]==v[0]:
                    for varAssig in LVA:
                        if varAssig[3]==2:
                            if varAssig[0]==restriccio[2]:
                                if not D[v[1]][v[2]][restriccio[1]]== D[varAssig[1]][varAssig[2]][restriccio[3]]:
                                    return False
            else:    #vertical
                if restriccio[2]==v[0]:
                    for varAssig in LVA:
                        if varAssig[3]==1:
                            if varAssig[0]==restriccio[0]:
                                if not D[v[1]][v[2]][restriccio[3]]== D[varAssig[1]][varAssig[2]][restriccio[1]]:
                                    return False
        return True

def printaSolucio(taulerHor, taulerVer, llista,dicc):
    solucio = np.zeros(taulerHor.shape, dtype='str')
    for x in range (0, taulerHor.shape[0]):
        indexLletra = 0
        for y in range (0, taulerHor.shape[1]):
            if (int(taulerHor[x,y]) > 0):
                for j in range(0, len(llista)):
                    if (llista[j][0] == int(taulerHor[x,y]) and llista[j][3]==1):
                        solucio[x,y]=chr(dicc[llista[j][1]][llista[j][2]][indexLletra])
                        indexLletra+=1
                        #print (chr(dicc[llista[j][1]][llista[j][2]][y-llista[j][1]]))
            else:
                indexLletra = 0
                solucio[x,y]="!"


    for y in range (0, taulerVer.shape[0]):
        indexLletra = 0
        for x in range (0, taulerVer.shape[1]):
            if (int(taulerVer[x,y]) > 0):
                for j in range(0, len(llista)):
                    if (llista[j][0] == int(taulerVer[x,y]) and llista[j][3]==2):
                        solucio[x,y]=chr(dicc[llista[j][1]][llista[j][2]][indexLletra])
                        indexLletra+=1
                        #print (chr(dicc[llista[j][1]][llista[j][2]][y-llista[j][1]]))
            else:
                indexLletra = 0
                #solucio[x,y]="!"
    print ("\n",solucio)
'''ActualitzarDominis(‘(X v),L,R):
Retorna la llista dels dominis per a les variables no assignades
de L considerant les restriccions de R despres d’assignar X amb v, retorna fals si algun
domini actualitzat és buit.
'''
def ActualitzarDominis(v, LVNA, R, DA, D):
    for restriccio in R:
        if v[3]==1: #horitzontal
            if restriccio[0]==v[0]:
                for vna in LVNA:
                    if vna[3]==2:
                        if vna[0]==restriccio[2]:
                            domini = DA[(vna[0],vna[3])]
                            #nouDomini = np.array([],dtype=np.int32)
                            nouDomini = []
                            for index in range(len(domini)):
                                if D[v[1]][v[2]][restriccio[1]]== D[vna[1]][domini[index]][restriccio[3]]:
                                    nouDomini.append(domini[index])
                            DA[(vna[0],vna[3])] = nouDomini
        else:
             if restriccio[2]==v[0]:
                for vna in LVNA:
                    if vna[3]==1:
                        if vna[0]==restriccio[0]:
                            domini = DA[(vna[0],vna[3])]
                            nouDomini = []
                            for index in range(len(domini)):
                                if D[v[1]][v[2]][restriccio[3]]== D[vna[1]][domini[index]][restriccio[1]]:
                                    nouDomini.append(domini[index])
                            DA[(vna[0],vna[3])] = nouDomini

    for domini in DA.values():
        if len(domini)==0:
            return False
    #DA[(v[0],v[3])] = v[[2]]
    return DA

def Backtracking(LVA, LVNA, R, DA, D):
    if len(LVNA) == 0:
        return LVA
    var = LVNA[0]
    LVNA.pop(0)
    for paraula in DA[(var[0],var[3])]:
        var[2]=paraula
        if SatisfaRestriccions(var, LVA, R, DA, D):
            DAaux = dict(DA)
            DAaux = ActualitzarDominis(var, LVNA, R, DAaux, D)
            if(DAaux != False):
                LVA.append(var)
                res=Backtracking(LVA, LVNA, R, DAaux, D)
                if res != 0:
                    return res
        var[2]= -1
    return 0

if __name__ == "__main__":

    dt = np.dtype([('id',np.int32,1 ),('size',np.int32,1),('index', np.int32, 1), ('orientation',np.int32,1)])

    fitxer_dic = "diccionari_A.txt"
    fitxer_tau = "crossword_A.txt"
    diccionari = np.genfromtxt(fitxer_dic,dtype='S16')
    tauler = np.loadtxt(fitxer_tau, dtype='S16', comments='!')
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
    #print ("Restriccions:\n",restriccions,"\n")
    dicc = construirDiccionari(diccionari)
    DA = construirDA(variables,dicc)
    #print ("Dicc\n:",dicc,"\nDA: ",DA)

    llistaBuida = []
    llista = Backtracking(llistaBuida,variables,restriccions,DA, dicc)
    #print ("Solucio:\n", llista)
    if llista != 0:
        for j in range(0,len(llista)):
            print (dicc[llista[j][1]][llista[j][2]])
        printaSolucio(X,Y,llista,dicc)

