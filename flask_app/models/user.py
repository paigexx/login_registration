from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # returns a user id 
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("login_registration").query_db(query, data)


    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL("login_registration").query_db(query,data)
        # That conditional is important in case that the query is empty. without the conditional it will crash
        if len(results) < 1: 
            return False
        print(results)
        # DONT forget to wrap in clas
        return cls(results[0])

    @staticmethod
    def validate_reg(data):
        is_valid = True
        #  add a validation for only letters for first/last name

        if len(data["first_name"]) <= 2: 
            flash("You last name must be longer than 2 characters.")
            is_valid = False
        
        if not data["first_name"].isalpha():
            flash("You name must be within the characters of the English alphabet.")
            is_valid = False
        
        
        if len(data["last_name"]) <= 2: 
            flash("You last name must be longer than 2 characters.")
            is_valid = False

        if not data["last_name"].isalpha():
            flash("You name must be within the characters of the English alphabet.")
            is_valid = False
        

        if not email_regex.match(data["email"]):
            flash("Please enter a valid email.")
            is_valid = False

        if len(data["password"]) < 8:
            flash("password must be 8 or more characters")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("passwords must match")
            is_valid = False

        return is_valid
        
