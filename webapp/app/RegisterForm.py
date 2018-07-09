from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, PasswordField, FieldList
from wtforms_components import TimeField
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymongo as pm


###############################################################################    
class RegisterForm(FlaskForm):
    register_email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    register_password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=20)])
    register_nom = StringField('nom', validators=[InputRequired(), Length(min=1, max=30)])
    register_prenom = StringField('prenom', validators=[InputRequired(), Length(min=1, max=30)])
    register_tags = StringField('tags', validators=[InputRequired(), Length(min=1, max=30)])
    register_rue = StringField('rue', validators=[InputRequired(), Length(min=1, max=50)])
    register_cp = StringField('cp', validators=[InputRequired(), Length(min=5, max=5)])
    register_ville = StringField('ville', validators=[InputRequired(), Length(min=1, max=30)])
    register_submit = SubmitField('Valider') 
###############################################################################