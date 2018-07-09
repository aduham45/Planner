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
class LoginForm(FlaskForm):
    login_email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    login_password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=20)])
    login_submit = SubmitField('Connexion')
###############################################################################    