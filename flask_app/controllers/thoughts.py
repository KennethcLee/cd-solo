import re
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask.templating import render_template_string
from flask_app.models.login import Logins
from flask_app.models.thought import Thoughts
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
app.secret_key="randomstring"

@app.route("/thoughts")
def thoughts():
    if session.get('logged_in') == True:
        data = {
            'user_id': session['user_id'],
            'email': session['email']
        }
        user=Logins.get_user(data)
        thoughts=Thoughts.get_all()
        print('*** 100 ***', thoughts)
        return render_template("/thoughts.html", user=user, thoughts=thoughts)
    else:
        return redirect("/login")

@app.route("/thought_create", methods=['POST'])
def thought_create():
    if session.get('logged_in') == True:
        data = {
            'user_id': session['user_id'],
            'thought': request.form['thought']
        }
        if not Thoughts.validate_thought(data):
            return redirect("/thoughts")
        Thoughts.create(data)
        return redirect("/thoughts")
    else:
        return redirect("/login")

@app.route("/thoughts/like/<int:id>")
def thought_like(id):
    if session.get('logged_in') == True:
        data = {
            'id': id
        }
        Thoughts.like(data)
        print('*** 120 ***', data)
        return redirect("/thoughts")
    else:
        return redirect("/login")

@app.route("/thoughts/dislike/<int:id>")
def thought_dislike(id):
    if session.get('logged_in') == True:
        data = {
            'id': id
        }
        Thoughts.dislike(data)
        print('*** 120 ***', data)
        return redirect("/thoughts")
    else:
        return redirect("/login")

@app.route("/thoughts/delete/<int:id>")
def thought_delete(id):
    if session.get('logged_in') == True:
        data = {
            'id': id
        }
        Thoughts.delete(data)
        print('*** 120 ***', data)
        return redirect("/thoughts")
    else:
        return redirect("/login")

@app.route("/users/<int:user_id>")
def thought_get_all_user(user_id):
    if session.get('logged_in') == True:

        print('*** 190 ***')
        data = {
            'user_id': session['user_id'],
            'email': session['email']
        }
        user=Logins.get_user(data)
        print('*** 190A ***', user)

        data = {
            'id': user_id
        }

        thoughts = Thoughts.get_all_user(data)
        print('*** 190B ***', data)
        return render_template("/users.html", user=user, thoughts=thoughts)
    else:
        return redirect("/login")
