from os import stat
from flask import flash 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.login import Logins
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Games:
    def __init__(self, data):
        self.id=data['id']
        self.game_type=data['game_type']
        self.game_name=data['game_name']
        self.level=data['level']
        self.min_element=data['min_element']
        self.max_element=data['max_element']
        self.min_line=data['min_line']
        self.max_line=data['max_line']
        self.max_question=data['max_question']
        self.score_question=data['score_question']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_menu_data(cls, data):
        print('***  3000  ***')
        query = "SELECT * FROM game_level WHERE game_type = %(game_type)s ORDER BY level"
        print('***  3000A  ***', query)
        result = []
        levels = connectToMySQL('games').query_db(query, data)
        print('***  3000B  ***', result)
        for j in levels:
            result.append(cls(j))
        return result

    @classmethod
    def get_level_data(cls, data):
        print('***  3100  ***')
        query = "SELECT * FROM game_level WHERE game_type = %(game_type)s AND level = %(level)s"
        print('***  3100A  ***', query)
        result = connectToMySQL('games').query_db(query, data)
        print('***  3100B  ***', result[0])
        return cls(result[0])
