from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, SelectMultipleField
from wtforms_components import TimeField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class ReusableForm(FlaskForm):
    add_dep=StringField('Adresse de départ :', validators=[DataRequired()])
    add_arr=StringField('Adresse d\'arrivée :', validators=[DataRequired()])
    #tags=StringField('Tags :', validators=[DataRequired()])
    tags = SelectMultipleField('Tags', choices=Tags(TAGS))
    locomotion=RadioField('Locomotion :', choices=[('driving','Voiture'),('transit','Transports en commun'),('walking','A pied')])
    optimisation=RadioField('Optimisation :', choices=[('distance','Distance'),('time','Temps'),('affinity','Affinités')])
    h_dep=TimeField('Heure de départ :')
    j_dep=TimeField('Jour de départ :')
    h_arr=TimeField('Heure d\'arrivée :')
    j_arr=TimeField('Jour d\'arrivée :')
    escales=TextField('Escales :')
    t_max=RadioField('Durée maximale sans pause :', choices=[(3600,'1h00'),(7200,'2h00'),(10800,'3h00')])
    t_repas=RadioField('Durée maximale du repas :', choices=[(900,'15 min'),(1800,'30 min'),(3600,'1h00')])
    submit=SubmitField('Valider')