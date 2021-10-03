from os import stat
from flask import flash 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.login import Logins
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Thoughts:
    def __init__(self, data):
        self.id=data['id']
        self.user_id=data['user_id']
        self.thought=data['thought']
        self.likes=data['likes']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO thoughts(user_id, thought, likes, created_at, updated_at) VALUES (%(user_id)s, %(thought)s, 0, now(), now());"
        return connectToMySQL('thoughts').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM thoughts JOIN users ON users.id = thoughts.user_id"
        results = connectToMySQL('thoughts').query_db(query)
        thoughts = []
        if results:
            for j in results:
                thought = cls(j)
                thought.user = Logins(j)
                print('***  2000  ***', thought.user.fname)
                thoughts.append(thought)
        return thoughts

    @classmethod
    def like(cls, data):
        query = "UPDATE thoughts SET likes = likes + 1 WHERE id = %(id)s;"
        print('***  2010A  ***', data['id'])
        return connectToMySQL('thoughts').query_db(query, data)

    @classmethod
    def dislike(cls, data):
        query = "UPDATE thoughts SET likes = likes - 1 WHERE id = %(id)s;"
        print('***  2010B  ***', data['id'])
        return connectToMySQL('thoughts').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        print('***  2010C  ***', data['id'])
        return connectToMySQL('thoughts').query_db(query, data)

    @classmethod
    def get_all_user(cls, data):
        query = "SELECT * FROM thoughts JOIN users ON users.id = thoughts.user_id WHERE users.id = %(id)s"
        results = connectToMySQL('thoughts').query_db(query, data)
        thoughts = []
        print('***  2030  ***')
        if results:
            for j in results:
                print('***  2030A  ***')
                thought = cls(j)
                thought.user = Logins(j)
                print('***  2030B  ***', thought.user.fname)
                thoughts.append(thought)
        return thoughts

    @staticmethod
    def validate_thought(data):
        is_valid = True
        if len(data['thought']) < 5:
            flash("Thought needs to be at least 5 characters")
            is_valid = False
        return is_valid
