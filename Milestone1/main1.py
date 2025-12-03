from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
)
import datetime
import os
import json


app = Flask(__name__, static_url_path="/static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_FOLDER = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_FOLDER, exist_ok=True)

DB_PATH = os.path.join(INSTANCE_FOLDER, "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SECRET_KEY"] = "secret123"
app.config["JWT_SECRET_KEY"] = "jwtsecret123"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def check_password(self, p):
        return self.password == p

with app.app_context():
    db.create_all()


people_count = 5



@app.route("/")
def home():
    return redirect("/login1")


@app.route("/register1", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return render_template("register1.html", error="Email already exists")

        db.session.add(User(name=name, email=email, password=password))
        db.session.commit()
        return redirect("/login1")

    return render_template("register1.html")


@app.route("/login1", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("login1.html", error="User not found")

        if not user.check_password(password):
            return render_template("login1.html", error="Wrong password")

        token = create_access_token(
            identity=user.email,
            additional_claims={"name": user.name},
            expires_delta=datetime.timedelta(hours=6)
        )

        resp = redirect("/dashboard")
        set_access_cookies(resp, token)
        return resp

    return render_template("login1.html")


@app.route("/logout")
def logout():
    resp = redirect("/login1")
    unset_jwt_cookies(resp)
    return resp


@app.route("/dashboard")
@jwt_required()
def dashboard():
    email = get_jwt_identity()
    claims = get_jwt()
    user = {"name": claims["name"], "email": email}
    return render_template("dashboard1.html", user=user)


@app.route("/get_counts")
def get_counts():
    global people_count
    return jsonify({"count": people_count, "details": {"person": people_count}})


if __name__ == "__main__":
    app.run(debug=True)
