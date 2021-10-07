from os import stat
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.login import Logins

class SentenceSorting:
    def __init__(self, data):
        self.id=data['id']
        self.num_element=data['num_element']
        self.game_data=data['game_data']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_game_data(cls, data):
        print('***  9000  ***', data)
        query = "SELECT sentence_sorting_data.id, num_element, game_data, sentence_sorting_data.created_at, sentence_sorting_data.updated_at FROM sentence_sorting_data JOIN game_level_sentence_sorting_data ON game_level_sentence_sorting_data.id = sentence_sorting_data.id JOIN game_level ON game_level_sentence_sorting_data.game_level_id = game_level.id WHERE game_level.level = %(level)s AND game_type=%(game_type)s ORDER BY RAND() LIMIT 10"
        result = []
        questions = connectToMySQL('games').query_db(query, data)
        print('***  9000A  ***', query)
        print('***  9000B  ***', questions)
        for j in questions:
            result.append(cls(j))
        print('***  9000B  ***', result)
        return result

