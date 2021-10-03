import re
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask.templating import render_template_string
from flask_app.models.login import Logins
from flask_app.models.game import Games
from flask_app import app
from random import randrange
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
app.secret_key="randomstring"

@app.route("/dashboard")
def dashboard():
    if session.get('logged_in') == True:
        data = {
            'user_id': session['user_id'],
            'email': session['email'],
            'game_type': 'addition' 
        }
        user=Logins.get_user(data)
        # game_types=Games.get_game_types()
        print('*** 100 ***')
        return render_template("/dashboard.html", user=user)
    else:
        return redirect("/login")

@app.route("/games/<string:game_type>")
def game_menu(game_type):
    if session.get('logged_in') == True:
        data = {
            'user_id': session['user_id'],
            'email': session['email'],
            'game_type': game_type
        }
        session['game_type']=game_type
        session['gameover']=False
        session['question_total']=0
        session['question_correct']=0
        session['score']=0
        user=Logins.get_user(data)
        print('*** 300 ***', data)
        return render_template("%s.html" % game_type, user=user, data=data)
    else:
        return redirect("/login")

@app.route("/games/<string:game_type>/<int:level>/loading")
def game_load(game_type, level):
    if session.get('logged_in') == True:
        data = {
            'user_id': session['user_id'],
            'email': session['email'],
            'game_type': game_type
        }
        if session.get('gameover') == False:
            if session.get('question_total') == 0:
                session['level']=level
                data = {
                    'game_type': session['game_type'],
                    'level': session['level']
                }
                game_level_data=Games.get_level_data(data)
                session['min_digit']=game_level_data.min_digit
                session['max_digit']=game_level_data.max_digit
                session['min_line']=game_level_data.min_line
                session['max_line']=game_level_data.max_line
                session['max_question']=game_level_data.max_question
                session['question_total'] = 0
                session['question_correct'] = 0
                session['question_incorrect'] = 0
                print('*** 400B ***', game_level_data, game_level_data.min_digit)
                print('*** 400C ***', level, type(level), session['level'], type(session['level']))
        user=Logins.get_user(data)
        return redirect(url_for("game_play", game_type=session['game_type'], level=session['level']))
    else:
        return redirect("/login")

@app.route("/games/<string:game_type>/<int:level>", methods=['GET', 'POST'])
def game_play(game_type, level):
    if session.get('logged_in') == True:
        print('*** 500A ***', session)
        print('*** 500B ***', session['question_total'], session['question_correct'])
        if session['gameover'] == False:
            print('*** 500C ***', session['question_total'], session['max_question'])
            if session['game_type']=="addition":
                if session['question_total'] < session['max_question'] + 1:
                    if session['question_total'] == 0:
                        #Generate Mininum number for random range
                        min_num='1'
                        count = session['min_digit']
                        while count > 1:
                            min_num += '0'
                            count -= 1
                        min_num=int(min_num)
                        session['min_num']=min_num

                        #Generate Maximum number for random range
                        max_num='9'
                        count = session['max_digit']
                        while count > 1:
                            max_num += '9'
                            count -= 1
                        max_num=int(max_num)
                        session['max_num']=max_num
                        print('*** 500F ***', min_num, type(min_num), max_num, type(max_num))

                    else:
                        session['answer'] = int(request.form['answer'])
                        print('*** 500G ***', session['answer'], type(session['answer']))
                        validate = 0
                        for j in session['question_data']:
                            validate += j
                        if session['answer'] == validate:
                            session['question_correct'] += 1
                            session['score'] += 10
                            print('*** 500H ***', session['question_total'], session['question_correct'], session['question_incorrect'])

                    question_data=[]

                    for j in range(0, session['max_line']):
                        question_data.append(randrange(session['min_num'], session['max_num'] + 1))

                    print('*** 500M ***', question_data)
                    session['question_data']=question_data
                    session['question_incorrect']=session['question_total']-session['question_correct']
                    session['question_total']+=1
                    print('*** 500R ***', session)
                else:
                    session['gameover'] = True
                    data = {
                        'user_id': session['user_id'],
                        'game_level_id': session['level'],
                        'score': session['score'],
                        'question_total': session['question_total'],
                        'question_correct': session['question_correct']
                    }
                    result = Games.save_score(data)
                    print('*** 500T ***', result)

        return render_template("%s_play.html" % game_type)
        # return render_template("/games/addition.html", user=user, data=data)
    else:
        return redirect("/login")




