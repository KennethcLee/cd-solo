import re, random
from flask import Flask, request, redirect, render_template, session, url_for, flash, jsonify
from flask.templating import render_template_string
from flask_app.models.login import Logins
from flask_app.models.game import Games
from flask_app.models.score import Scores
from flask_app.models.sentencesorting import SentenceSorting
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
            # 'game_type': 'addition' 
        }
        user=Logins.get_user(data)
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
        print('*** 300A ***', data)
        get_menu_data=Games.get_menu_data(data);
        session['game_type']=game_type
        session['game_name']=get_menu_data[0].game_name
        session['gameover']=False
        session['question_total']=0
        session['question_correct']=0
        session['score']=0
        user=Logins.get_user(data)
        print('*** 300B ***', get_menu_data[0].game_name)
        print('*** 300C ***', session['game_name'])
        return render_template("game_menu.html", user=user, data=data, get_menu_data=get_menu_data)
    else:
        return redirect("/login")

@app.route("/games/<string:game_type>/<int:level>/loading", methods=['GET', 'POST'])
def game_load(game_type, level):
    #Load Game data for all games
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
                session['min_element']=game_level_data.min_element
                session['max_element']=game_level_data.max_element
                session['min_line']=game_level_data.min_line
                session['max_line']=game_level_data.max_line
                session['max_question']=game_level_data.max_question
                session['score_question']=game_level_data.score_question
                session['question_total'] = 0
                session['question_correct'] = 0
                session['question_incorrect'] = 0
                if session['game_type'] == "sentencesorting":
                    session['language'] = request.form['language']
                print('*** 400C ***', level, type(level), session['level'], type(session['level']), request.form, game_level_data, game_level_data.min_element)
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

            #Game Logic for Addition
            element = 0
            if session['game_type']=="addition":
                if session['question_total'] == 0:
                        #Generate Mininum number for random range
                        min_num='1'
                        element = session['min_element']
                        while element > 1:
                            min_num += '0'
                            element -= 1
                        min_num=int(min_num)
                        session['min_num']=min_num

                        #Generate Maximum number for random range
                        max_num='9'
                        element = session['max_element']
                        while element > 1:
                            max_num += '9'
                            element -= 1
                        max_num=int(max_num)
                        session['max_num']=max_num
                        print('*** 500F ***', min_num, type(min_num), max_num, type(max_num))
                else:
                #Check answer and calculate score
                    session['answer'] = int(request.form['answer'])
                    print('*** 500G ***', session['answer'], type(session['answer']))
                    validate = 0
                    for j in session['question_data']:
                        validate += j
                    if session['answer'] == validate:
                        session['question_correct'] += 1
                        session['score'] += session['score_question']
                        print('*** 500H ***', session['question_total'], session['question_correct'], session['question_incorrect'])

                if session['question_total'] < session['max_question']:
                #Check if not reach maximum question, generate question data and tally scores
                    question_data=[]

                    for j in range(0, session['max_line']):
                        question_data.append(randrange(session['min_num'], session['max_num'] + 1))

                    print('*** 500M ***', question_data)
                    session['question_data']=question_data
                    session['question_incorrect']=session['question_total']-session['question_correct']
                    session['question_total']+=1
                    print('*** 500R ***', session)
                else:
                #Ends game when reaches maxiumum question
                    session['gameover'] = True
                    data = {
                        'user_id': session['user_id'],
                        'game_level_id': session['level'],
                        'score': session['score'],
                        'question_total': session['question_total'],
                        'question_correct': session['question_correct']
                    }
                    result = Scores.save_score(data)
                    print('*** 500S ***', result)

            #Game logic for Sentence Sorting
            elif session['game_type']=="sentencesorting":
                print('*** 600A ***', session['question_total'], session['question_total'] > 0)
                if session['question_total'] > 0:
                    session['answer'] = list(map(int, (request.form['answer'].split(','))))
                    print('*** 600B ***', session['answer'], type(session['answer']))
                    validate = []
                    for j in range(0, len(session['answer'])):
                        validate.append(j)
                    if session['language'] in ['ar']:
                            validate.reverse()
                            print('*** 600M2 ***', validate)
                    print('*** 600C ***', session['answer'], type(session['answer']), validate)
                    if session['answer'] == validate:
                        session['question_correct'] += 1
                        session['score'] += session['score_question']
                        print('*** 600D ***', session['question_total'], session['question_correct'], session['question_incorrect'])
                #Check end of game or another question for Sentence Sorting
                if session['question_total'] < session['max_question']:
                    data = {
                        'game_type': session['game_type'],
                        'level': session['level'],
                        'max_question': session['max_question']
                    }
                    print('*** 600L2 ***', session['language'])

                    questions = SentenceSorting.get_game_data(data, 'en', session['language'])
                    print('*** 600M ***', questions, questions[0].game_data, session['question_total'])
                    #Asian language single sentence format do not use spaces
                    if session['language'] in ['zh-cn', 'ko-KR', 'ja']:
                        validate = list(questions[0].game_data)
                    else :
                        validate = list( (questions[0].game_data).split(" ") )
                    question_data = []
                    for j in range(0, len(validate)):
                        question_data.append([j, validate[j]])
                    random.shuffle(question_data)
                    session['question_data']=question_data
                    session['question_incorrect']=session['question_total']-session['question_correct']
                    session['question_total']+=1
                    print('*** 600N ***', question_data, validate)
                else:
                    session['gameover'] = True
                    data = {
                        'user_id': session['user_id'],
                        'game_level_id': session['level'],
                        'game_type': session['game_type'],
                        'score': session['score'],
                        'question_total': session['question_total'],
                        'question_correct': session['question_correct']
                    }
                    result = Scores.save_score(data)
                    print('*** 600Q ***', result)
        print('*** 600R ***')
        return render_template("%s_play.html" % game_type)
    else:
        return redirect("/login")




