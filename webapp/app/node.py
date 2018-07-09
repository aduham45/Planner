#!/usr/bin/env python
# coding: utf-8 

###############################################################################
#Fichier contenant la classe node
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#15/06/2018
###############################################################################


###############################################################################
#OBJET
###############################################################################
class Node: 
    #CONSTRUCTEUR DE Node
    def __init__(self,city,score,parent,H,G):
        self.city = city #Id : int 
        self.score = score #Score : float
        self.parent = parent #Parent : Node
        self.H = H #H : int 
        self.G = G #G : int
        
    def get_city(self):
        return self.city
    
    def get_score(self):   
        return self.score
        
    def get_parent(self):
        return self.parent    
        
    def get_H(self):
        return self.H
        
    def get_G(self):
        return self.G
###############################################################################