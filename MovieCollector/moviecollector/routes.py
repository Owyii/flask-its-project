from flask import render_template, url_for, redirect, flash, request, abort
from moviecollector import app, db, bcrypt
from moviecollector.forms import RegistrationForm, LoginForm, UpdateUserForm
from moviecollector.models import User,Films,Comment
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# lib to get movie information
from PyMovieDb import IMDB
import json

# lib needed to create a form to add comment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# some global variable to get the path of the db
file = "MovieCollector/instance/mydb.db"
database_url = r'sqlite:///C:\Users\Utente\Documents\GitHub\flask-its-project\MovieCollector\instance\mydb.db'

# function to get movie information from the IMDB Api
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

# @app.route("/about")
# def about():
#     return render_template("about.html", title="About Page")

@app.route("/film/<film>")
def film_page(film):
    print(film)
    return render_template("about.html",film=film)



# @app.route('/films/<int:id>')
# def film_detail(id):
#     engine = create_engine(database_url)
#     Session = sessionmaker(bind=engine)
#     # retrieve the film from the database based on its ID
#     session = Session()
#     film = session.query(Films).filter_by(id=id).first()
#     session.close()

#     # render a template with the film information
#     return render_template('film_detail.html', film=film)

@app.route('/film/<int:id>', methods=['GET', 'POST'])
def film_detail(id):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    # retrieve the film from the database based on its ID
    session = Session()
    film = session.query(Films).filter_by(id=id).first()
    session.close()

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        user = form.user.data
        new_comment = Comment(text=comment,user=user, film_id=id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('film_detail', id=id))
    comments = Comment.query.filter_by(film_id=id).all()
    return render_template('film_detail.html', film=film, form=form, comments=comments)

# Using the flaks lib i create a form to insert the comment
class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    user = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/films/<int:id>/comments', methods=['POST'])
@login_required
def add_comment(id):
    film = Films.query.get(id)
    text = request.form.get('text')
    comment = Comment(text=text, film=film)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('film_detail', id=id))

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

    # # define the Films table
    # class Films(Base):
    #     __tablename__ = 'Films'
    #     id = Column(Integer, primary_key=True)
    #     title = Column(String)
    #     director = Column(String)
    #     year = Column(Integer)
    #     description = Column(String)
    #     poster = Column(String)
    
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
        plot = "Non Disponibile" if data['description'] == None else data['description']
        genere = ", ".join(data["genre"])
        new_film = Films(id=max_id,
                         title=data['name'],
                         director=data['director'][0]['name'],
                         year=data['datePublished'],
                         description=plot,
                         poster=data['poster'],
                         rating=data['rating']['ratingValue'],
                         duration=data['duration'],
                         genere=genere)
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

@app.route("/user_account")
@login_required
def user_account():
    # crea l'url per l'immagine del profilo dell'utente
    image_file = url_for(
        'static', filename=f"images/{current_user.image_file}")

    # restituisce la pagina user_account.html passando il titolo della pagina, l'url dell'immagine
    # del profilo dell'utente
    return render_template("user_account.html", title=f"{current_user.username} page",
                           image_file=image_file)

@app.route("/user_account/edit", methods=['POST', 'GET'])
@login_required
def edit_user_account():
    # Percorso del file immagine dell'utente
    image_file = url_for('static', filename=f"images/{current_user.image_file}")

    # Creazione del form per l'aggiornamento dei dati dell'utente
    form = UpdateUserForm()

    if form.validate_on_submit():
        # Aggiornamento del file immagine dell'utente se presente
        if form.image_file.data:
            new_file_name = save_image_file(form.image_file.data)
            current_user.image_file = new_file_name

        # Aggiornamento del nome utente se diverso dal precedente
        if current_user.username != form.username.data:
            current_user.username = form.username.data

        # Aggiornamento dell'email utente se diversa da quella precedente
        if current_user.email != form.email.data:
            current_user.email = form.email.data

        # Salvataggio dei dati aggiornati nel database
        db.session.commit()

        # Messaggio di conferma per l'utente
        flash(f"I tuoi dati sono stati aggiornati {form.username.data}", category="success")
        return redirect(url_for('user_account'))
    else:
        # Se il form non è stato validato, riempire i campi del form con i dati dell'utente
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Mostra la pagina di modifica dati utente
    return render_template("edit_user_account.html", title=f"{current_user.username} - Pagina di aggiornamento dati",
                           image_file=image_file, form=form)


def save_image_file(image_file_data):
    # Estrae l'estensione del file immagine
    _, file_ext = os.path.splitext(image_file_data.filename)

    # Crea un nuovo nome univoco per il file immagine
    new_name = secrets.token_hex(8)
    new_file_name = new_name + file_ext

    # Percorso del file immagine nel server
    file_path = os.path.join(os.getcwd(), "myflaskblog", "static", "images", new_file_name)

    # Salva il file immagine nel server
    image_file_data.save(file_path)

    # TODO: rimuovere il vecchio file immagine (os)
    # TODO: ridurre le dimensioni del file immagine caricato (pillow)

    # Ritorna il nuovo nome del file immagine
    return new_file_name