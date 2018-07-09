#!/usr/bin/env python
#  coding: utf-8 

###############################################################################
#Fichier contenant les fonctions permettant la récupération des données au format JSON
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#15/03/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import json
import csv
import time
import requests
import place as p
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
#from pyspark.sql import SQLContext
#from pyspark.sql.functions import explode
from math import sin, cos, acos, radians
###############################################################################


###############################################################################
#CONSTANTES
###############################################################################
#Robin Keys
TK_MAPS_1="AIzaSyB8pxsl2jFQSwshMT2I5Weue8CKLgxalY8"
#Arnaud Keys
TK_MAPS_2="AIzaSyCiZVNwOpKaJyBT0L0s6PDUA98_nizshIA"
#Foursquare
CLIENT_ID="1LD4L3ES2MGHGMEUQTSGMTTJUL5AWHTYMOA340FFHY5HBLED"
CLIENT_SECRET="PYDER5QZHVZZE4NYAUFKTHIMXEP513WWBLV14DNOWKAZLUDN"
#Filtres de recherche
LIMIT="50"
RAYON_TERRE=6378137.0
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant de récupérer la date d'aujourd'hui et celle dans un mois
#renvoi en string pour l'url
def getDate():
    date_today=time.time()
    end_time=date_today+2629743 #in one month
    return [str(date_today), str(end_time)]


#Fonction permettant de récupérer des coordonnées GPS à partir d'une adresse
def getGps(address):
    g = Nominatim()
    location=g.geocode(address)
    return [str(location.latitude), str(location.longitude)]


#Permet de récupérer un JSON avec le trajet entre N points
def getTrace(path_file, latDep, longDep, latArr, longArr, tWaypoints, mode):
    #Création des stops
    temp=np.shape(tWaypoints)
    if(temp[0]==0):
        waypoints=''
    elif(temp[0]>=1):
        waypoints="&waypoints=via:"+ str(tWaypoints[0,0]) + "%2C" + str(tWaypoints[0,1])
        #print(waypoints)
    elif(temp[0]>1):
        for i in range(1,temp[0]):
            waypoints = waypoints + "%7Cvia:" + str(tWaypoints[i,0]) + "%2C" + str(tWaypoints[i,1])
    #Récupération des données via API
    link="https://maps.googleapis.com/maps/api/directions/json?origin="+str(latDep)+","+str(longDep)+"&mode="+mode+"&destination="+str(latArr)+","+str(longArr)+waypoints+"&key="+TK_MAPS_1
    json_data=requests.get(link)
    #conversion au format JSON
    data=json_data.json()
    #écriture du fichier
    with open(path_file, 'w') as json_file :
        json.dump(data, json_file, indent=4)
    return(link)


#Renvoie toutes les coordonnées GPS d'un tracé sous forme de tableau string lat | long
#Export des coordonnées dans CSV
def getTraceGps(base_url, csv_file):
    lat=[];lng=[]
    r=requests.get(base_url)
    data=r.json()['routes'][0]['legs'][0]['steps']
    df=pd.DataFrame({'position':data})
    nSize=len(df)
    for i in range(0,nSize):
        coord=data[i]['end_location']
        lat.append(coord['lat'])
        lng.append(coord['lng'])
    with open(csv_file, "w") as f:
        writer=csv.writer(f, lineterminator="\n")
        writer.writerows(np.column_stack((lat, lng)))
    return ([[lat], [lng]])


#Fonction permettant de renvoyer une liste d'id_place
def getPlaces(lat, lng, rayon):
    #Récupération des données via API
    link="https://api.foursquare.com/v2/venues/search?ll="+lat+","+lng+"&categoryId=4d4b7104d754a06370d81259&limit="+LIMIT+"&radius="+rayon+"&client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v=20180403"
    list_id=[]
    #Requêtes
    json_data=requests.get(link)
    data=json_data.json()['response']['venues']
    df=pd.DataFrame({'venues':data})
    nSize=len(df)
    #conversion au format JSON
    for i in range(0,nSize):
        data_id=data[i]
        list_id.append(data_id['id'])
    #renvoi de liste
    return(list_id)


#Fonction permettant de retourner une place avec details dans un JSON
def getPlaceFromId(id_p, path_file):
    link="https://api.foursquare.com/v2/venues/"+id_p+"?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v=20180403"
    print("request : "+link)
    json_data=requests.get(link)
    try:
        data=json_data.json()['response']['venue']
        with open(path_file, 'w') as json_file :
            json.dump(data, json_file, indent=4)
    except KeyError:
        print("no data")


#Fonction permettant de lire un json et d'instancier une place à partir des données
#Retourne une liste de Places
def fromJsonToPlace(path_file, city_id):
    list_places=[]
    data_json=json.load(open(path_file))
    if (len(data_json)!=0):
        nSize=len(data_json['categories'])
        #On enregistre uniquement les éléments avec description et photo
        try:
            types=[]
            #Mise en forme des données sous liste
            for i in range(0,nSize):
                types.append(data_json['categories'][i]['name'])
            id_=data_json['id']
            photo=data_json['bestPhoto']['prefix']+data_json['bestPhoto']['suffix']
            visitsCount=data_json['stats']['visitsCount']
            geometry=[data_json['location']['lat'],data_json['location']['lng']]
            name=data_json['name']
            print("CITYID de la place enregistrée : "+str(city_id))
            list_places.append(p.Place(id_, name, photo, types, geometry, visitsCount, city_id))
        except KeyError:
            print("informations manquantes")
        except IndexError:
            print("informations manquantes")
    else:
        print("hors sélection")
    return list_places


#Suppression des doublons dans une liste
#Retourne la liste filtrée
def remove_duplicates(lst):
    i=0
    j=0 
    nSize=len(lst)
    while(i<nSize-1):
        obj=lst[i]
        j=i+1
        while(j<nSize):
            if(obj.getId()==lst[j].getId()):
                del lst[j]
                nSize=nSize-1
            else:
                j=j+1
        i=i+1
    return lst


#Lecture du fichiers contenant les coordonnées GPS
#Recherche des places autour de chaque point
#Retourne la liste avec toutes les places
def getPlacesGps(path_coords, path_file):
    #Ouverture du fichier
    t1=time.time()
    with open(path_coords, "r") as file_csv:
        places=[]
        places_id=[]
        city_id=[]
        temp=csv.reader(file_csv)
        coords=list(map(tuple,temp))
        coords_t = [t[2:4] for t in coords]
        datas_coord=np.array(coords_t).astype("float")
        nSize=len(datas_coord)
        for i in range(0,nSize):
            print(str(i)+" : "+str(datas_coord[i][0])+","+str(datas_coord[i][1]))
            t=len(getPlaces(str(datas_coord[i][0]), str(datas_coord[i][1]), str(5000)))
            print("Nombre de places pour la ville : " + str(t))
            if(i==0):
                places_id = getPlaces(str(datas_coord[i][0]), str(datas_coord[i][1]), str(5000))
            else:
                places_id = places_id + getPlaces(str(datas_coord[i][0]), str(datas_coord[i][1]), str(5000))
            for j in range (0,t):
                city_id.append(int(coords[i][0]))
        nSize=len(places_id)
        print("Nombre de places au total : "+str(nSize))
        print("Taille de la liste de villes : "+ str(len(city_id)))
        for i in range(0,nSize):
            getPlaceFromId(places_id[i], path_file)
            if(i==0):
                places=fromJsonToPlace(path_file, city_id[i])
            else:
                places=places+fromJsonToPlace(path_file, city_id[i])
    t2=time.time()
    print("Temps de reception des places : ", t2-t1, " s")
    return remove_duplicates(places)


#Fonction permettant de récupérer la distance et la durée entre deux coordonnées
#lors d'un trajet selon différents modes de transport
def getDistance_Duree(latDep, lngDep, latArr, lngArr, mode):
    t1=time.time()
    #Récupération des données via API
    link="https://maps.googleapis.com/maps/api/directions/json?origin="+latDep+","+lngDep+"&mode="+mode+"&destination="+latArr+","+lngArr+"&key="+TK_MAPS_1
    print(link)
    json_data=requests.get(link)
    #conversion au format JSON
    data=json_data.json()
    t2=time.time()
    dist = data['routes'][0]['legs'][0]['distance']['value']
    duree = data['routes'][0]['legs'][0]['duration']['value']
    heuristic = RAYON_TERRE*acos(sin(radians(float(latDep)))*sin(radians(float(latArr)))+cos(radians(float(latDep)))*cos(radians(float(latArr)))*cos(radians(float(lngArr))-radians(float(lngDep))))
    print(t2-t1, "s")
    return [mode, duree, dist, heuristic]


#Récupération de toutes les places
def placesToCsv():
    temp = getPlacesGps('../data/cities.csv', '../data/data_place.json')
    with open('../data/all_places.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        for member in temp:
            wr.writerow([member.getId(), member.getName(), member.getPhoto(), str(member.getTypes()), str(member.getGeometry()), str(member.getVisitsCount()), str(member.getCity_id())])
            
            
#Reception des tags disponibles dans les places françaises
#ecriture d'un fichier csv listant les places  
#retourne une liste avec les places_id et le stags associés
def getTypes():
    list_tags=[]
    df = pd.read_csv('../data/all_places.csv')
    nSize=len(df)
    types = df.type
    id_places=df.id
    #Premiere boucle pour supprimer les # entre les mots
    for i in range(0,nSize):
        data = types[i].split()
        for words in data:
            nwords = words.replace('#',' ')
            #Ajout des ID des places et des tags associes                       
            list_tags.append([id_places[i], nwords.rsplit(None, 1)[-1].replace('[', '').replace(']', '').replace("'", "").replace('/', '').replace('&','').replace('or','').replace('Caf\xc3\xa9','') ])
            final=list_tags
    #Ecrit tous les Id et les tags dans un CSV        
    with open('../data/list_tag_places_2.csv', 'w') as f:
        wr = csv.writer(f, delimiter='\n')
        wr.writerows([final])
    return final    
    

#Création du csv permettant de peupler la table d'association tag, place 
#Une Place est associee par son id aux id de Tags
def placeTags(path_file, return_file):
    associations=getTypes()
    tags = np.genfromtxt(path_file, dtype = None)
    print(associations)
    #print(StringIO(associations))
    tags = np.genfromtxt(path_file, dtype = None, encoding='utf8')
    print(tags)
    nSize=len(tags)
    print(nSize)
    ySize=len(associations)
    with open(return_file, 'w') as csv_file:
        wr=csv.writer(csv_file)
        for i in range(0,ySize):
            for j in range(0,nSize):
                if(associations[i][1]==tags[j]):
                    print(associations[i][0])
                    print(j)
                    wr.writerow([associations[i][0], j])
                    


#Récupération des paramètres de distance, durée et heuristique
#entre toutes les villes
#Insertion dans un CSV                     
def paramsToCsv(path_file, return_file):
    with open(path_file, 'r') as csvfile:
        cities=csv.reader(csvfile)
        l=list(map(tuple,cities))
        nSize=len(l)
        df=pd.DataFrame(l)
        id_dep=df.iloc[:,0]
        id_arr=df.iloc[:,0]
        lat_dep=df.iloc[:,2]
        lng_dep=df.iloc[:,3]
        lat_arr=df.iloc[:,2]
        lng_arr=df.iloc[:,3]
        #print(lat_dep)
        #print(lat_arr)
        with open(return_file, 'w+') as csv_file:
            for i in range(0,nSize):
                for j in range(0,nSize):
                    if (i!=j or i<j):
                        wr = csv.writer(csv_file)
                        try:
                            wr.writerow([getDistance_Duree(lat_dep[i], lng_dep[i], lat_arr[j], lng_arr[j], "driving"), id_dep[i], id_arr[j]])
                            wr.writerow([getDistance_Duree(lat_dep[i], lng_dep[i], lat_arr[j], lng_arr[j], "walking"), id_dep[i], id_arr[j]])
                            wr.writerow([getDistance_Duree(lat_dep[i], lng_dep[i], lat_arr[j], lng_arr[j], "transit"), id_dep[i], id_arr[j]])
                            print(id_dep[i], id_arr[j])
                        except IndexError:
                            print("Trajet inexistant")
###############################################################################
