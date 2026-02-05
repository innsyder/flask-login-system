from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_scss import Scss
from datetime import datetime 

app = Flask(__name__)
app.secret_key = "mysecretkey123"
Scss(app, static_dir="static", asset_dir="assets")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" 
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET" , "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username exists")
        
        hashed = generate_password_hash(password)
        u = User(username=username, password_hash=hashed)
        db.session.add(u)
        db.session.commit()

        session["user"] = username 
        return redirect("/dashboard")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user"] = user.username
            return redirect("/dashboard")
        
        return render_template("login.html", error="Invalid username or password")
    
    return render_template("login.html")


@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()

        if user:
            return redirect(f"/reset/{user.id}")
        else:
            return render_template("forget.html", error="User not found")
        
    return render_template("forget.html")


@app.route("/reset/<int:user_id>", methods=["GET", "POST"])
def reset(user_id):
    user = User.query.get(user_id)

    if not user:
        return redirect("/login")

    if request.method == "POST":
        new_password = request.form["new_password"]
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return redirect("/login")
    
    return render_template("reset.html")



@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("dashboard.html", username=session["user"])


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)






