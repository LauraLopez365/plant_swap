from flask_app.config.mysqlconnection import connectToMySQL
#might need other import like flash or other classes and regex
from flask_app.models import user_model

from flask import Flask, request, session

from flask import flash

DB="plant_swap2"

class Plant:
    def __init__(self,data):
        self.id=data["id"]
        self.plant_name=data["plant_name"]
        self.image_path=data["image_path"]
        self.plant_requests=data["plant_requests"]
        self.plant_info=data["plant_info"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.creator=None
        self.trade=[]

    @classmethod
    def create_plant_post(cls,data):

        query="""INSERT INTO plants(plant_name,image_path,plant_requests,plant_info,user_id)
        VALUES (%(plant_name)s,%(image_path)s,%(plant_requests)s,%(plant_info)s,%(user_id)s);"""

        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def get_all_plants_from_creator(cls,data):
        print("im here in the plant model line 32.")
        query = "SELECT * FROM plants WHERE user_id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DB).query_db(query,data)
        print(results)
        # Create an empty list to append our instances of plants
        plants = []
        # Iterate over the db results and create instances of recipes with cls.
        for plant in results:
            plants.append(cls(plant))
        print(plants)
        return plants
    
    @classmethod
    def validate_plant(cls,data):

        is_valid = True

        if len(data["plant_name"]) < 2:
            flash("Plant name must be at least 2 Characters")
            is_valid = False
        if len(data["plant_requests"]) < 5:
            flash("Plant requests must be at least 5 Characters")
            is_valid = False
        if len(data["plant_info"]) < 5:
            flash("Plant information must be at least 5 Characters")
            is_valid = False
        
        return is_valid
    

    @classmethod
    def update_plant_info(cls,plant_data):
        print(plant_data)

        query=""" 
        UPDATE plants 
        SET id=%(id)s,plant_name=%(plant_name)s, image_path=%(image_path)s, plant_requests=%(plant_requests)s, plant_info=%(plant_info)s
        WHERE id= %(id)s
        ;"""

        return connectToMySQL(DB).query_db(query,plant_data) 
    


    @classmethod
    def get_plants_with_users(cls):
        query = """SELECT *  
                FROM plants 
                JOIN users
                ON plants.user_id = users.id
        ;"""
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DB).query_db(query)
        # Create an empty list to append our instances of friends
        print("results",results)
        
        plants_holder=[]
        # Iterate over the db results and create instances of plants with cls.
        for row_from_db in results:
            plant_objects =cls(row_from_db) #hold all the recipe information and appends all the user information to the referenced object( if there is a where clause this goes outside of the for loop)
            
            user_data = { 
                "id" : row_from_db["users.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "password" : row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            
            }
            plant_objects.creator=(user_model.User(user_data))#
            plants_holder.append(plant_objects)
            
        print("a",plants_holder)#recipe holder
        return plants_holder
    

    @classmethod
    def show_one_plant_w_creator(cls,id):
    
        query="""SELECT * FROM plants JOIN users
        ON plants.user_id=users.id
        WHERE plants.id=%(id)s;"""

        results = connectToMySQL(DB).query_db(query,{'id': id})
        print(results[0])

        
        # Iterate over the db results and create instances of friends with cls.
        one_plant_holder=cls(results[0])
        #hold all the recipe information and appends all the user information to the referenced object(where clause goes outside of the for loop)
        for row_from_db in results:

            user_data_results = { 
                "id" : row_from_db["users.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "password" : row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            
                }
            one_plant_holder.creator=(user_model.User(user_data_results))#the right side replaces "None" in the constructor method, One_recipe_holder follows the same constructor method, but is named differently then the user data is replaced when we get the query results back with the user information

        

            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",one_plant_holder)#recipe holder
        return one_plant_holder
    

    @classmethod
    def get_plant_w_creator_and_trades(cls,plant_id):

        query="""
            SELECT * FROM plants
            LEFT JOIN trades on plant.id=trades.plant_id
            LEFT JOIN users ON trades.user_id=users.id
            JOIN users AS creator ON plants.user_id=creator.id
            WHERE plants.id= %(id)s;
            """
        
        results = connectToMySQL(DB).query_db(query,{'id': id})
        if results:

            plant_swap=cls(results[0])

            plant_swap.creator= user_model.User({
            "id":results[0]["creator.id"],
            "first_name":results[0]["creator.first_name"],
            "last_name":results[0]["creator.last_name"],
            "email":results[0]["creator.email"],
            "password":results[0]["creator.password"],
            "created_at":results[0]["creator.created_at"],
            "updated_at":results[0]["creator.updated_at"],

            })
            for result in results:
                if result["trades.user_id"]:

                    plant_swap.trade.append(user_model.User({
                        "id":result["id"],
                        "first_name":result["first_name"],
                        "last_name":result["last_name"],
                        "email":result["email"],
                        "password":result["password"],
                        "created_at":result["created_at"],
                        "updated_at":result["updated_at"],
                            }))

            return plant_swap
        return None
        

        


    @classmethod
    def delete_plant(cls,id):
        query="""Delete FROM plants WHERE id=%(id)s;"""
        return connectToMySQL(DB).query_db(query,{"id":id})