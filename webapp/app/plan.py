#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les fonction de planification
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#juin 2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from computing import get_graph_matrix, init_matrix, get_classement
import pandas as pd
from node import *
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Obtenir tous les enfants d'un noeud parent
"""
    IN : 
        node : noeud père
        df : matrice de données graphe (get_graph_matrix)
        overallScore : Dataframe city_id - score
        target : noeud cible
        optimization : Type d'otpimisation 'distance', 'time', 'affinity'
        filtre : Matrice 'df' filtrée par les conditions utilisateur
        distance_begin : distance réelle cumulée     
    OUT : 
        liste de nodes  
"""
def children(node, df, overallScore, target, optimization, filtre, distance_begin):
    children=[]
    d1=filtre.loc[filtre['cityDep_id']==node.city]['cityArr_id']
    d2=filtre.loc[filtre['cityArr_id']==node.city]['cityDep_id']
    d2=pd.concat([d1, d2])
    temp=d2.values[:]
    #Renvoie un tableau de noeuds
    for value in temp : 
        if(value != target.city):
            try:
                score=overallScore.loc[overallScore['City_id']==value]['Score'].values[0]
                parent=node
                H=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))]['heuristic'].values[0]
                G=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))][optimization].values[0]+distance_begin
                child=Node(value,score,parent,H,G)
                children.append(child)
            except:
                score=0
                parent=node
                #print(value, target.city)
                H=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))]['heuristic'].values[0]
                G=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))][optimization].values[0]+distance_begin
                child=Node(value,score,parent,H,G)
                children.append(child) 
        else : 
            children.append(target)
    return children


#Obtenir le noeud suivant en fonction de G et H 
"""
    IN : liste de nodes
    OUT : node
"""
def get_best_child(liste):
    for i in range(0, len(liste)):
        for j in range(i+1, len(liste)):
            x1=liste[i].H
            y1=liste[i].G
            x2=liste[j].H
            y2=liste[j].G
            if((x1+y1)>(x2+y2)):
                tmp=liste[i]
                liste[i]=liste[j]
                liste[j]=tmp
    return(liste[0])
 
    
#Obtenir le chemin optimal
"""
    IN : 
        start : node
        target : node
        df : matrice de données graphe (get_graph_matrix)
        overallScore : Dataframe city_id - score
        optimization : Type d'otpimisation 'distance', 'time', 'affinity'
        filtre : Matrice 'df' filtrée par les conditions utilisateur
    OUT :    
"""
def get_path(start, target, df, overallScore, optimization, filtre, df_cities, add_dep, add_arr, waypoint):
    """stack=[]
    result_id=[]
    stack.append(start)
    pere=start
    tmp=0
    distance_begin=0
    while(tmp!=target.city):
        x=children(pere, df, overallScore, target, 'distance',filtre, distance_begin)
        #########################
        temp=x
        for node_s in stack:
            for node_c in x:
                if(node_s.city==node_c.city):
                    temp.remove(node_c)
        #########################
        child=get_best_child(temp)
        stack.append(child)
        pere=child
        print(child.city)
        tmp=stack[-1].city
        distance_begin += pere.G
    for obj in stack:
        result_id.append(obj.city)
    result_names=[]
    for obj in result_id:
        if(obj<100):
            result_names.append([df_cities.iloc[int(obj)-1]['name'], overallScore.loc[overallScore['City_id']==obj]['Score'].values[0]])
        elif(obj==1000):
            result_names.append([add_dep, 0])
        elif(obj==10000):
            result_names.append([add_arr, 0]) 
    return result_names"""
    result_names=[]    
    stack=[]
    result_id=[]
    stack.append(start)
    pere=start
    tmp=0
    distance_begin=0
    for k in 0,len(waypoint):
        if k<len(waypoint):
            #index des waypoints
            target_id=100000+k
            next_target=Node(target_id, 0, None, 0, 0)
            print("WAYPOINT")
        elif k==len(waypoint):
            next_target=target
            print("FINAL")
        while(tmp!=next_target.city):
            x=children(pere, df, overallScore, next_target, 'distance', filtre, distance_begin)
            temp=x
            for node_s in stack:
                for node_c in x:
                    if(node_s.city==node_c.city):
                        temp.remove(node_c)
            child=get_best_child(temp)
            stack.append(child)
            pere=child
            tmp=stack[-1].city
            distance_begin += pere.G
    for obj in stack:
        result_id.append(obj.city)
    ###########################################################################
    for obj in result_id:
        if(obj<100):
            result_names.append([df_cities.iloc[int(obj)-1]['name'], overallScore.loc[overallScore['City_id']==obj]['Score'].values[0]])
        elif(obj==1000):
            result_names.append([add_dep, 0])
        elif(obj==10000):
            result_names.append([add_arr, 0])
        elif(obj >= 100000): 
            idx=obj-100000
            result_names.append([waypoint[idx], 0])
    return result_names


"""datas=init_matrix()
tags=['Art', 'Museum']
overall_score = get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0]
start=Node(1000, 0, None, 0, 0)
target=Node(10000, 0, None, 0, 0)
add_dep='Saint-Nazaire'
add_arr='Marseille'
escale=[]
t_max=7200
d_max=300000
mode='driving'
optimisation='distance'
dtfr=get_graph_matrix(add_dep, add_arr, escale, mode, overall_score)

df_filtered = dtfr.loc[dtfr['distance'] < d_max]
print(get_path(start, target, dtfr, overall_score, optimisation, df_filtered, datas[0], add_dep, add_arr, escale))"""

###############################################################################