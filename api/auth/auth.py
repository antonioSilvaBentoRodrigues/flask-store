from flask import Blueprint, render_template, redirect,url_for, request, flash
from flask_login import login_user, logout_user, current_user
from database.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

bp_auth = Blueprint('bp_auth', __name__)


@bp_auth.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bp_views.market"))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
    
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(password=password,pwhash=user.password):
                login_user(user)
                flash("Login successfully","success")
                return redirect(url_for("bp_views.market"))
            else:
                flash("Password invalid", "danger")
        else:
            flash("User not found", "danger")
    return render_template("login.html")


@bp_auth.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("bp_views.home"))


@bp_auth.route("/signup", methods=["GET","POST"])
def sign():
    if current_user.is_authenticated:
        return redirect(url_for("bp_views.market"))
    
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists","danger")
        elif password!=confirm_password:
                flash("Passwords don't match", "danger")
        elif len(password)<8:
                flash("Password too short", "danger")
        elif not re.search(string=password, pattern="[!#$%&()*+,-./:;<=>?@[\]^_{|}~]"):
                flash("Password must contain one of the follow special character (!#$%&()*+,-./:;<=>?@[\]^_{|}~])","warning")
        else:
            try:
                user = User(
                            updated_at=datetime.utcnow(),
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=generate_password_hash(password=password))

                db.session.add(user)
                db.session.commit()
            except Exception as e:
                 print("Error connecting to db", e)
            finally:
                flash("User created successfully","success")
                login_user(user=user)
                return redirect(url_for("bp_views.market"))
            
    return render_template("sign.html")