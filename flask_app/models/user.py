from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, redirect
from flask_app.models.recipe import Recipe


class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

    # returns a user id 
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("recipes").query_db(query, data)


    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL("recipes").query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_reg(data):
        is_valid = True
        
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


        if len(data["first_name"]) <= 2 or not data["first_name"].isalpha(): 
            flash("You last name must be longer than 2 characters.")
            is_valid = False
        
        if len(data["last_name"]) <= 2 or not data["last_name"].isalpha():
            flash("You last name must be longer than 2 characters of the English alphabet.")
            is_valid = False

        if not email_regex.match(data["email"]):  
            flash("Please enter a valid email.")
            is_valid = False


        if User.get_user_by_email(data): 
            flash("Email address already exsits!")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be 8 or more characters")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("passwords must match")
            is_valid = False

        return is_valid
        
    @classmethod
    def get_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = %(user_id)s WHERE users.id = %(user_id)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        user = cls(results[0])
        print(user)
        print(user.first_name)

        for row in results: 

            recipe_data = {
            "id": row["recipes.id"],
            "name": row["name"],
            "description": row["description"],
            "instructions": row["instructions"],
            "under_30": row["under_30"],
            "made_on": row["made_on"]
            }


            user.recipes.append(Recipe(recipe_data))
        return user