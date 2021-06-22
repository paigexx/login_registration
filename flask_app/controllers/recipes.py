import re
from flask.templating import render_template_string
from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models.recipe import Recipe

@app.route("/recipe/<int:recipe_id>")
def show_instructions(recipe_id):
    data = {
        "recipe_id": recipe_id
    }
    recipe = Recipe.get_recipe(data)
    return render_template("recipe_show.html", recipe = recipe)

@app.route("/user/create_recipe")
def create_recipe():
    return render_template("new_recipe.html")

@app.route("/recipe/new_recipe", methods=['POST'])
def new_recipe():
    data = {
        "user_id": session["user_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "made_on": request.form["made_on"],
        "under_30": request.form["under_30"],
    }
    print("validating")

    if not Recipe.validate_recipe(request.form): 
        print("not valid")
        return redirect("/user/create_recipe")

    Recipe.create_recipe(data)
    return redirect("/user/homepage")

@app.route("/recipe/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    data = {
        "recipe_id": recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect("/user/homepage")

@app.route("/recipe/edit/<int:recipe_id>")
def edit_recipe_render(recipe_id):
    data = {
        "recipe_id": recipe_id
    }
    recipe = Recipe.get_recipe(data)
    return render_template("edit_recipe.html", recipe = recipe)

@app.route("/recipe/edit/<int:recipe_id>/form",methods = ["POST", "GET"])
def edit_recipe(recipe_id):
    if request.form: 
        print(request.form)
        data = {
            "recipe_id": recipe_id,
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "under_30": request.form["under_30"],
            "made_on": request.form["made_on"]
        }
        Recipe.edit_recipe(data)
    return redirect(f"/recipe/{recipe_id}")