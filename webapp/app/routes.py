from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, SelectMultipleField, SelectField
from wtforms_components import TimeField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine, Document
import pymongo as pm
from RegisterForm import RegisterForm
from LoginForm import LoginForm
import bcrypt
from LogoutForm import LogoutForm
from ModifForm import ModifForm
from ModifAcceptedForm import ModifAcceptedForm
from tags import *
import computing as cp
import plan as pl
import time
from node import *
###############################################################################
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
bootstrap = Bootstrap(app)
datas=cp.init_matrix()
SESSION_TYPE = "mongodb"
#Session(app)
mongo = pm.MongoClient()
###############################################################################
client=pm.MongoClient('mongodb://root:root_06@ds263660.mlab.com:63660/smartplanner_users')
db=client.get_database()
users=db['users']
###############################################################################

 
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
    max_escales=SelectField('Nombre maximal d\'escales :', choices=[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)])
    escales=TextField('Escales :')
    t_max=RadioField('Durée maximale sans pause :', choices=[(0,'Sans pause'),(3600,'1h00'),(7200,'2h00'),(10800,'3h00')])
    d_max=RadioField('Distance maximale sans pause:', choices=[(0,'Sans pause'),(100000,'100km'),(20000,'200km'),(300000,'300km')])
    t_repas=RadioField('Durée maximale du repas :', choices=[(900,'15 min'),(1800,'30 min'),(3600,'1h00')])
    submit=SubmitField('Valider')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form=LoginForm(request.form)
    if login_form.validate_on_submit():
        hashpass=bcrypt.hashpw(request.form['login_password'].encode('utf-8'), bcrypt.gensalt())
        user=users.find({'email':request.form['login_email'], 'password':hashpass})   
        if user:
            session['email']=request.form['login_email']
            return redirect(url_for('form'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form)  
    if register_form.validate_on_submit():
        hashpass=bcrypt.hashpw(request.form['register_password'].encode('utf-8'), bcrypt.gensalt())
        users.insert({'email': request.form['register_email'], 'password':hashpass, 'nom':request.form['register_nom'], 'prenom':request.form['register_prenom'], 'rue':request.form['register_rue'], 'cp':request.form['register_cp'], 'ville':request.form['register_ville'], 'tags':request.form['register_tags']})
        session['email'] = request.form['register_email']
        return redirect(url_for('form'))
    return render_template('register.html', register_form=register_form)    
    

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', Title="Accueil")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    logout_form=LogoutForm(request.form)
    modif_form=ModifForm(request.form)
    modif_accepted_form=ModifAcceptedForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        session['email']=None
        return redirect(url_for('login'))
    if modif_accepted_form.register_submit.data and modif_accepted_form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('profile.html', logout_form=logout_form, modif_form=modif_form, session_email=session['email'], modif_accepted_form=modif_accepted_form)    
    

@app.route('/form', methods=['GET','POST'])
def form():
    logout_form=LogoutForm(request.form)
    modif_form=ModifForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        session['email']=None
        return redirect(url_for('index'))
    
    form = ReusableForm(request.form)
    #tags_user=[]
    #add_dep='Lille'
    #add_arr='Marseille'
    #escales='Grenoble'
    test=[]
    tags=['Hall', 'Museum']
    #optimisation='distance'
    #mode='driving'
    #overallScore= cp.get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0]
    start=Node(13, 0, None, 0, 0)
    target=Node(2, 0, None, 0, 0)
    #d_max=300000
    #dtfr = cp.get_graph_matrix('Lille', 'Marseille', [], 'driving', overallScore)
    #df_filtered = dtfr
    if request.method == 'POST':
        add_dep=request.form.get('add_dep')
        #add_dep='Lille'
        session["add_dep"]=add_dep
        
        add_arr=request.form.get('add_arr')
        #add_arr='Marseille'
        session["add_arr"]=add_arr
        escales=[form.escales.data]
        #escales=['Grenoble']
        
        tags=form.tags.data
        session["tags"]=tags
        
        optimisation=request.form.get('optimisation')
        #session["optimisation"]=optimisation
        
        mode=request.form.get('locomotion')
        #session["mode"]=mode
        
        h_dep=request.form.get('h_dep')
        j_dep=request.form.get('j_dep')
        h_arr=request.form.get('h_arr')
        j_arr=request.form.get('j_arr')
        #escales=request.form.get('escales')
        t_max=request.form.get('t_max')
        #d_max=request.form.get('d_max')
        t_repas=request.form.get('t_repas')
        
        overallScore = cp.get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0]
        #session["overallScore"]=overallScore
        
        #t_max=10800
        d_max=300000
        #mode='driving'
        #optimisation='distance'
        
        dtfr=cp.get_graph_matrix(add_dep, add_arr, escales, 'driving', overallScore)
        #session["dtfr"]=dtfr
        df_filtered = dtfr.loc[dtfr['distance'] < d_max]
        #session["df_filtered"]=df_filtered
        #df_filtered = df.loc[df['time']<=t_max]
        test=pl.get_path(start, target, dtfr, overallScore, optimisation, df_filtered, datas[0], add_dep, add_arr, escales)
        #test=cp.get_way(tags, cp.get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0], 2, datas[0])
        session["test"]=test
        return redirect('/map')
    else:
        #add_dep=session.get("add_dep", None)
        #add_arr=session.get("add_arr", None)
        tags=session.get("tags", None)
        #optimisation=session.get("optimisation", None)
        #mode=session.get("mode", None)
        #overallScore=session.get("overallScore", None)
        #dtfr=session.get("dtfr", None)
        #df_filtered=session.get("df_filtered", None)
        test=session.get("test", None)  
    #test=pl.get_path(start, target, dtfr, overallScore, optimisation, df_filtered, datas[0], add_dep, add_arr)
    #session["test"]=test
        #return redirect('/map')
    #if tags == []:
        #tags=session.get("tags", None)
    #else:
        #pass
    #test=cp.get_way(tags, cp.get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0], 2, datas[0])
    #test=pl.get_path(start, target, df, overallScore, optimisation, df_filtered, datas[0])
    #session["test"]=test
    #tags=['Museum']
    return render_template('form.html', title='Formulaire', form=form, logout_form=logout_form, modif_form=modif_form, session_email=session['email'])
 

@app.route('/test')
def test():
    return render_template('t.html', title='test')

@app.route('/map')
def map():
    depart=session.get("add_dep", None)
    arrivee=session.get("add_arr", None)
    tags=session.get("tags", None)
    test=session.get("test", None)
    
    return render_template('map.html', title='Map', depart=depart, arrivee=arrivee, tags=tags, test=test)


 
if __name__ == "__main__":
    app.run(debug="true")
