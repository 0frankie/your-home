from flask import Flask
from pyngrok import ngrok
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from globals import db

# Create the Flask app
app = Flask(__name__, instance_relative_config=True)

DB_NAME = "app.db"
DB_PATH = os.path.join("./instance", DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Define a route
@app.route("/")
def home():
    return "Hello, Flask!"


# Run the app
if __name__ == "__main__":

    app.run(debug=True, port=5000, host='0.0.0.0')
