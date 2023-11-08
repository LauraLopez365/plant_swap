from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.plant_model import Plant
# #need the following 2 lines to run bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def reroute():
    return redirect("/login")

# route to login
@app.route("/login")
def users_index():
    return render_template("login.html")


#invisible login route
@app.route("/login", methods=["POST"])
def login():
    #return the user object if the validation is true on the models page
    print(request.form)
    found_user_or_none= User.validate_login(request.form)

    if not found_user_or_none:
        return redirect("/login")

    session["user_id"]=found_user_or_none.id
    return redirect("/dashboard")

#invisible registration route, runs the constructor method
@app.route("/register", methods=["POST"])
def register():

    user_in_db=User.get_by_email(request.form["email"])
    if user_in_db:
        flash("email already in use")
        return redirect("/login")

    if not User.validate_registration(request.form):
        return redirect("/login")
    #confirm password and confirm password fields match


    data ={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
        }
    print("*"*60)
    session["user_id"] = User.create_user(data)
    
    
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        return redirect("/login")
    

    data={
        "id":session["user_id"]
    }
    print(data)
    this_user=User.get_user_by_id(data)
    # plant_swap=Plant.get_plant_w_creator_and_trades(data)

#need to create new dashboard for plants info
    return render_template("dashboard.html", this_user=this_user,plants=Plant.get_plants_with_users())

@app.route("/user/<int:id>/edit")
def edit_one_user(id):
    if not "user_id" in session:
        return redirect("/login")
    print(id)
    data={
        "id":session["user_id"]
    }
    user_to_edit=User.get_user_by_id(data)

    print("got to line 82")

    return render_template("edit_one_user.html",user_to_edit=user_to_edit)




#invisisble route to save user edits
@app.route("/user/<int:user_id>/save_edit", methods=["POST"])
def save_user_edit(user_id):

    if not User.validate_user(request.form):
        return redirect(f"/user/{user_id}/edit")

    

    user_data ={
        "user_id":session["user_id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
        }
    


    User.update(user_data)

    return redirect("/dashboard")


#route to logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")