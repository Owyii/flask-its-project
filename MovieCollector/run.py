#set FLASK_APP=run.py
#set FLASK_DEBUG=1
#flask run

from flask import Flask, render_template, url_for, redirect
from forms import Registration, Login

app = Flask(__name__)
app.config['SECRET_KEY'] = '3f6c59a78e0f1e874119ae92aead45e99bee571d'


posts = [
{"author" :"Pico de Paperis",
 "title" : "This is a blog",
 "content":"This is a post by PdP",
 "date_posted":"16-11-2022 15:48"
},         
{"author" :"Paolino Paperino",
 "title" : "Qua Qua Qua",
 "content":"Paperino ha scritto in italiano",
 "date_posted":"15-11-2022 20:48"
}              
]



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title ="Home Page", posts = posts)



@app.route("/about")
def about():
    return render_template("about.html", title="About Page")

@app.route("/login")
def login():
    form = Login()
    return render_template("login.html", title="LogIn Page", form = form)

@app.route("/register", methods = ["POST","GET"])
def register():
    form = Registration()

    if form.validate_on_submit():
        print("Registered")
        return redirect("/login")

    return render_template("register.html", title="Register Page", form = form)

@app.route("/new_post")
def new_post():
    return render_template("new_post.html", title="New Post Page")

if __name__ == "__main__":
    app.run()