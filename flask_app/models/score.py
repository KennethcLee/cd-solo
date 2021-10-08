from os import stat
from flask import flash 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Scores:
    def __init__(self, data):
        self.id=data['id']
        self.user_id=data['user_id']
        self.game_type=data['game_type']
        self.game_name=data['game_name']
        self.level=data['level']
        self.first_name=data['first_name']
        self.score=data['score']
        self.created_at=data['scores.created_at']
        self.updated_at=data['scores.updated_at']

    @classmethod
    def get_all(cls, data):
        print('***  2000  ***')
        query = "SELECT * FROM users JOIN scores on users.id = scores.user_id JOIN game_level on scores.game_level_id = game_level.id WHERE game_type = %(game_type)s ORDER BY score DESC LIMIT 10"
        results = connectToMySQL('games').query_db(query, data)
        print("***   100 SCORE   ***", results )
        scores = []
        if results:
            for j in results:
                scores.append(cls(j))
        return scores

    @classmethod
    def save_score(cls, data):
        print('***  4000  ***')
        query = "INSERT INTO scores(user_id, game_level_id, score, question_total, question_correct, created_at, updated_at) VALUES (%(user_id)s, (SELECT id FROM game_level WHERE game_type = %(game_type)s AND level = %(game_level_id)s), %(score)s, %(question_total)s, %(question_correct)s, now(), now())"
        print('***  4000A  ***', query)
        return connectToMySQL('games').query_db(query, data)


