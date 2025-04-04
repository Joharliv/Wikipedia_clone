from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.secret_key = "1234"
app.permanent_session_lifetime = timedelta(days=1)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    username = db.Column("username", db.String(100))
    mobile = db.Column("mobile", db.String(10))
    email = db.Column("email", db.String(100))
    password_hash = db.Column(db.String(100))

    def __init__(self, name, username, mobile, email, password):
        self.name = name
        self.username = username
        self.mobile = mobile
        self.email = email
        self.password_hash = generate_password_hash(password)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("password")

        found = users.query.filter_by(username=username).first()
        if found:
            return render_template("signup.html", error="Username already exists. Please choose another.")

        usr = users(name, username, mobile, email, password)
        db.session.add(usr)
        db.session.commit()

        return render_template("login.html", success="Account Created Successfully")
    return render_template("signup.html")

@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form.get("username")
        session["username"] = username
        password = request.form.get("password")
        found = users.query.filter_by(username=username).first()

        if not found:
            return render_template("signup.html", error="Username not found, Please Signup first.")

        if check_password_hash(found.password_hash, password):
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Incorrect Password.")
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    search_results = []
    no_results = False  

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query
            }
            response = requests.get(url, params=params).json()

            if "query" in response and response["query"]["search"]:
                search_results = [
                    {"title": item["title"], "link": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}"}
                    for item in response["query"]["search"]
                ]
            else:
                no_results = True  

    return render_template("home.html", search_results=search_results, no_results=no_results)



@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")




if __name__ == "__main__":
    app.run(debug=True)
