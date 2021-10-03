import re
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_app.models.login import Logins
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
app.secret_key="randomstring"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    data = {
        'password': request.form['password']
    }
    if not Logins.validate_password_format(data):
        return redirect("/")
    data = {
        'password': request.form['password_confirm']
    }
    if not Logins.validate_password_format(data):
        return redirect("/")
    data = {
        'password': request.form['password'],
        'password_confirm': request.form['password_confirm']
    }
    if not Logins.validate_password_match(data):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    if not Logins.validate_register(data):
        return redirect("/")
    Logins.submit(data)
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("/login.html")


@app.route("/login_user", methods=['POST'])
def login_user():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    user = Logins.get_user(data)
    if not user:
        flash("Invalid Email/Password")
        return redirect("/login")
    print('*** 900B ***', data, user, user.password, request.form['password'])
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect("/login")
    session['user_id']=user.id
    session['email']=user.email
    session['logged_in']=True
    print('*** 900B ***', session['user_id'], user.id)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session['logged_in']=False
    return redirect("/login")