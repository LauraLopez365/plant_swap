from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.plant_model import Plant

#root route=login page
@app.route("/")
def index():
    return redirect("/login")

#this route takes to a page to imput data to create a new plant object
@app.route("/plant/new")
def create_plant_post():
    if not "user_id" in session:
        return redirect("/")
    
    return render_template("create_plant_post.html")

# route to save new plant_post, invisible route
@app.route("/plant_post/create", methods=["POST"])
def plant_new():

    plant_data={
        "plant_name":request.form["plant_name"],
        "image_path":request.form["image_path"],
        "plant_requests":request.form["plant_requests"],
        "plant_info": request.form["plant_info"],
        "user_id":session['user_id'],
    }


    if not Plant.validate_plant(plant_data):
        return redirect("/plant/new")
    
    
    
    Magazine.create_magazine(magazine_data)

    return redirect("/dashboard")