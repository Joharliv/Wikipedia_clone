from flask import Flask, render_template, redirect, url_for, request,session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
app.secret_key="1234"
app.permanent_session_lifetime=timedelta(minutes=15)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///users.sqlite3'

db=SQLAlchemy(app)
class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    name=db.Column("name",db.String(100))
    username=db.Column("username",db.String(100))
    mobile=db.Column("mobile",db.String(10))
    email=db.Column("email",db.String(100))
    password_hash=db.Column(db.String(100))

    def __init__(self,name,username,mobile,email,password):
        self.name=name
        self.username=username
        self.mobile=mobile
        self.email=email
        self.password_hash=generate_password_hash(password)


@app.route("/")
def index():
    


    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup.html",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        mobile=request.form.get("mobile")
        email=request.form.get("email")
        password=request.form.get("password")
        
        found=users.query.filter_by(username=username).first()
        if(found):
            session["username"]=found.username
            return render_template("login.html")
        else:
        
            usr=users(name,username,mobile,email,password)
            db.session.add(usr)
            db.session.commit()
            return render_template("login.html")
        
    else:
        return render_template("signup.html")


   

@app.route("/login.html", methods=[ "GET","POST"])
def login():
    if request.method == "POST":
        session.permanent=True
        username=request.form.get("username")
        session["username"]=username
        password=request.form.get("password")
        found=users.query.filter_by(username=username).first()
        if(not found):
            return render_template("signup.html")

        if(check_password_hash(found.password_hash,password)):
            #where will user go after verification
            return render_template("home.html")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")



@app.route("/")
def user():
    username=session["username"]
    return f"<h1>{username}</h1>"

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":

    app.run(debug=True)  # Enable debug mode to see errors
