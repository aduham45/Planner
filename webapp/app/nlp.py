#!/usr/bin/env python
# coding: utf-8 

###############################################################################
#Fichier contenant les fonctions permettant de créer la base de données de tags et similarités entre mots
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#05/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from nltk.corpus import wordnet
import csv
import numpy as np
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#prends deux mots en arguments et renvoie la mesure de similarité
def get_similarity(str1, str2):
    try:
        word1=wordnet.synsets(str1, 'n')[0]
        word2=wordnet.synsets(str2, 'n')[0]
        s=word1.wup_similarity(word2)
    except IndexError:
        s=0.0
    return(s)


#Création du csv contenant les similarités entre les mots contenus dans les tags
#Csv à importer dans la base de données
def similarities_toCsv(path_file, return_file):
    #Récupération du fichier des villes
    tags=np.genfromtxt(path_file, dtype=str)
    nSize=len(tags)
    #écriture dans le fichier contenant ID_tag1 | ID_Tag2 | Similarity
    with open(return_file, 'w') as csv_file:
        wr=csv.writer(csv_file)
        for i in range(0,nSize):
            for j in range(0,nSize):
                if(i <= j):
                    print(tags[i] + " "+ tags[j])
                    print(str(i) + " " + str(j) + " " + str(get_similarity(tags[i], tags[j])))
                    wr.writerow([i, j, get_similarity(tags[i], tags[j])])
   
    
#similaritiesToCsv('../data/tags.csv','../data/similaritiesTags.csv')
similarities_toCsv('../data/tags.csv','../data/similaritiesTags.csv')
###############################################################################
