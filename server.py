# It took me a while to understand with modularization, but the server.py imports the controllers, and the controllers imports the models. So that ideally puts all of it in the server.py
from flask_app import app #import flask so we can use it
from flask_app.controllers import users_controller
from flask_app.controllers import plants_controller



if __name__=='__main__':
    app.run(debug=True, host="localhost", port=5002)