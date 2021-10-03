from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Logins:
    def __init__(self, data):
        self.id=data['id']
        self.fname=data['first_name']
        self.lname=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def submit(cls,data):
        query="INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s, now(), now());"
        return connectToMySQL('games').query_db(query,data)

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['fname']) < 2:
            flash("First name is too short.")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last name is too short.")
            is_valid = False
        if len(data['email']) < 4:
            flash("Email is too short.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.")
            is_valid = False
        else:
            print("***  100A ***", data)
            query="SELECT * FROM users WHERE email = %(email)s;"
            result = connectToMySQL('games').query_db(query, data)
            print("***  100B ***", query, result)
            if result:
                flash("Account already exists")
                is_valid = False
        return is_valid

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('games').query_db(query, data)
        if not results:
            return False
        elif len(results) < 1:
            return False
        print("*** 800A ***", results)
        return cls(results[0])

    @staticmethod
    def validate_password_format(data):
        is_valid = True
        if not (data['password']):
            flash("Please enter Password")
            is_valid = False
        elif len(data['password']) < 8:
            flash("Password is too short.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_password_match(data):
        is_valid = True
        print('*** 300A ***', data['password'], data['password_confirm'])
        if data['password'] != data['password_confirm']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_email(data):
        is_valid = True
        if not (data['email']):
            flash("Invalid email/password")
            is_valid = False
        return is_valid
