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
sc = pyspark.SparkContext.getOrCreate()
conf = pyspark.SparkConf()
conf.setAppName('SmartPlanner')
conf.setMaster('spark://10.2.68.52:7077')
#conf.setMaster('local[*]')
conf.set('spark.executor.memory', '10g')
conf.set('spark.executor.cores', '3')
conf.set('spark.cores.max', '9')
conf.set('spark.logConf', True)
sc.stop()
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession(sc)
spark.catalog.clearCache()
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
windowSpec = Window.orderBy("ind")
df_cities=dtf.citiesToDf()
df_types=dtf.typesToDf()
df_placeTypes=dtf.placeTypesToDf()
df_similarities=dtf.similaritiesToDf()
df_places=dtf.placesToDf()
sc_places=spark.createDataFrame(df_places)
user_tags=[]
d={'Visits':[]}
df_visits=pd.DataFrame(data=d)
d={'City_id':[]}
df_city=pd.DataFrame(data=d)
df_types=dtf.typesToDf()
#n=len(tab_tags)
n_pT=len(df_placeTypes)
#Ajout des city_id à la matrice
#Ajout du nombre de visites à la matrice
for i in range(0,n_pT):
    place_id=df_placeTypes.iloc[i]['place_id']
    city_id=df_places.loc[place_id, 'city_id']
    df_city=df_city.append({'City_id': city_id}, ignore_index=True)
    visits=df_places.loc[place_id, 'visits']
    df_visits=df_visits.append({'Visits': visits}, ignore_index=True)
df_placeTypes=pd.concat([df_placeTypes, df_city], axis=1)
df_placeTypes=pd.concat([df_placeTypes, df_visits], axis=1)
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant de retourner une Dataframe avec les distances, temps entre les villes avec le lieu de départ et d'arrivée de l'utilisateur
def computeDepArr(addDep, addArr, wayPoints, mode): 
    #Récupération des coordonnées depuis les adresses fournies
    coordDep=dm.getGps(addDep)
    coordArr=dm.getGps(addArr)
    rows=[]
    temp=len(wayPoints)
    #Récupération de la dataframe contenant les villes
    cities=dtf.citiesToDf()
    nSize=len(cities)
    #Appel de la fonction permettant de calculer la distance d'un point à tous les autres
    for i in range(0,nSize):
        #Obtention des paramètres depuis le lieu de départ 
        distDuree=dm.getDistance_Duree(coordDep[0], coordDep[1], str(cities.iloc[i][1]), str(cities.iloc[i][2]), mode)
        rows.append([distDuree[1], distDuree[2], distDuree[3], 1000, i])
        #Obtention des paramètres depuis le lieu d'arrivée 
        distDuree=dm.getDistance_Duree(coordArr[0], coordArr[1], str(cities.iloc[i][1]), str(cities.iloc[i][2]), mode)
        rows.append([distDuree[1], distDuree[2], distDuree[3], 10000, i])
        if(temp>0):
            print("Waypoints with cities")
            #Obtention des paramètres depuis les Waypoints
            for j in range(0,temp):
                coordWayp=dm.getGps(wayPoints[j])
                #Pour toutes les villes
                distDuree=dm.getDistance_Duree(coordWayp[0], coordWayp[1], str(cities.iloc[i][1]), str(cities.iloc[i][2]), mode)
                rows.append([distDuree[1], distDuree[2], distDuree[3], 100000+j, i])
    if(temp>0):
        print("Waypoints with start and arrival")
        #Obtention des paramètres depuis les Waypoints
        for j in range(0,temp):
            #Depuis le départ
            distDuree=dm.getDistance_Duree(coordWayp[0], coordWayp[1], coordDep[0], coordDep[1], mode)
            rows.append([distDuree[1], distDuree[2], distDuree[3], 1000, 100000+j])
            #Depuis l'arrivée
            distDuree=dm.getDistance_Duree(coordWayp[0], coordWayp[1], coordArr[0], coordArr[1], mode)
            rows.append([distDuree[1], distDuree[2], distDuree[3], 10000, 100000+j])
    print("Start - Arrival")
    #Calcul des paramètres entre le départ et l'arrivée
    distDuree=dm.getDistance_Duree(coordDep[0], coordDep[1], coordArr[0], coordArr[1], mode)
    rows.append([distDuree[1], distDuree[2], distDuree[3], 1000, 10000])
    df1=pd.DataFrame(rows, columns=['time', 'distance', 'heuristic', 'cityDep_id', 'cityArr_id'])
    #Retourne la nouvelle DataFrame
    return(df1)

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
def scoreTotal(simi, visits):
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
def getClassement(df_placeTypes, tab_tags):
    #Init fonction udf
    n=len(tab_tags)
    udfScoreTotal=udf(scoreTotal, FloatType())
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
    sc_placeTypes=spark.createDataFrame(df_placeTypes)
    scoreTable=[]
    for i in range(0,n):
        col=tab_tags[i]
        temp=sc_placeTypes.groupBy('place_id', 'City_id', 'Visits').agg({col: 'mean'})
        temp=temp.withColumn('Score',udfScoreTotal('avg('+col+')', 'Visits'))
        temp=temp.groupBy('City_id').agg({'Score': 'mean'})
        temp.orderBy('avg(Score)', ascending=False)
        #Liste de dataframe où sont conservés les classements par score
        scoreTable.append(temp)
        #Matrice du Score total obtenu par chaque ville
        if(i==0):
            overallScore=temp
        elif(i>0):
            overallScore=overallScore.union(temp)
    overallScore=overallScore.groupBy('City_id').agg({'avg(Score)': 'mean'})
    overallScore=overallScore.orderBy('avg(avg(Score))', ascending=False)
    overallScore=overallScore.filter(overallScore.City_id <= 60)
    #retourne le classement des villes
    return [overallScore, scoreTable]  


#Renvoi de la liste de villes recommandée en fonction des choix de l'utilisateur
def getWay(tab_tags, df_overallScore, n):
    list_steps=[]
    for i in range(0,n):
        city_id=df_overallScore.iloc[i , 0]
        city_name=df_cities.loc[[city_id], 'name']
        list_steps.append([city_name.values[0], df_overallScore.loc[[i], 'avg(avg(Score))'].values[0]])
    return list_steps


#t=getClassement(df_placeTypes, tab_tags)[0].toPandas()
#test=getWay(tab_tags, getClassement(df_placeTypes, tab_tags)[0].toPandas(), 5)
#print(test)
    

#CONSTRUCTION DE LA MATRICE PERMETTANT DE CALCULER LES GRAPHES
"""
_______________________________________________________________________________
time | distance | heuristic | cityDep_id | cityArr_id | ScoreCity1 | ScoreCity2
_____|__________|___________|____________|____________|____________|___________"""
def getGraphMatrix(add_dep, add_arr, waypoint, mode):
    #df_test=computeDepArr(add_dep, add_arr, waypoint, 'driving')
    df_test=pd.read_csv('../data/trajet_temoin.csv').astype(int)
    df_params=dtf.paramsToDf("'driving'")
    df_params=pd.concat([df_params, df_test], axis=0)
    df_params.append(df_test)
    #Spark Dataframe avec le score de chaque ville
    overallScore=getClassement(df_placeTypes)[0]
    #Boucle dans chaque ligne pour affilier un score à chaque ville
    df_overallScore=overallScore.toPandas()
    df_overallScore
    list_scoreDep=[]
    list_scoreArr=[]
    for index, row in df_params.iterrows():
        cityDep_id=row['cityDep_id']
        cityArr_id=row['cityArr_id']
        #Recherche du score sur la ville de départ
        if(cityDep_id==1000 or cityDep_id==10000 or cityDep_id==100000):
            list_scoreDep.append(0)
        else:
            score=df_overallScore.loc[(df_overallScore['City_id']==cityDep_id), 'avg(avg(Score))']
            if(list(score) != []):
                list_scoreDep.append(list(score)[0])
            else:
                list_scoreDep.append(0)
        #Recherche du score sur la ville d'arrivée
        if(cityArr_id==1000 or cityArr_id==10000 or cityArr_id==100000):
            list_scoreArr.append(0)
        else:
            score=df_overallScore.loc[(df_overallScore['City_id']==cityArr_id), 'avg(avg(Score))']
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
    sc_params=spark.createDataFrame(df_params)
    return sc_params
###############################################################################
    
#sc_params=getGraphMatrix(add_dep, add_arr, waypoint, 'driving')