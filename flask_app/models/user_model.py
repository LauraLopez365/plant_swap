from flask_app.config.mysqlconnection import connectToMySQL
#might need other import like flash or other classes and regex
from flask import Flask, session,request
from flask_app.models import plant_model
from flask_app.models import user_model
from flask import flash
import re #regex model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)

#schema name in workbench cannot match a table name
DB="plant_swapr"

class User:
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.plants= []
        #linking many recipes to this user line 25
        #follow database table fields plus any data you want to create
        #link to other classes here!
        

#method for creating a new user instance
    @classmethod
    def create_user(cls,data):

        query="""INSERT INTO users(first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""

        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        print(data)
        data={
            "id":data["user_id"],
            "first_name":data["first_name"],
            "last_name":data["last_name"],
            "email":data["email"],
            }
        print("in update class method")
        query=""" 
        UPDATE users 
        SET id=%(id)s, first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
        WHERE id= %(id)s
        ;"""

        return connectToMySQL(DB).query_db(query,data) 
    
    @classmethod
    def get_user_by_id(cls,id):
        print("im hereeeeeeeeeeeee in get user by id")

        

        query="""
        SELECT * FROM users
        WHERE id = %(id)s;
        """

        results= connectToMySQL(DB).query_db(query,id) #was{"id:id"}
        print(results)
        if len(results) == 0:
            return None
        else:
            return cls(results[0]) #create user object called by id from the database
            


#method for retrieving all data from the users table
    @classmethod
    def get_all_users(cls):
        query="SELECT * FROM users;"
        results= connectToMySQL(DB).query_db(query)
        #rest of code here
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_by_email(cls,email):
        print("data", email)
        email_dict={"email":email}
        print("email_dict", email_dict)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,email_dict)
        # Didn't find a matching user
        print("result", result)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_with_plants(cls,data): 

        query= """SELECT * FROM users 
        LEFT JOIN plants ON users.id = plants.user_id 
        WHERE users.id=%(id)s"""
        print("im here in the user_model line 110")
        results = connectToMySQL(DB).query_db(query,data) 
        print(results)
        
   #####need to update here the attributes for plants####     
        for row_from_db in results:
            users_holder= []
            plant_data = { 
                "id" : row_from_db["plants.id"],
                "plant_name" : row_from_db["plant_name"],
                "image_path" : row_from_db["image_path"],
                "plant_requests" : row_from_db["plant_requests"],
                "plant_info": row_from_db["plant_info"],
                "user_id": row_from_db["user_id"],
                "created_at": row_from_db["plants.created_at"],
                "updated_at": row_from_db["plants.updated_at"]
            
            }

            users_holder.plants.append(plant_model.Plant(plant_data))
#variablename.constructor name in dojo.append can be used on the array,import name,class name, variable for new object created by the query
#one of the rows im getting back from the join statement

        print("users_holder", users_holder)
        return users_holder
    

    

    @staticmethod
    def validate_registration(data):

        
        is_valid = True
        
        
        if len(data["first_name"]) < 3:
            flash("First name must be 3 or more characters")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("Last name must be 3 or more characters")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid email address!")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be 8 characters")
            is_valid = False
        if data["password"] != data["confirm_pw"]:
            flash("Passwords do not match")
            is_valid= False
        return is_valid
    
    @staticmethod
    def validate_login(data):

        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid login credentials!")
            return False #stop immediately does no match database


        print("this is my print",data)
        #find user in database by email

        found_user_or_none = User.get_by_email(data['email'])
        print(found_user_or_none)
        if found_user_or_none == False:
            flash("Invalid login credentials!")
            return False
        #check password
        if not bcrypt.check_password_hash(found_user_or_none.password, data["password"]):
            flash("Invalid login credentials!")
            return False
        

        return found_user_or_none
    
    @classmethod
    def validate_user(cls,user_data):

        is_valid=True

        
        if len(user_data["first_name"]) < 3:
            flash("First name must be 3 or more characters")
            is_valid = False
            
        if len(user_data["last_name"]) < 3:
            flash("Last name must be 3 or more characters")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user_data["email"]): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid