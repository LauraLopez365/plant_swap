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
    
    
    
    Plant.create_plant_post(plant_data)

    return redirect("/dashboard")


@app.route("/plant/<int:plant_id>/show")
def show_one_plant(plant_id):
    if not "user_id" in session:
        return redirect("/login")

    data={
        "id":session["user_id"]
    }
    print(data)
    this_user=User.get_user_by_id(data)
    one_plant_w_creator=Plant.show_one_plant_w_creator(plant_id)

    return render_template("show_one_plant.html",this_user=this_user,one_plant_w_creator=one_plant_w_creator)

@app.route("/plant/<int:plant_id>/edit")
def edit_one_plant(plant_id):
    if not "user_id" in session:
        return redirect("/login")
        
    data={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data)
    plant_to_edit=Plant.show_one_plant_w_creator(plant_id)

    return render_template("edit_one_plant.html",this_user=this_user,plant_to_edit=plant_to_edit)


@app.route("/plant/<int:plant_id>/save_edit", methods=["POST"])
def save_plant_edit(plant_id):

    if not Plant.validate_plant(request.form):
        return redirect(f"/user/{plant_id}/edit")


    plant_data ={
        "id": plant_id,
        "plant_name": request.form["plant_name"],
        "image_path": request.form["image_path"],
        "plant_requests": request.form["plant_requests"],
        "plant_info": request.form["plant_info"]
        }
    


    Plant.update_plant_info(plant_data)

    return redirect("/dashboard")



@app.route("/plant/<int:id>/delete")
def delete_one_plant(id):
    if not "user_id" in session:
        return redirect("/login")
    Plant.delete_plant(id)
    
    return redirect("/dashboard")


#need to add session user plants on the html page and put the requested swap on the page as well with som way to link them
@app.route("/plant/<int:id>/swap")
def request_swap(id):
    if not "user_id" in session:
        return redirect("/login")
    
    data={
        "id":session["user_id"]
    }
    
    this_user=User.get_user_by_id(data)
    one_plant_w_creator=Plant.show_one_plant_w_creator(id)
    users_plants=Plant.get_all_plants_from_creator(data)

    return render_template("set_up_a_swap.html",this_user=this_user,one_plant_w_creator=one_plant_w_creator, users_plants=users_plants)

# invisible route to create list
@app.route("/plant/<int:plant_id>/complete_swap", methods=["POST"])
def complete_swap(plant_id):


    Plant.add_to_trades(plant_id,)


    return redirect("dashboard")

@app.route("/user/<int:user_id>/swap_list")
def show_swaps(user_id):
    if not "user_id" in session:
        return redirect("/login")
    
    data={
        "id":session["user_id"]
    }
    this_user=User.get_user_by_id(data)
    plant_swap=Plant.get_plant_w_creator_and_trades(1)
    

    return render_template("dashboard.html",this_user=this_user,plant_swap=plant_swap)

