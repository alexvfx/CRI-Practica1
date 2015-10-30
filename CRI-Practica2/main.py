__author__ = 'Marti, Alex, Alvaro'
# -*- coding: utf-8 -*-

#Instància --> fila
#Atribut --> columna

import numpy as np
import math as mt
import atribut as at
import instancia as ins

def BorrarInterrogants(data):
    """
    Funció que retorna la base de dades sense les instàncies que tenen '?'.
    :param data: Matriu de la base de dades.
    :return: Matriu de la base de dades actualitzada.
    """
    deleteIndex = []
    for i in range(len(data)):
        for element in data[i]:
            if element == '?' and i not in deleteIndex:
                deleteIndex.append(i)
    for i in range(len(deleteIndex)-1,-1,-1):
        data = np.delete(data, deleteIndex[i], axis=0)
    return data

def CrearInstancia(data,names,posobjectiu):
    """
    Funció que crea una llista amb les instàncies de la classe instància que tenim a la base de dades.
    :param data: Matriu de la base de dades.
    :param names: Noms dels diferents atributs de la base de dades.
    :param posobjectiu: Posició de la columna objectiu.
    :return: Una llista amb les instàncies.
    """
    instanceList = []
    for element in data:
        instance = ins.Instancia()
        instance.CrearLlistaInstancies(element,names,posobjectiu)
        instanceList.append(instance)
    return instanceList

def CrearAtributs(data):
    """
    Funció que crea una llista amb els atributs de la classe atribut que tenim a la base de dades.
    :param data: Matriu de la base de dades.
    :return: Una llista amb els atributs.
    """
    superList = []
    atributList = []
    j = 0
    while j < len(data[0]):
        mainList = []
        for element in data:
            mainList.append(element[j])
        superList.append(mainList)
        j += 1
    for element in superList:
        atribut = at.Atribut(element)
        atribut.NumeroVariables()
        atribut.TypeVariables()
        atributList.append(atribut)
    return atributList

def CalculateElements(atributs,instancies,index,posobjectiu):
    """
    Funció que calcula els valors d'objectiu que té cada element d'un atribut.
    :param atributs: Llista d'atributs.
    :param instancies: Llista d'instàncies
    :param index: Índex de l'atribut que volem calcular.
    :param posobjectiu: Posició de l'atribut objectiu.
    :return: Una llista de tuples amb les quantitats de cada element.
    """
    numList = []
    for element in atributs[index].TVariables:
        countP = 0
        countE = 0
        for x in instancies:
            if element[0] == x.AtributeList[index][0]:
                if x.ValorObjectiu == atributs[posobjectiu].TVariables[0][0]:
                    countP += 1
                if x.ValorObjectiu == atributs[posobjectiu].TVariables[1][0]:
                    countE += 1
        numList.append((countP, countE))
    return numList

def CalcularEntropiaGeneral(atribute):
    """
    Funció que calcula l'entropia de l'objectiu
    :param atribute: Atribut del qual volem calcular l'entropia
    :return: Valor de l'entropia
    """
    countE = atribute.TVariables[0][1]
    countP = atribute.TVariables[1][1]
    Entropia1 = (countE/(countE+countP))*(mt.log(countE/(countE+countP))/mt.log(2))
    Entropia2 = (countP/(countE+countP))*(mt.log(countP/(countE+countP))/mt.log(2))
    EntropiaGeneral = -(Entropia1 + Entropia2)
    return EntropiaGeneral

def CalcularEntropia(atributes,instances,posobjectiu):
    """
    Funció que calcula les entropies de cada atribut en relació amb l'atribut objectiu
    :param atributes: Llista d'atributs.
    :param instances: Llista d'instàncies.
    :param posobjectiu: Posició de l'atribut objectiu.
    :return: Llist amb els valors de les entropies.
    """
    j = 0
    EntropiesList = []
    while j < len(Atributs):
        if j == posobjectiu:
            j += 1
        else:
            elements = CalculateElements(atributes,instances,j,posobjectiu)
            i = 0
            ValorEntropia = 0
            while i < len(atributes[j].TVariables):
                Entr = -(atributes[j].TVariables[i][1]/len(instances))
                if elements[i][1] == 0 or elements[i][0] == 0:
                        Result = 0
                else:
                    Entropia1 = (elements[i][0]/atributes[j].TVariables[i][1])*(mt.log(elements[i][0]/atributes[j].TVariables[i][1])/mt.log(2))
                    Entropia2 = (elements[i][1]/atributes[j].TVariables[i][1])*(mt.log(elements[i][1]/atributes[j].TVariables[i][1])/mt.log(2))
                    Result = Entr*(Entropia1 + Entropia2)
                ValorEntropia += Result
                i += 1
            EntropiesList.append(ValorEntropia)
            j += 1
    return EntropiesList

def CalcularGuany(entropiaobjectiu,llistaentropies):
    """
    Funció que calcula els guanys de cada atribut.
    :param entropiaobjectiu: Valor de l'entropia de l'objectiu.
    :param llistaentropies: Llista amb els valors de les entropies.
    :return: Llista amb els guanys de cada atribut.
    """
    GuanysList = []
    for entropia in llistaentropies:
        Guany = entropiaobjectiu-entropia
        GuanysList.append(Guany)
    return GuanysList

def MillorAtribut(guanys,instancies):
    """
    Funció que troba el millor atribut.
    :param guanys: Llista de guanys.
    :param instancies: Llista d'instàncies.
    :return: Nom de l'atribut.
    """
    i = 0
    maxGain = 0
    maxGainID = 0
    while i < len(guanys):
        if guanys[i] > maxGain:
            maxGain = guanys[i]
            maxGainID = i
        i += 1
    return (maxGainID,instancies[0].AtributeList[maxGainID][1])

if __name__ == '__main__':

    # Data = np.loadtxt('agaricus-lepiota.data', dtype=str, delimiter=',')
    # Data = np.loadtxt('prova_db.data', dtype=str, delimiter=',')
    Data = np.loadtxt('mammals.data', dtype=str, delimiter=',')
    # Names = ["class","cap-shape","cap-surface","cap-color","bruises","odor","gill-attachment",
    #          "gill-spacing","gill-size","gill-color","stalk-shape","stalk-root","stalk-surface-above-ring",
    #          "stalk-surface-below-ring","stalk-color-above-ring","stalk-color-below-ring",
    #          "veil-type","veil-color","ring-number","ring-type","spore-print-color","population","habitat"]
    # Names = ["Objectiu","Herbivor","Interior"]
    Names = ["body temperature","gives birth","Four-legged","Hibernates","Mammal"]

    #Indicar en quina posició està l'atribut objectiu
    PosObjectiu = 4

    newData = BorrarInterrogants(Data)
    Atributs = CrearAtributs(newData)
    Instancies = CrearInstancia(newData,Names,PosObjectiu)

    EntropiaObjectiu = CalcularEntropiaGeneral(Atributs[PosObjectiu])
    Entropies = CalcularEntropia(Atributs,Instancies,PosObjectiu)
    Guanys = CalcularGuany(EntropiaObjectiu,Entropies)

    Atribut = MillorAtribut(Guanys,Instancies)

    print "ID Atribut:", Atribut[0]
    print "Nom Atribut:", Atribut[1]
