#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les fonction permettant de réaliser les calculs de trajet
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#05/01/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import pandas as pd
import numpy as np
import data_mining as dm
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import IntegerType
from pyspark.sql.types import FloatType
from pyspark.sql.window import Window
from pyspark.sql import functions as F
from pyspark.sql.functions import udf
from math import log
import pyspark
import dataframes as dtf
###############################################################################


###############################################################################
#Création du spark context
###############################################################################

def get_spark_context():
    sc = pyspark.SparkContext.getOrCreate()
    conf = pyspark.SparkConf()
    conf.setAppName('SmartPlanner')
    #conf.setMaster('spark://10.2.68.52:7077')
    conf.setMaster('local[*]')
    conf.set('spark.executor.memory', '8g')
    conf.set('spark.executor.cores', '3')
    conf.set('spark.cores.max', '9')
    conf.set('spark.logConf', True)
    sc.stop()
    sc = pyspark.SparkContext(conf=conf)
    spark = SparkSession(sc)
    spark.catalog.clearCache()
    return spark

###############################################################################


###############################################################################
#TESTS
###############################################################################
#tab_tags=['Art', 'Site', 'Museum', 'Gallery']
#waypoint=['Amiens']
#add_dep='Lille'
#add_arr='Marseille'
###############################################################################


###############################################################################
#IMPORT DES MATRICES DE DONNEES SOUS FORME DE DataFrames
###############################################################################
#Récupération de la matrice de types sous forme de dataframe
#df_types=dtf.typesToDf()
#Spark DataFrame
#df_types=spark.createDataFrame(df_types)
#Récupération de la matrice de similarité sous forme de dataframe
#df_similarities=dtf.similaritiesToDf()
#Spark DataFrame
#df_similarities=spark.createDataFrame(df_similarities)
#Récupération de la matrice de placeTypes sous forme de dataframe
#df_placeTypes=dtf.placeTypesToDf()
#Spark DataFrame
#df_placeTypes=spark.createDataFrame(df_placeTypes)
#Récupération de la matrice de placesSimilarity sous forme de dataframe
#Spark DataFrame
#placesSimilarities=spark.read.format('csv').option('header', 'true').load('../data/placesSimilarities.csv')
def init_matrix():
    df_cities=dtf.cities_toDf()
    df_types=dtf.types_toDf()
    df_placeTypes=dtf.placeTypes_toDf()
    df_similarities=dtf.similarities_toDf()
    df_places=dtf.places_toDf()
    d={'Visits':[]}
    df_visits=pd.DataFrame(data=d)
    d={'City_id':[]}
    df_city=pd.DataFrame(data=d)
    df_types=dtf.types_toDf()
    #n=len(tab_tags)
    n_pT=len(df_placeTypes)
    #Ajout des city_id à la matrice
    #Ajout du nombre de visites à la matrice
    for i in range(0,n_pT):
        place_id=df_placeTypes.iloc[i]['place_id']
        city_id=df_places.loc[df_places['id']==place_id, 'city_id'].values[0]
        df_city=df_city.append({'City_id': city_id}, ignore_index=True)
        visits=df_places.loc[df_places['id']==place_id, 'visits'].values[0]
        df_visits=df_visits.append({'Visits': visits}, ignore_index=True)
    df_placeTypes=pd.concat([df_placeTypes, df_city], axis=1)
    df_placeTypes=pd.concat([df_placeTypes, df_visits], axis=1)
    return [df_cities, df_types, df_placeTypes, df_similarities, df_places]
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant de retourner une Dataframe avec les distances, temps entre les villes avec le lieu de départ et d'arrivée de l'utilisateur
def compute_depArr(addDep, addArr, waypoints, mode): 
    #Récupération des coordonnées depuis les adresses fournies
    coord_dep=dm.get_gps(addDep)
    coord_arr=dm.get_gps(addArr)
    rows=[]
    temp=len(waypoints)
    #Récupération de la dataframe contenant les villes
    cities=dtf.cities_toDf()
    n_size=len(cities)
    #Appel de la fonction permettant de calculer la distance d'un point à tous les autres
    for i in range(0,n_size):
        #Obtention des paramètres depuis le lieu de départ 
        dist_duree=dm.get_distance_duree(coord_dep[0], coord_dep[1], str(cities.iloc[i][2]), str(cities.iloc[i][3]), mode)
        rows.append([dist_duree[1], dist_duree[2], dist_duree[3], 1000, i+1])
        #Obtention des paramètres depuis le lieu d'arrivée 
        dist_duree=dm.get_distance_duree(coord_arr[0], coord_arr[1], str(cities.iloc[i][2]), str(cities.iloc[i][3]), mode)
        rows.append([dist_duree[1], dist_duree[2], dist_duree[3], 10000, i+1])
        if(temp>0):
            #Obtention des paramètres depuis les Waypoints
            for j in range(0,temp):
                coord_wayp=dm.get_gps(waypoints[j])
                #Pour toutes les villes
                dist_duree=dm.get_distance_duree(coord_wayp[0], coord_wayp[1], str(cities.iloc[i][2]), str(cities.iloc[i][3]), mode)
                rows.append([dist_duree[1], dist_duree[2], dist_duree[3], 100000+j, i+1])
    if(temp>0):
        #Obtention des paramètres depuis les Waypoints
        for j in range(0,temp):
            #Depuis le départ
            dist_duree=dm.get_distance_duree(coord_wayp[0], coord_wayp[1], coord_dep[0], coord_dep[1], mode)
            rows.append([dist_duree[1], dist_duree[2], dist_duree[3], 1000, 100000+j])
            #Depuis l'arrivée
            dist_duree=dm.get_distance_duree(coord_wayp[0], coord_wayp[1], coord_arr[0], coord_arr[1], mode)
            rows.append([dist_duree[1], dist_duree[2], dist_duree[3], 10000, 100000+j])
    #Calcul des paramètres entre le départ et l'arrivée
    dist_duree=dm.get_distance_duree(coord_dep[0], coord_dep[1], coord_arr[0], coord_arr[1], mode)
    rows.append([dist_duree[1], dist_duree[2], dist_duree[3], 1000, 10000])
    df1=pd.DataFrame(rows, columns=['time', 'distance', 'heuristic', 'cityDep_id', 'cityArr_id'])
    #Retourne la nouvelle DataFrame
    return(df1)
    
"""temp = compute_depArr('Lille', 'Marseille', ['Grenoble'], 'driving')    
with open('trajet_temoin.csv', 'w') as csv_file:
    temp.to_csv(csv_file)"""

"""
#Fonction permettant de mesurer la similarité entre 2 places
def getSimilarity(id_place1, id_place2):
    score=0.0
    #Récupération des tag_id de chaque place    
    words1=df_placeTypes[df_placeTypes.place_id==id_place1]['word']
    words2=df_placeTypes[df_placeTypes.place_id==id_place2]['word']
    #Récupération du nombre de tag par id 
    nb1=len(words1)
    nb2=len(words2)
    nb_ind=nb1+nb2
    for i in range(0,nb1):
        for j in range(0, nb2):
            result=df_similarities[((df_similarities.type_id1==words1.iloc[i]) & (df_similarities.type_id2==words2.iloc[j]))^((df_similarities.type_id1==words2.iloc[j]) & (df_similarities.type_id2==words1.iloc[i]))]['similarity']
            if(words1.iloc[i]!=words2.iloc[j]):
                score=score+result.iloc[0]
            else:
                score=score+1
            #print(score)
    return score/nb_ind
"""

"""
#Fonction permettant de mesurer la similarité entre les TAGS UTILISATEURS ET TOUTES LES PLACES
def getSimilarityUsersPlaces(df_tags, df_placesTypes_ind):
    list_final=[]
    for i in range(1, df_tags.count()+1):
        #Select tag_id 
        tag_user=df_tags.where(df_tags.id==i).select('value').collect()
        print("TAG USER : "+tag_user)
        for j in range(1, df_placesTypes_ind.count()+1):
            #Select place id
            event_id=df_placesTypes_ind.where(df_placesTypes_ind.ind==j).select('place_id').collect()[0]
            #Select Tags for each place
            tags_place=df_placesTypes_ind.where(df_placesTypes_ind.place_id==event_id['place_id']).select('word')
            tags_place=tags_place.withColumn('id', monotonically_increasing_id())
            windowSpec = Window.orderBy("id")
            tags_place=tags_place.withColumn("id", F.row_number().over(windowSpec))
            #Créer une dataframe avec la similarité de chaque event avec chaque tag
            score=0.0
            for k in range (1, tags_place.count()+1):
                temp=tags_place.where(tags_place.id==k).select('word').collect()
                print("TAG PLACE : "+temp)
                simi=df_similarities.where(((df_similarities.type_id1==tag_user[0][0])&(df_similarities.type_id2==temp[0][0]))|((df_similarities.type_id2==tag_user[0][0])&(df_similarities.type_id1==temp[0][0]))).select('similarity').collect()
                score=score+simi[0]['similarity']
            print("SCORE : "+ score)
            list_final.append([tag_user, event_id['place_id'], score/df_tags.count()])    
    return 0
"""

"""
#Fonction créant la matrice de similarité entre les évenements
def placesSimilarities():
    #Création de la DataFrame carrée avec des similarités de 0
    temp=df_placeTypes['place_id'].unique()
    print(len(temp))
    df_sim=pd.DataFrame(np.zeros((len(temp),len(temp))), columns=list(temp), index=list(temp))
    #Boucle peuplant la matrice avec les similarités calculées
    for i in range(1, len(temp)):
        for j in range(1, len(temp)):
            #évite de recommander le même point d'intéret
            if(i!=j):
                print(temp[i]+", "+temp[j]+" : "+str(getSimilarity(temp[i], temp[j])))
                df_sim.loc[[temp[i]],[temp[j]]]=getSimilarity(temp[i], temp[j])
    df_sim.to_csv('../data/placesSimilarities.csv', sep=',', encoding='utf-8')
    return(df_sim)
"""

"""
#Fonction permettant de lire les Tags données par l'utilisateur 
def computeRecommandation(tab_tags):
    #Passage en SparkDataframes
    #Nombre de tags saisis par l'utilisateur
    user_tags=[]
    nSize=len(tab_tags)
    #CONSTRUCTION DE LA MATRICE DE SIMILARITE ENTRE LES EVENEMENTS
    #Récupération des id de tags choisis par l'utilisateur
    for i in range(0, nSize):
        user_tags.append(int(df_types.index[df_types.name==tab_tags[i]].get_values()[0]))
    #Ajout d'index dans la dataframe des tags
    user_tags_df=spark.createDataFrame(user_tags, IntegerType())
    user_tags_df=user_tags_df.withColumn('id', monotonically_increasing_id())
    windowSpec = Window.orderBy("id")
    user_tags_df=user_tags_df.withColumn("id", F.row_number().over(windowSpec))
    user_tags_df.cache()
    #Ajout d'index dans la dataframe de placeTypes
    df_placeTypes_ind=spark.createDataFrame(df_placeTypes)
    df_placeTypes_ind=df_placeTypes_ind.withColumn('ind', monotonically_increasing_id())
    windowSpec = Window.orderBy("ind")
    df_placeTypes_ind=df_placeTypes_ind.withColumn("ind", F.row_number().over(windowSpec))
    df_placeTypes_ind.cache()
    getSimilarityUsersPlaces(user_tags_df,df_placeTypes_ind)
    return 0
"""


#Fonction utilisée pour UDF matrix
#Score = similarité + log(nombre de visites)
def score_total(simi, visits):
    if(visits >= 1):
        return(simi + (log(visits)/2))
    else:
        return(simi)


#CONSTRUCTION DE LA MATRICE DE SIMILARITE ENTRE LES EVENEMENTS
#Récupération des id de tags choisis par l'utilisateur
"""
_________________________
City_id | avg(avg(Score))
________|________________"""
"""
_________________________
place_id | avg(avg(Score))
_________|_______________"""
def get_classement(df_placeTypes, tab_tags, df_types, df_similarities, df_cities):
    #Init fonction udf
    user_tags=[]
    n_pT=len(df_placeTypes)
    n=len(tab_tags)
    #Mesure de similarités avec les points d'intérêts
    for i in range(0, n):
        user_tags.append(int(df_types.index[df_types.name==tab_tags[i]].get_values()[0]))
    for i in range(0, n):
        d={tab_tags[i]:[]}
        df=pd.DataFrame(data=d)
        #Select tag_id 
        tag_user=user_tags[i]
        #Création d'une dataframe d'une seule colonne de nom tag_id
        for j in range(0, n_pT):   
            #Ajouter une colonne de calcul de similarité pour chaque tag 
            temp=int(df_placeTypes.loc[j]['word'])
            if(tag_user<temp):
                simi=df_similarities.loc[(df_similarities['type_id1']==tag_user)&(df_similarities['type_id2']==temp), 'similarity'].values[0]
            elif(tag_user==temp):
                simi=1.0
            elif(tag_user>temp):
                simi=df_similarities.loc[(df_similarities['type_id2']==tag_user)&(df_similarities['type_id1']==temp), 'similarity'].values[0]
            df=df.append({tab_tags[i]: simi}, ignore_index=True)
        df_placeTypes=pd.concat([df_placeTypes, df], axis=1)
    #Computation du classement des villes  
    #Correspond aux colonnes Score par 'tag'
    temp=df_placeTypes.iloc[:,4:]
    max_val=df_placeTypes['Visits'].apply(np.log).max()
    df_placeTypes['Score']=(temp.sum(axis=1)/n + df_placeTypes['Visits'].apply(np.log))/(max_val+1)
    overall_score=df_placeTypes.groupby('City_id')['Score'].mean().reset_index()
    overall_score=overall_score.sort_values('Score', ascending=False).reset_index().drop(['index'], axis=1)
    score_table=df_placeTypes.groupby('City_id').mean().sort_values('Score', ascending=False).reset_index().drop(['word', 'Visits'], axis=1)
    score_table=score_table.iloc[:50,:]
    return [overall_score, score_table]  


#Renvoi de la liste de villes recommandée en fonction des choix de l'utilisateur
def get_way(tab_tags, df_overall_score, n, df_cities):
    list_steps=[]
    for i in range(0,n):
        city_id=df_overall_score.iloc[i , 0]
        city_name=df_cities.loc[[city_id-1], 'name']
        list_steps.append([city_name.values[0], df_overall_score.loc[[i], 'Score'].values[0]])
    return list_steps


#CONSTRUCTION DE LA MATRICE PERMETTANT DE CALCULER LES GRAPHES
"""
______________________________________________________
time | distance | heuristic | cityDep_id | cityArr_id 
_____|__________|___________|____________|____________"""
def get_graph_matrix(add_dep, add_arr, waypoint, mode, overall_score):
    df_test=compute_depArr(add_dep, add_arr, waypoint, 'driving')
    #df_test=pd.read_csv('../static/data/trajet_temoin.csv')
    #df_test=df_test.iloc[:,1:]
    #print(df_test)
    df_params=dtf.params_toDf(mode)
    df_params=pd.concat([df_params, df_test], axis=0)
    #df_params.append(df_test)
    #Dataframe avec le score de chaque ville
    #Boucle dans chaque ligne pour affilier un score à chaque ville
    df_overall_score=overall_score
    list_scoreDep=[]
    list_scoreArr=[]
    for index, row in df_params.iterrows():
        cityDep_id=row['cityDep_id']
        cityArr_id=row['cityArr_id']
        #Recherche du score sur la ville de départ
        if(cityDep_id==1000 or cityDep_id==10000 or cityDep_id==100000):
            list_scoreDep.append(0)
        else:
            score=df_overall_score.loc[(df_overall_score['City_id']==cityDep_id), 'Score']
            if(list(score) != []):
                list_scoreDep.append(list(score)[0])
            else:
                list_scoreDep.append(0)
        #Recherche du score sur la ville d'arrivée
        if(cityArr_id==1000 or cityArr_id==10000 or cityArr_id==100000):
            list_scoreArr.append(0)
        else:
            score=df_overall_score.loc[(df_overall_score['City_id']==cityArr_id), 'Score']
            if(list(score) != []):
                list_scoreArr.append(list(score)[0])
            else:
                list_scoreArr.append(0)
    df_scoreDep=pd.DataFrame(list_scoreDep, columns=['ScoreCity1'])
    df_scoreArr=pd.DataFrame(list_scoreArr, columns=['ScoreCity2'])
    df_params=df_params.reset_index(drop=True)
    df_scoreDep=df_scoreDep.reset_index(drop=True)
    df_scoreArr=df_scoreArr.reset_index(drop=True)
    df_params=pd.concat([df_params, df_scoreDep, df_scoreArr], axis=1, join='inner')
    #sc_params=spark.createDataFrame(df_params)
    out=df_params
    return out
###############################################################################