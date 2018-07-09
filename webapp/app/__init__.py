###############################################################################
#Fichier permettant l'initialisation de l'application
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask import Flask
from config import Config
from app import routes
import data_mining, computing, plan
from Node import Node
from flask_bootstrap import Bootstrap

###############################################################################
#Initialisation de l'application
###############################################################################
#Creation de l'instance de l'appplication dans une variable globale
app = Flask(__name__)
 #app.config.from_pyfile('config.py')
app.config.from_object(Config)
bootstrap = Bootstrap(app)


