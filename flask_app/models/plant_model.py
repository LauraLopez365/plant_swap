from flask_app.config.mysqlconnection import connectToMySQL
#might need other import like flash or other classes and regex
from flask_app.models import user_model

from flask import Flask, request, session

from flask import flash

DB="plant_swapr"

class Plant:
    def __init__(self,data):
        self.id=data["id"]
        self.plant_name=data["plant_name"]
        self.image_path=data["image_path"]
        self.plant_requests=data["plant_requests"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user=None

    @classmethod
    def create_plant_post(cls,data):

        query="""INSERT INTO plants(plant_name,image_path,plant_requests,plant_info,user_id)
        VALUES (%(plant_name)s,%(image_path)s,%(plant_requests)s,%(plant_info)s,%(user_id)s);"""

        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def get_all_plants_from_creator(cls,data):
        query = "SELECT * FROM plants WHERE user_id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DB).query_db(query,data)
        # Create an empty list to append our instances of plants
        plants = []
        # Iterate over the db results and create instances of recipes with cls.
        for magazine in results:
            magazines.append(cls(magazine))
        return magazines