__author__ = 'marti'
# -*- coding: utf-8 -*-

#1 -> horitzontal
#2 -> vertical

import numpy as np
np.set_printoptions(precision=2)

fitxer_dic = "diccionari_CB.txt"
fitxer_tau = "crossword_CB.txt"
diccionari = np.genfromtxt(fitxer_dic,dtype='str')
tauler = np.loadtxt(fitxer_tau, dtype='|S16', comments='!')
tauler.tostring()

print tauler

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

def Backtracking_Alt(LVA, LVNA, R, D):
    if LVNA == []:
        return LVA
    Variable = LVNA[0]
    for Paraula in D[Variable[1]]:
        Variable[2] = Paraula
        Satisfa = SatisfaRestriccions(Variable, LVA, R)
        if Satisfa == True:
            LVA.append(Variable)
            del LVNA[0]
            Result = Backtracking_Alt(LVA, LVNA, R, D)
            if Result:
                return Result
            else:
                mal = LVA.pop()
                LVNA.insert(0,mal)
        Variable[2] = ''
    return None

D = construirDiccionari(diccionari)
print D
LVNA = [[1.0, 6, '', 1], [4.0, 4, '', 1], [5.0, 5, '', 1],
        [6.0, 5, '', 1], [1.0, 4, '', 2], [5.0, 2, '', 2],
        [2.0, 6, '', 2], [3.0, 5, '', 2]]
LVA = []
R = [[1.0, 0, 1.0, 0], [1.0, 3, 2.0, 0], [1.0, 5, 3.0, 0], [4.0, 1, 2.0, 2], [4.0, 3, 3.0, 2],
     [5.0, 0, 5.0, 0], [5.0, 2, 2.0, 4], [5.0, 4, 3.0, 4], [6.0, 1, 5.0, 1], [6.0, 3, 2.0, 5]]
print Backtracking_Alt(LVA,LVNA,R,D)