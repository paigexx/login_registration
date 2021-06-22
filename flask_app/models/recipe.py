from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    def __init__(self, data): 
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions  = data["instructions"]
        self.under_30 = data["under_30"]
        self.made_on = data["made_on"]

    @classmethod
    def get_recipe(cls, data): 
        query = "SELECT * FROM recipes WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL("recipes").query_db(query,data)
        print(results[0])
        return results[0]

    @classmethod 
    def create_recipe(cls, data): 
        query = "INSERT INTO recipes (user_id, name, description, instructions, under_30, made_on) VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(made_on)s);"
        results = connectToMySQL("recipes").query_db(query, data)
        print("Recipe added successfully!")
        return results

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(recipe_id)s;"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, made_on = %(made_on)s WHERE recipes.id = %(recipe_id)s;"
    
        modified_data = {
            "recipe_id": data["recipe_id"],
            "name": data["name"],
            "description": data["description"],
            "instructions": data["instructions"],
            "under_30": data["under_30"],
            "made_on": data["made_on"]
        }

        result = connectToMySQL("recipes").query_db(query,modified_data)
        return result

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data["name"]) < 3: 
            flash("Name must be three characters")
            is_valid = False
        
        if len(data["description"]) < 3: 
            flash("Description must be three characters")
            is_valid = False

        if len(data["instructions"]) < 3: 
            flash("Instructions must be three characters")
            is_valid = False   

        return is_valid