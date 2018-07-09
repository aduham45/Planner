###############################################################################
#Fichier de configuration de l'application
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import os
basedir = os.path.abspath(os.path.dirname(__file__))


###############################################################################
#Fonction contenant la classe de configuration de l'application
###############################################################################
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'solutec'
	#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqllite:///' + os.path.join(basedir, 'app.db')
	#SQLALCHEMY_TRACK_MODIFICATIONS = False

	
