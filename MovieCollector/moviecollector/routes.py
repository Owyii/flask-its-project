from flask import render_template, url_for, redirect, flash, request
from moviecollector import app, db, bcrypt
from moviecollector.forms import RegistrationForm, LoginForm
from moviecollector.models import User,Films
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# lib to get movie information
from PyMovieDb import IMDB
import json

# some global variable
database_url = r'sqlite:///C:\Users\Emanuele\Documents\GitHub\flask-its-project\MovieCollector\instance\mydb.db'

# function to get movie information
def search_film_title(title):
    imdb = IMDB()
    res = imdb.search(title)
    data = json.loads(res)
    output = []
    for i in data['results']:
        output.append([i['name'],i['id']])
    return output

def search_film_information(id):
    print(f"id è {id}")
    imdb = IMDB()
    res = imdb.get_by_id(id)
    return json.loads(res)


@app.route("/")
@app.route("/home")
def home():
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)

    session = Session()
    films = session.query(Films).all()
    session.close()
    # render a template with the film information
    return render_template('home.html',title="Home Page", films=films)
    #return render_template('home.html',title="Home Page")

@app.route("/about")
def about():
    return render_template("about.html", title="About Page")

@app.route("/film/<film>")
def film_page(film):
    return render_template("about.html", film=film)

@app.route('/add', methods=['GET', 'POST'])
def search_film_title_page():
    if request.method == 'POST':
        # get the film title from the form
        title = request.form['title']
        
        # get a list of possible matches
        matches = search_film_title(title)
        
        # pass the matches to the template for display
        return render_template('select_film.html', matches=matches)
    else:
        return render_template('search_film.html')

@app.route('/select_film', methods=['POST'])
def select_film():
    # create a list with the information 
    selected_film = request.form['film']
    film_list = selected_film.strip('][').split(", ")
 
    # create sqlAlchemy obj that are needed
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    Base = declarative_base()

    # define the Films table
    class Films(Base):
        __tablename__ = 'Films'
        id = Column(Integer, primary_key=True)
        title = Column(String)
        director = Column(String)
        year = Column(Integer)
        description = Column(String)
        poster = Column(String)
    
    # check if the Films table exists in the database
    metadata = MetaData()
    print(f'plsssss {film_list}')
    print(f"film  è {film_list[0]}   {film_list[-1]}")
    data = search_film_information(film_list[-1].strip('\''))

    # create the table in the database
    metadata.create_all(engine)
    conn = engine.connect()
    max_id = conn.execute(text("SELECT MAX(id) FROM Films"))
    result = max_id.first()[0]

    print(result)
    print(data)

    if result is None:
        max_id = 0
    else:
        max_id = result + 1
    
    #if it give back no error messages
    if('status' not in data.keys()): 
        session = Session()
        # create a new row to add to the table
        new_film = Films(id=max_id,title=data['name'],director=data['director'][0]['name'],year=data['datePublished'],description=data['description'],poster=data['poster'])
        # add the new row to the session
        session.add(new_film)
        session.commit()
    return redirect('/')

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back {user.username}', category='success')
            return redirect('home')

        else:
            flash('Wrong email or password', category='danger')
            return redirect('login')
    else:
        return render_template("login.html", title="Login Page", form=form)

@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data,
                    password=pw_hash,
                    email=form.email.data)
        with app.app_context():

            db.session.add(user)
            db.session.commit()

        flash(
            f"Your account has been created {form.username.data}", category="success")
        return redirect('/login')

    return render_template("register.html", title="Register Page", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logged Out', category='info')
    return redirect('/home')