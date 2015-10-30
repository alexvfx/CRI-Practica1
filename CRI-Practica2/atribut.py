__author__ = 'Marti, Alex, Alvaro'
# -*- coding: utf-8 -*-

class Atribut(object):
    def __init__(self, ElementList):
        self.ElementList = ElementList
        self.NumVariables = 0
        self.TVariables = []

    def NumeroVariables(self):
        ListElement = []
        for element in self.ElementList:
            if element not in ListElement:
                ListElement.append(element)
        self.NumVariables = len(ListElement)

    def TypeVariables(self):
        VariablesList = []
        for element in range(self.NumVariables):
            VariablesList.append([])
        for x in self.ElementList:
            i = 0
            while i < self.NumVariables:
                if x in VariablesList[i]:
                    VariablesList[i].append(x)
                    i = self.NumVariables
                else:
                    if VariablesList[i] == []:
                        VariablesList[i].append(x)
                        i = self.NumVariables
                    else:
                        i += 1
        for element in VariablesList:
            self.TVariables.append((element[0], float(len(element))))