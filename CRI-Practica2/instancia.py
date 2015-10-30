__author__ = 'Marti, Alex, Alvaro'
# -*- coding: utf-8 -*-

class Instancia(object):
    def __init__(self):
        self.AtributeList = []
        self.ValorObjectiu = None

    def CrearLlistaInstancies(self, Instance, Names, Objectiu):
        AtributesList = []
        self.ValorObjectiu = Instance[Objectiu]
        i = 0
        while i < len(Instance):
            AtributesList.append([Instance[i],Names[i]])
            i += 1
        self.AtributeList = AtributesList