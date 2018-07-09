#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier appelant les fonctions permettant la récupération des données au format JSON
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#15/03/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import data_mining as dm
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import place as p
import computing as cp
###############################################################################


###############################################################################
#MAIN
###############################################################################
test=cp.compute_depArr('Mairie de Lille, Lille', 'Vieux Port, Marseille', [], 'driving')
test.to_csv('../../data/trajet_temoin.csv', sep=',', encoding='utf-8', index=False)
###############################################################################
