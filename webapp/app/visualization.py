#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les fonction permettant de visualiser les données
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#05/01/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import dataframes
import networkx as nx
import matplotlib.pyplot as plt
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
def ways_visualization(df):
    G=nx.from_pandas_edgelist(df, source='cityDep_id', target='cityArr_id', edge_attr='distance')
    nx.draw(G, with_labels=True, node_color='g', alpha=0.7, node_size=500, width=0.1,edge_color='g')
    plt.show()

ways_visualization(dataframes.paramsToDf("'driving'"))
###############################################################################