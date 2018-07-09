#!/usr/bin/env python
# coding: utf-8 

###############################################################################
#Fichier contenant la classe place
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#15/03/2018
###############################################################################


###############################################################################
#OBJETS
###############################################################################
class Place:
    #CONSTRUCTEUR DE Place
    def __init__(self, id_, name, photo, types, geometry, visitsCount, city_id):
        self.id_ = id_ #String
        self.name=name #String
        self.photo=photo #String
        self.types=types #String[]
        self.city_id=city_id #Int
        self.geometry=geometry #Float[]
        self.visitsCount=visitsCount #Int

    def getId(self):
        return self.id_#String

    def getName(self):
        return self.name #String

    def getPhoto(self):
        return self.photo #String

    def getTypes(self):
        return self.types #tab String

    def getGeometry(self):
        return self.geometry #tab Float

    def getVisitsCount(self):
        return self.visitsCount #Int
    
    def getCity_id(self):
        return self.city_id #Int

    def displayPlace(self):
        print("Id : " + self.id_)
        print("Name : " + self.name)
        print("Photo : " + self.photo)
        print("Types : " + str(self.types))
        print("Geometry : " + str(self.geometry))
        print("VisitsCounts : " + str(self.visitsCount))
        print("City_id : " + str(self.city_id))
###############################################################################
