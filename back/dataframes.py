#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#02/01/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import pandas as pd
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
"""
#Fonction permettant de mettre la table TYPE au format de DataFrame
def typesToDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT type.id, type.name FROM type', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table CITY au format de DataFrame
def citiesToDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT city.id, city.name, city.lat, city.lng FROM city', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table PLACE au format de DataFrame
def placesToDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT place.id, place.name, place.photo, place.type, place.visits, place.lat, place.lng, place.city_id FROM place', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table PARAMS au format de DataFrame
def paramsToDf(mode):
    connexion=db.init_db()
    qr="SELECT param.id,param.time, param.distance, param.heuristic, param.cityDep_id, param.cityArr_id FROM param WHERE param.mode LIKE " + mode
    results=pd.read_sql(qr, connexion, index_col='id')
    return results


#Fonction permettant de mettre la table SIMILARITY au format de DataFrame
def similaritiesToDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT similarity.id, similarity.type_id1, similarity.type_id2, similarity.similarity FROM similarity', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table PLACETYPE au format de DataFrame
def placeTypesToDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT placeTypes.place_id, placeTypes.word FROM placeTypes', connexion)
    return results
"""

#Fonction permettant de mettre la table TYPE au format de DataFrame
def typesToDf():
    results=pd.read_csv('../data/tags.csv', names=['name'])
    return results


#Fonction permettant de mettre la table CITY au format de DataFrame
def citiesToDf():
    results=pd.read_csv('../data/cities.csv', names=['id', 'name', 'lat', 'lng'], encoding='latin-1')
    return results


#Fonction permettant de mettre la table PLACE au format de DataFrame
def placesToDf():
    results=pd.read_csv('../data/all_places.csv', names=['id', 'name', 'photo', 'type', 'visits', 'lat', 'lng', 'city_id'])
    results
    return results


#Fonction permettant de mettre la table PARAMS au format de DataFrame
def paramsToDf(mode):
    results=pd.read_csv('../data/params.csv', names=['mode', 'time', 'distance', 'heuristic', 'cityDep_id', 'cityArr_id'])
    results=results.loc[results['mode']==mode]
    results=results.iloc[:,1:]
    return results


#Fonction permettant de mettre la table SIMILARITY au format de DataFrame
def similaritiesToDf():
    results=pd.read_csv('../data/similaritiesTags.csv', names=['type_id1', 'type_id2', 'similarity'])
    return results


#Fonction permettant de mettre la table PLACETYPE au format de DataFrame
def placeTypesToDf():
    results=pd.read_csv('../data/placeTags.csv', names=['place_id', 'word'])
    return results

placesToDf()
###############################################################################