#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#Fichier contenant la fonction créant le formulaire de renseignements
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, BooleanField, DateTimeField, FieldList, FormField, HiddenField
import request, app
#from wtforms_components import TimeField
from wtforms.validators import DataRequired
from .tags import *

###############################################################################
#Fonction créant le formulaire
###############################################################################
class EscalesForm(FlaskForm):
    escales = StringField('', validators=[DataRequired()])


class TrajectForm(FlaskForm):
	depart = StringField('', validators=[DataRequired()])
	start_date_time = DateTimeField('Jour et heure de départ (format JJ/MM/AAAA HH:MM)',format='%d/%m/%Y %H:%M')
	arrivee = StringField('', validators=[DataRequired()])
	#♣escales = BooleanField('Voulez-vous ajouter des escales ?')
	#choix_escales = StringField('Choix des escales ')
	choix_escales = FieldList(FormField(EscalesForm), min_entries=0, max_entries=3)
	addEscales = SubmitField('Plus d\'escales ')
	deleteEscales = SubmitField('Supprimer derniere escale ')
	mode = SelectField('Moyen de transport', choices=[('Voiture', 'Voiture'), ('Train', 'Train'), ('A pied', 'A pied')])
	pause_voyage = SelectField('Duree maximale d\'un trajet avant une pause', choices=[('1h', '1h'),('2h', '2h'),('3h', '3h'),('4h', '4h')])
	tps_repas = SelectField('Duree maximale du repas', choices=[('30min', '30min'),('1h', '1h'),('2h', '2h')])
	tags = SelectMultipleField('Tags', choices=Tags(TAGS))
	submit = SubmitField('Valider')