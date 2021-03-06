__author__ = 'Marti, Alex, Alvaro'
# -*- coding: utf-8 -*-

#1 -> horitzontal
#2 -> vertical

#Variables -> [float id,int size, string paraula]
#Restrictions -> [id1, pos1, id2, pos 2]
import numpy as np
import random
import time

def construirDiccionari(diccionari):
    '''Crea un diccionari ordenat segons el tamany de cada paraula'''
    dicc = {}
    max = 20
    for x in range(2,max+1):
        dicc[x] =[]
    for element in diccionari:
        dicc[len(element)].append(element)
    return dicc

def construirVariablesHor(tauler,X):
    '''crear un tauler(paraules horitzontals) X amb tots els IDS de les variables a la posició on va cada paraula'''
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
    '''crear un tauler(paraules verticals) Y amb tots els IDS de les variables a la posició on va cada paraula'''
    for y in range (0, tauler.shape[0]):
        adjudicat = False
        indice = 0
        for x in range (0, tauler.shape[1]):
            try:
                if (int(tauler[x,y]) > 0 and adjudicat==False):
                    if (x < tauler.shape[1]-1 and int(tauler[x+1,y])>=0):
                        indice = int(tauler[x,y])
                        adjudicat = True
                if (int(tauler[x,y]) >= 0):
                    Y[x,y] = indice

            except ValueError:
                indice = 0
                adjudicat = False

def crearVariables(X,Y):
    '''Recorrent els taulers X,Y crea la llista de variables'''

    contEspais=0 #conta els espais que té cada paraula
    indice = 0 # fixa l'id d'una paraula per afegir-ho a la variable
    variablesReturn = [] #llista on s'omplen les variables

    #variables Horitzontals
    for x in range(0,X.shape[0]):
        for y in range(0,X.shape[1]):
            #Troba al tauler un id no assignat, assigna indice per fixar aquest indice
            if (X[x,y] > 0 and X[x,y] != indice):
                indice = X[x,y]
                contEspais=1
            #assigna a la variable l'index fixat
            elif (X[x,y] == indice):
                contEspais+=1
                if (contEspais > 1):
                    if (y==X.shape[0]-1 or X[x,y+1] == 0):
                        m = [indice, contEspais,-1,1]
                        variablesReturn.append(m)

    #variables verticals
    contEspais=0
    for x in range(0,Y.shape[0]):
        for y in range(0,Y.shape[1]):
            #Troba al tauler un id no assignat, assigna indice per fixar aquest indice
            if (Y[y,x] > 0 and Y[y,x] != indice):
                indice = Y[y,x]
                contEspais=1
            #assigna a la variable l'index fixat
            elif (Y[y,x] == indice):
                contEspais+=1
                if (contEspais > 1):
                    if (y==Y.shape[0]-1 or Y[y+1,x] == 0):
                        m = [indice, contEspais,-1,2]
                        variablesReturn.append(m)
    return variablesReturn

def construirRestriccions(X,Y):
    '''recorrer els taulers X,Y per saber on hi ha conflicte entre diferents paraules i retorna una llista amb aquestes restriccions'''

    restriccions = [] #llista on s'afegiran les restriccions
    contVer = {} #diccionari per paraules horitzontals
    contHor = {} #diccionari per paraules verticals

    for x in range (0, tauler.shape[0]):
        for y in range (0, tauler.shape[1]):
            #comprova ID tauler horitzontals si hi ha paraula incrementa aquella posicio del diccionari
            if (X[x][y] > 0):
                if(X[x][y] not in contHor.keys()):
                    contHor[X[x][y]]=0
                else:
                    contHor[X[x][y]]+=1
            #comprova ID tauler verticalss si hi ha paraula incrementa aquella posicio del diccionari
            if(Y[x][y] > 0):
                if(Y[x][y] not in contVer.keys()):
                    contVer[Y[x][y]]=0
                else:
                    contVer[Y[x][y]]+=1

            #Si les posicions al diccionari son mes grans que 1 es que hi ha conflicte i l'afegeix a la llista de conflictes
            if(X[x][y] > 0 and Y[x][y] > 0):
                m = [X[x][y],contHor[X[x][y]],Y[x][y],contVer[Y[x][y]]]
                restriccions.append(m)
    return restriccions

def construirDA(variables,dicc):
    '''Crea un diccionari on per cada variable es crea una Key (id, orientacio) i el seu value és el seu propi domini d'aquella paraula'''
    DA = {}
    for variable in variables:
        llista = []
        for i in range(len(dicc[variable[1]])):
            llista.append((i))
        #random.shuffle(llista)
        DA[(variable[0],variable[3])] = llista
    return DA

def SatisfaRestriccions(v, LVA, R, DA, D):
    '''Comprova que per una variable en concret no hi ha cap conflicte amb tota la llista de variables assignades'''
    if LVA == []:
        return True
    else:
        for restriccio in R:
            if v[3]==1:  #horitzontal
                if restriccio[0]==v[0]: #coincideix la restricció amb la variable
                    for varAssig in LVA:
                        if varAssig[3]==2: #comproba la restricció amb tota la llista de verticals de LVA
                            if varAssig[0]==restriccio[2]: #si troba que hi ha restricció
                                if not D[v[1]][v[2]][restriccio[1]]== D[varAssig[1]][varAssig[2]][restriccio[3]]:#comproba al diccionari la posicio de la lletra on hi ha restriccio
                                    return False
            else:    #vertical
                if restriccio[2]==v[0]:#coincideix la restricció amb la variable
                    for varAssig in LVA:#comproba la restricció amb tota la llista de verticals de LVA
                        if varAssig[3]==1:
                            if varAssig[0]==restriccio[0]:
                                if not D[v[1]][v[2]][restriccio[3]]== D[varAssig[1]][varAssig[2]][restriccio[1]]:#comproba al diccionari la posicio de la lletra on hi ha restriccio
                                    return False
        return True

def printaSolucio(taulerHor, taulerVer, llista,dicc):
    '''retorna un tauler amb totes les paraules finals posades al seu lloc per poder printar-lo posteriorment'''
    solucio = np.zeros(taulerHor.shape, dtype='str')
    for x in range (0, taulerHor.shape[0]):
        indexLletra = 0
        for y in range (0, taulerHor.shape[1]):
            if (int(taulerHor[x,y]) > 0):
                #si troba un id busca a la llista de variables la variable amb aquest id i ho afegeix a solucio buscant-la al diccionari
                for j in range(0, len(llista)):
                    if (llista[j][0] == int(taulerHor[x,y]) and llista[j][3]==1):
                        solucio[x,y]=chr(dicc[llista[j][1]][llista[j][2]][indexLletra])
                        indexLletra+=1

            else:
                indexLletra = 0
                solucio[x,y]="#"
    for y in range (0, taulerVer.shape[0]):
        indexLletra = 0
        for x in range (0, taulerVer.shape[1]):
            if (int(taulerVer[x,y]) > 0):
                #si troba un id busca a la llista de variables la variable amb aquest id i ho afegeix a solucio buscant-la al diccionari
                for j in range(0, len(llista)):
                    if (llista[j][0] == int(taulerVer[x,y]) and llista[j][3]==2):
                        solucio[x,y]=chr(dicc[llista[j][1]][llista[j][2]][indexLletra])
                        indexLletra+=1

            else:
                indexLletra = 0

    return solucio

def ActualitzarDominis(v, LVNA, R, DA, D):
    '''per cada DA comprova totes les restriccions amb LVNA per actualitzar cada domini propi de cada variable'''
    for restriccio in R:
        if v[3]==1: #horitzontal
            if restriccio[0]==v[0]:#comproba si la variable té cap restricció
                for vna in LVNA:
                    if vna[3]==2:
                        if vna[0]==restriccio[2]:#comproba la restriccio amb tota la llista de variables no asignades horitzontals
                            domini = DA[(vna[0],vna[3])]
                            nouDomini = []
                            #crea un nou domini per afegir tots els index del domini vell que satisfan la restricció
                            for index in range(len(domini)):
                                if D[v[1]][v[2]][restriccio[1]]== D[vna[1]][domini[index]][restriccio[3]]:
                                    nouDomini.append(domini[index])
                            DA[(vna[0],vna[3])] = nouDomini
        else:
             if restriccio[2]==v[0]:#comproba si la variable té cap restricció
                for vna in LVNA:
                    if vna[3]==1:#comproba la restriccio amb tota la llista de variables no asignades verticals
                        if vna[0]==restriccio[0]:
                            domini = DA[(vna[0],vna[3])]
                            nouDomini = []
                             #crea un nou domini per afegir tots els index del domini vell que satisfan la restricció
                            for index in range(len(domini)):
                                if D[v[1]][v[2]][restriccio[3]]== D[vna[1]][domini[index]][restriccio[1]]:
                                    nouDomini.append(domini[index])
                            DA[(vna[0],vna[3])] = nouDomini

    for domini in DA.values():
        if len(domini)==0:
            return False
    #DA[(v[0],v[3])] = [v[2]]
    return DA

def SeleccionarVariable(LVNA,DA):
    '''Retorna la variable amb el domini més petit'''
    minDom = 99999999
    for i in DA.keys():
        if len(DA[i])<minDom:
            minDom = len(DA[i])
            paraula = i
    for i in LVNA:
        if (i[0],i[3]) == paraula :
            LVNA.remove(i)
            return i

def Backtracking(LVA, LVNA, R, DA, D):
    '''Algoritme Backtracking'''
    if len(LVNA) == 0:
        return LVA
    var = SeleccionarVariable(LVNA,DA)
    for paraula in DA[(var[0],var[3])]:
        var[2]=paraula
        DAaux = dict(DA)
        del DAaux[(var[0],var[3])]
        DAaux = ActualitzarDominis(var, LVNA, R, DAaux, D)
        if(DAaux != False):
            LVA.append(var)
            res=Backtracking(LVA, LVNA, R, DAaux, D)
            if res != 0:
                return res
            LVA.remove(var)
        var[2]= -1
    LVNA.insert(0,var)
    return 0

if __name__ == "__main__":
    t1=0
    vegades = 1
    for i in range(0,vegades):
        t0 = time.clock()

        fitxer_dic = "diccionari_A.txt"
        fitxer_tau = "crossword_A.txt"
        diccionari = np.genfromtxt(fitxer_dic,dtype='S16')
        tauler = np.loadtxt(fitxer_tau, dtype='S16', comments='!')
        tauler.tostring()

        X = np.zeros(tauler.shape)
        Y = np.zeros(tauler.shape)
        construirVariablesHor(tauler, X)
        construirVariablesVer(tauler, Y)
        # print ("tauler")
        # print (X,"\n")
        # print (Y,"\n")
        variables = crearVariables(X,Y)

        #print ("Variables:\n",variables,"\n")
        restriccions = construirRestriccions(X,Y)
        #print ("Restriccions:\n",restriccions,"\n")
        dicc = construirDiccionari(diccionari)
        #print ("Dicc:\n",dicc,"\n")
        DA = construirDA(variables,dicc)
        #print ("DA:\n",DA,"\n")

        llistaBuida = []
        llista = Backtracking(llistaBuida,variables,restriccions,DA, dicc)
        #print ("Solucio:\n", llista)
        if llista != 0:
            sol = printaSolucio(X,Y,llista,dicc)
            #print ("Solucio:\n",sol)
            for element in sol:
                for elem in element:
                    print (elem, end="\t")

                print ("\n")
        print ("-----\t-------\t-------\t-------\t-------")
        t1 += (time.clock() - t0)
    final = t1/vegades
    print ("%.2f sec" % final)