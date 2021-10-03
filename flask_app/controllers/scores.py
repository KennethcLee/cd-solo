import re
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask.templating import render_template_string
from flask_app import app
from flask_app.models.login import Logins
from flask_app.models.score import Scores

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
app.secret_key="randomstring"

@app.route("/scoreboard")
def scoreboard():
    if session.get('logged_in') == True:
        data = {
            'user_id': session['user_id'],
            'email': session['email'],
            'game_type': 'addition'
        }
        user=Logins.get_user(data)
        # game_types=Games.get_game_types()
        scores=Scores.get_all(data)
        print('*** 200 ***')
        return render_template("/scoreboard.html", user=user, scores=scores)
    else:
        return redirect("/login")
